# Simple chat with AI models

This project showcases how one can use the [SimpleAI](https://github.com/lhenault/simpleAI) tool to use LLM, VLM or SLM AI models and chat with them "à la ChatGPT".

It aims for simplicity and can be extended or adapted for one's needs, and implements the following components:

- Model servers to predict tokens using a set of trained models,
- A SimpleAI server that links UI and models, exposing an API compatible with OpenAI's one,
- A basic chat UI to interact with models from any browser,
- And a Telegram integration in order to chat with models directly from this platform

## Installation

Install `Docker` and `docker-compose` and simply run:

```bash
docker-compose up
```
