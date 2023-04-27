from pydantic import BaseModel, Field
#from examples.base_config import ExampleBaseConfig
from llmagent.agent.config import AgentConfig
from llmagent.embedding_models.config import EmbeddingModelsConfig
from llmagent.vector_store.config import VectorStoreConfig
from llmagent.language_models.config import LLMConfig
from llmagent.parsing.config import ParsingConfig
from llmagent.prompts.config import PromptsConfig

from typing import List

class URLQAConfig(AgentConfig):
    embeddings: EmbeddingModelsConfig = Field(
        default_factory=lambda:
        EmbeddingModelsConfig(
            model_type="openai",
        ))
    vecdb: VectorStoreConfig = Field(
        default_factory=lambda:
        VectorStoreConfig(
            type="qdrant",
            compose_file="llmagent/vector_store/docker-compose-qdrant.yml",
        ))
    llm: LLMConfig = Field(
        default_factory=lambda:
        LLMConfig(
            type="openai",
        ))

    parsing: ParsingConfig = Field(
        default_factory=lambda:
        ParsingConfig(
            chunk_size=500,
            chunk_overlap=50,
        ))

    prompts: PromptsConfig = Field(
        default_factory=lambda:
        PromptsConfig(
            max_tokens=1000,
        ))

    urls: List[str] = Field(default_factory=lambda: [
        "https://news.ycombinator.com/item?id=35629033",
        "https://www.newyorker.com/tech/annals-of-technology/chatgpt-is-a-blurry-jpeg-of-the-web",
        "https://www.wired.com/1995/04/maes/",
        "https://cthiriet.com/articles/scaling-laws",
        "https://www.jasonwei.net/blog/emergence",
        "https://www.quantamagazine.org/the-unpredictable-abilities-emerging-from-large-ai-models-20230316/",
        "https://ai.googleblog.com/2022/11/characterizing-emergent-phenomena-in.html",
    ])


