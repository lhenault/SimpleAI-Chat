from typing import Iterable, Optional

from openai import OpenAI


class SimpleChatClient:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8080/",
        api_key: Optional[str] = None,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def list_models(self) -> Iterable:
        return [
            item.get("id") 
            for item in self.client.models.list().to_dict().get("data")
        ]
    
    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.8,
        model_id: str = "default",
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = 2048,
    ):
        if system_prompt is not None:
            messages = [dict(role="system", content=system_prompt), *messages]
        
        for chunk in self.client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        ):
            if hasattr(chunk.choices[0].delta, "content"):
                if isinstance(chunk.choices[0].delta.content, str):
                    yield chunk.choices[0].delta.content
