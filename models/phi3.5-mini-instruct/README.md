# MosaicML's MPT-7B-Chat

## Description

This example shows how to use [Microsoft Phi-3.5](https://www.mosaicml.com/blog/mpt-7b), with a [SimpleAI](https://github.com/lhenault/simpleAI) server.

> Phi-3.5-mini is a lightweight, state-of-the-art open model built upon datasets used for Phi-3 - synthetic data and filtered publicly available websites - with a focus on very high-quality, reasoning dense data. The model belongs to the Phi-3 model family and supports 128K token context length. The model underwent a rigorous enhancement process, incorporating both supervised fine-tuning, proximal policy optimization, and direct preference optimization to ensure precise instruction adherence and robust safety measures.

Read more about the Phi-3 family [here](https://azure.microsoft.com/en-us/blog/new-models-added-to-the-phi-3-family-available-on-microsoft-azure/).

It implements `chat` methods for both streaming and non-streaming modes.

## Setup

First build the image with:

```bash
docker build . -t microsoft-phi-35:latest
```

Then declare your model in your *SimpleAI* configuration file `models.toml`:

```toml
[Phi-3dot5-mini-instruct]
    [Phi-3dot5-mini-instruct.metadata]
        owned_by    = 'Microsoft'
        permission  = []
        description = 'Phi-3.5-mini is a lightweight, state-of-the-art open model built upon datasets used for Phi-3 - synthetic data and filtered publicly available websites - with a focus on very high-quality, reasoning dense data. The model belongs to the Phi-3 model family and supports 128K token context length. The model underwent a rigorous enhancement process, incorporating both supervised fine-tuning, proximal policy optimization, and direct preference optimization to ensure precise instruction adherence and robust safety measures.'
    [Phi-3dot5-mini-instruct.network]
        type = 'gRPC'
        url = 'simple-ai-model-00:50051'
```

## Start service

Just start your container with:

```bash
docker run -it --rm -p 50051:50051 --gpus all microsoft-phi-35:latest
```

And start your *SimpleAI* instance, for instance with:

```bash
simple_ai serve [--host 127.0.0.1] [--port 8080]
```
