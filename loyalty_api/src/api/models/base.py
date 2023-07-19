import orjson
from fastapi_pagination import Page
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ORDJSONModelMixin(BaseModel):
    class Config:
        allow_population_by_field_name = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


Page = Page.with_custom_options(
    size=Field(20, ge=1, le=100),
)
