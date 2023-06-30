from functools import wraps
from typing import Generic, List, TypeVar, Union

from pydantic.generics import GenericModel


DataT = TypeVar("DataT")


class ApiResponse(GenericModel, Generic[DataT]):
    success: bool
    result: DataT | None
    errors: List[Union[str, dict]] | None


def wrap_response(view):
    @wraps(view)
    async def wrapper(*args, **kwargs):
        return ApiResponse(
            success=True, result=await view(*args, **kwargs), errors=None
        )

    return wrapper
