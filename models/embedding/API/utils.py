from pydantic import BaseModel  # noqa: D100


class EmbeddingRequest(BaseModel):  # noqa: D101
	texts: list[str]
