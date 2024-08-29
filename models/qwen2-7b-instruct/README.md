# MosaicML's MPT-7B-Chat

## Description

This example shows how to use [Qwen2 &b Instruct](https://github.com/QwenLM/Qwen2), with a [SimpleAI](https://github.com/lhenault/simpleAI) server.

It implements `chat` methods for both streaming and non-streaming.

## Setup

First build the image with:

```bash
docker build . -t alibaba-qwen2-instruct:latest
```

Then declare your model in your *SimpleAI* configuration file `models.toml`:

```toml
[Qwen2-7B-Instruct]
    [Qwen2-7B-Instruct.metadata]
        owned_by    = 'Alibaba Qwen Team'
        permission  = []
        description = 'Qwen2 7B instruct model'
    [Qwen2-7B-Instruct.network]
        type = 'gRPC'
        url = 'simple-ai-model-01:50051'
```

## Start service

Just start your container with:

```bash
docker run -it --rm -p 50051:50051 --gpus all alibaba-qwen2-instruct:latest
```

And start your *SimpleAI* instance, for instance with:

```bash
simple_ai serve [--host 127.0.0.1] [--port 8080]
```
