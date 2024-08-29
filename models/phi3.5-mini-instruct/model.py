import logging
from dataclasses import dataclass
from threading import Event, Thread
from typing import Optional, Union

import torch
from get_models import MODEL_ID
from simple_ai.api.grpc.chat.server import LanguageModel
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer,
)

@dataclass
class StopOnTokens(StoppingCriteria):
    stop_token_ids: Optional[Union[list, tuple]]

    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        stop_tokens = self.stop_token_ids
        if isinstance(stop_tokens, int):
            stop_tokens = (stop_tokens,)
        for stop_id in stop_tokens:
            if input_ids[0][-1] == stop_id:
                return True
        return False

MAX_SEQUENCE_LENGTH = 4096
MODEL_END_OF_TEXT = ("<|end|>", "-----")

@dataclass(unsafe_hash=True)
class ChatModel(LanguageModel):
    gpu_id: int = 0
    device = torch.device("cuda", gpu_id)
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, model_max_length=MAX_SEQUENCE_LENGTH, truncation_side="left"
    )
    config = AutoConfig.from_pretrained(MODEL_ID, trust_remote_code=True)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        config=config,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    ).to(device)

    def format_chat_log(self, chatlog: list[dict[str, str]] = dict()) -> str:
        return self.tokenizer.apply_chat_template(
            conversation=chatlog,
            tokenize=False,
            add_generation_prompt=True,
        )
        
    def chat(
        self,
        chatlog: list[list[str]] = None,
        max_tokens: int = MAX_SEQUENCE_LENGTH // 2,
        temperature: float = 0.9,
        top_p: int = 0.5,
        role: str = "assistant",
        end_of_text: Optional[Union[str, list, tuple]] = MODEL_END_OF_TEXT,
        *args,
        **kwargs,
    ) -> str:
        try:
            if end_of_text is None:
                end_of_text = self.tokenizer.eos_token
            
            if isinstance(end_of_text, str):
                end_of_text = (end_of_text,)

            logging.info(f"Preprocessing chatlog:\n{chatlog}")
            prompt = self.format_chat_log(chatlog=chatlog)

            logging.info(f"Input prompt:\n{prompt}")
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=MAX_SEQUENCE_LENGTH // 2,
            ).to(self.model.device)

            # Use Torch's Flash attention
            with torch.backends.cuda.sdp_kernel(
                enable_flash=True, enable_math=False, enable_mem_efficient=False
            ):
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    temperature=temperature,
                    top_p=top_p,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
                output = self.tokenizer.batch_decode(outputs)[0]
                logging.info(f"Model output:\n{output}")

                # Remove the context from the output
                output = output[len(prompt):]

                # Stop if end of text
                for item in end_of_text:
                    if item in output:
                        output = output.split(item)[0]
                    break

                # Avoid issues with GPU vRAM
                del inputs
                torch.cuda.empty_cache()

                return [{"role": role, "content": output}]
        except Exception as ex:
            logging.exception(ex)
        return

    def stream(
        self,
        chatlog: list[list[str]] = None,
        max_tokens: int = MAX_SEQUENCE_LENGTH // 2,
        temperature: float = 0.9,
        top_p: int = 0.5,
        role: str = "assistant",
        end_of_text: Optional[Union[str, list, tuple]] = MODEL_END_OF_TEXT,
        *args,
        **kwargs,
    ):
        try:
            if end_of_text is None:
                end_of_text = self.tokenizer.eos_token
                stop = StopOnTokens(
                    stop_token_ids=self.tokenizer.eos_token_id
                )
            else:
                if isinstance(end_of_text, str):
                    end_of_text = (end_of_text,)

                stop = StopOnTokens(
                    stop_token_ids=self.tokenizer.convert_tokens_to_ids(end_of_text)
                )

            # Yield role
            yield [{"role": role}]

            logging.info(f"Preprocessing chatlog:\n{chatlog}")
            prompt = self.format_chat_log(chatlog=chatlog)

            logging.info(f"Input prompt:\n{prompt}")
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=MAX_SEQUENCE_LENGTH // 2,
            ).to(self.model.device)

            logging.info(f"Input has {len(inputs[0])} tokens.")

            # Use Torch's Flash attention
            with torch.backends.cuda.sdp_kernel(
                enable_flash=True, enable_math=False, enable_mem_efficient=False
            ):
                # Generate stream, yield delta
                streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)
                generation_kwargs = dict(
                    **inputs,
                    streamer=streamer,
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    temperature=temperature,
                    top_p=top_p,
                    pad_token_id=self.tokenizer.eos_token_id,
                    stopping_criteria=StoppingCriteriaList([stop]),
                )

                stream_complete = Event()

                def generate_and_signal_complete(generation_kwargs=generation_kwargs):
                    self.model.generate(**generation_kwargs)
                    stream_complete.set()

                thread = Thread(target=generate_and_signal_complete)
                thread.start()

                logging.info("Output:")
                ended = False
                for delta in streamer:
                    if delta:
                        for item in end_of_text:
                            if item in delta:
                                logging.info(delta)
                                yield [{"content": delta.split(item)[0]}]
                                ended = True
                                break
                        if ended:
                            break
                        logging.info(delta)
                        yield [{"content": delta}]

                thread.join(timeout=60)

                # Avoid issues with GPU vRAM
                del streamer
                del inputs
                torch.cuda.empty_cache()

        except Exception as ex:
            logging.exception(ex)

        return
