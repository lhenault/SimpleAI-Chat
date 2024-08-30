import logging
from typing import Any, Optional
import time
import asyncio

import functools
from dotenv import load_dotenv

from chat_client import SimpleChatClient
from db import get_context
from config import (
    API_KEY,
    BASE_URL,
)

load_dotenv()

chat_client = SimpleChatClient(
    api_key=API_KEY,
    base_url=BASE_URL,
)

models = chat_client.list_models()

def run_in_executor(f):
    @functools.wraps(f)
    async def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: f(*args, **kwargs))

    return inner


def format_chat_log(chat_log: list[dict]):
    formatted_chat_log = []
    for message_pair in chat_log:
        formatted_chat_log.append({"role": "user", "content": message_pair.get("input")})
        formatted_chat_log.append({"role": "assistant", "content": message_pair.get("response")})
    return formatted_chat_log


@run_in_executor
def get_response(
    message: str, 
    history: Optional[list[dict]] = None, 
    summary: Optional[Any] = None,
):
    logging.info(f"Input: {message}")
    logging.info(f"Context: {history}")
    
    start = time.time()
    
    if history is None:
        history = []
    
    messages = format_chat_log(
        chat_log=history
    ).append({"role": "user", "content": message})
    
    logging.info(f"Formatted log: {messages}")
    
    response = ""
    
    for token in chat_client.chat(
        messages=messages, 
        model_id=models[0],
        system_prompt=get_context(),
    ):
        response += token
        
    logging.info(f"Response: {response}")

    end = time.time()
    return response, end - start

@run_in_executor
def summarise_text(text: str):
    messages = [
        {
            "role": "user", 
            "content": f"Summarise this chat, be concise and don't go for longer than a few sentences."
        },
        {
            "role": "user", 
            "content": text
        },
    ]
    response = ""
    
    for token in chat_client.chat(
        messages=messages, 
        model_id=models[0],
        system_prompt="You are a helpful assistant who is paying attention to details.",
    ):
        response += token
        
    logging.info(f"Produced summary: {response}")
    return response