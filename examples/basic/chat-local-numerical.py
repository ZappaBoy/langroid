"""
Test multi-round interaction with a local LLM, playing a simple "doubling game".

In each round:

- User gives a number
- LLM responds with the double of that number


python3 examples/basic/chat-local-numerical.py

Recommended local model setup:
- spin up an LLM with oobabooga at an endpoint like http://127.0.0.1:5000/v1
- run this script with -m local/127.0.0.1:5000/v1

See this [script](https://github.com/langroid/langroid-examples/blob/main/examples/docqa/rag-local-simple.py)
for other ways to specify the local_model.

"""
import os
import fire

import langroid as lr
from langroid.utils.configuration import settings
import langroid.language_models as lm

# for best results:
DEFAULT_LLM = "litellm/ollama/mixtral:8x7b-instruct-v0.1-q4_K_M"

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# (1) Define the desired fn-call as a ToolMessage via Pydantic.


def app(
    m: str = DEFAULT_LLM,  # model name
    d: bool = False,  # debug
    nc: bool = False,  # no cache
):
    settings.debug = d
    settings.cache = not nc
    # create LLM config
    llm_cfg = lm.OpenAIGPTConfig(
        chat_model=m or DEFAULT_LLM,
        chat_context_length=4096,  # set this based on model
        max_output_tokens=100,
        temperature=0.2,
        stream=True,
        timeout=45,
    )

    agent = lr.ChatAgent(
        lr.ChatAgentConfig(
            llm=llm_cfg,
            system_message="""
            You are a number-doubling expert. When user gives you a NUMBER,
            simply respond with its DOUBLE and SAY NOTHING ELSE.
            DO NOT EXPLAIN YOUR ANSWER OR YOUR THOUGHT PROCESS.
            """,
        )
    )

    task = lr.Task(agent)
    task.run("15")  # initial number


if __name__ == "__main__":
    fire.Fire(app)