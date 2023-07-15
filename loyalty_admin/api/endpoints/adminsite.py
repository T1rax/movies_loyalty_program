import logging
from typing import Any

# from common.exceptions import PromoException
from common.models.promo import PromoType
from common.services.communication import ServiceCommunicator
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.amis.components import Form
from fastapi_amis_admin.crud.schema import BaseApiOut
from fastapi_amis_admin.models.fields import Field
from pydantic import BaseModel
from settings import settings
from starlette.requests import Request


logger = logging.getLogger(__name__)


# Create AdminSite instance
site = AdminSite(settings=Settings(database_url=settings.db.url))


@site.register_admin
class CreatePromoForm(admin.FormAdmin):
    """
    Форма для создания промокода
    """

    page_schema = "Создать промокод"
    form = Form(
        title="Форма для создания промокода", submitText="Создать промокод"
    )

    class schema(BaseModel):  # Тут обязательно название с маленькой буквы
        """
        Класс для указания полей формы
        """

        campaign_name: str = Field(
            ..., title="Название группы промокодов", max_length=50
        )
        products: list = Field(
            ...,
            title="ID продуктов, на которые работает промокод",
        )
        type: PromoType = Field(PromoType.DISCOUNT, title="Тип промокода")
        value: int = Field(..., title="Номинал")
        activation_date: str = Field(..., title="Дата активации")
        user_ids: list = Field(
            ...,
            title="Список пользователей",
        )
        activations_limit: int = Field(..., title="Количество активаций")

    # Запускается при отправке формы
    async def handle(
        self, request: Request, data: schema, **kwargs
    ) -> BaseApiOut[Any]:
        """
        Запускается при отправке формы
        """
        service_communicator = ServiceCommunicator()
        try:
            succeeded, msg = await service_communicator.create_promo(
                data.dict()
            )
            if succeeded:
                return BaseApiOut(msg=msg)
            else:
                return BaseApiOut(status=-1, msg=msg)
        except Exception as e:
            logger.exception(e, exc_info=True)
            return BaseApiOut(status=-1, msg="Неизвестная ошибка")


@site.register_admin
class SearchPromoCode(admin.FormAdmin):
    """
    Форма для поиска промокода
    """

    page_schema = "Поиск промокода"
    form = Form(
        title="Поиск промокода",
        submitText="Поиск",
    )

    class schema(BaseModel):
        """
        Класс для указания полей формы
        """

        type: str = Field(
            ..., title="Тип поиска"
        )  # TODO - Тут нужно сделать Enum с типами поиска
        products: list = Field(
            ..., title="На какие продукты работает промокод"
        )
        campaign_name: str = Field(..., title="Название кампании")
        active: bool = Field(..., title="Деактивирован ли промокод")

    async def handle(
        self, request: Request, data: schema, **kwargs
    ) -> BaseApiOut[Any]:
        """
        Запускается при отправке формы
        """
        # TODO - Нужен колбек обработки отправки формы
        return BaseApiOut(status=-1, msg=data.json())


@site.register_admin
class StatusPromoCode(admin.FormAdmin):
    """
    Форма для поиска промокода
    """

    page_schema = "Статус промокода"
    form = Form(
        title="Статус промокода",
        submitText="Поиск",
    )

    class schema(BaseModel):
        """
        Класс для указания полей формы
        """

        promo_code: str = Field(..., title="Промокод")
        user_id: str = Field(..., title="User ID пользователя")

    async def handle(
        self, request: Request, data: schema, **kwargs
    ) -> BaseApiOut[Any]:
        """
        Запускается при отправке формы
        """
        # TODO - Нужен колбек обработки отправки формы
        return BaseApiOut(status=-1, msg=data.json())


@site.register_admin
class DeactivatePromoCode(admin.FormAdmin):
    """
    Форма для деактивации промокода
    """

    page_schema = "Деактивация промокода"
    form = Form(
        title="Деактивация промокода",
        submitText="Деактивировать",
    )

    class schema(BaseModel):
        """
        Класс для указания полей формы
        """

        promo_code: str = Field(..., title="Промокод")
        user_id: str = Field(..., title="User ID пользователя")

    async def handle(
        self, request: Request, data: schema, **kwargs
    ) -> BaseApiOut[Any]:
        """
        Запускается при отправке формы
        """
        # TODO - Нужен колбек обработки отправки формы
        return BaseApiOut(status=-1, msg=data.json())


@site.register_admin
class CreateLoyaltyCard(admin.FormAdmin):
    """
    Форма для создания регистрации в программе лояльности
    """

    page_schema = "Создание карты лояльности"
    form = Form(
        title="Создание карты лояльности",
        submitText="Создать",
    )

    class schema(BaseModel):
        """
        Класс для указания полей формы
        """

        user_id: str = Field(..., title="User ID пользователя")

    async def handle(
        self, request: Request, data: schema, **kwargs
    ) -> BaseApiOut[Any]:
        """
        Запускается при отправке формы
        """
        # TODO - Нужен колбек обработки отправки формы
        return BaseApiOut(status=-1, msg=data.json())


@site.register_admin
class ChangeLoyaltyLevel(admin.FormAdmin):
    """
    Форма для изменения уровня в программе лояльности
    """

    page_schema = "Изменения уровня Лояльности"
    form = Form(
        title="Изменения уровня Лояльности",
        submitText="Изменить",
    )

    class schema(BaseModel):
        """
        Класс для указания полей формы
        """

        user_id: str = Field(..., title="User ID пользователя")
        level: int = Field(
            ..., title="Новый уровень лояльности"
        )  # TODO - Тут нужен ENUM с уровнями лояльности

    async def handle(
        self, request: Request, data: schema, **kwargs
    ) -> BaseApiOut[Any]:
        """
        Запускается при отправке формы
        """
        # TODO - Нужен колбек обработки отправки формы
        return BaseApiOut(status=-1, msg=data.json())


@site.register_admin
class PointsLoyaltyCard(admin.FormAdmin):
    """
    Форма для изменения баланса счета пользователя в программе лояльности
    """

    page_schema = "Пополнить/списать баллы"
    form = Form(
        title="Пополнить/списать баллы",
        submitText="Отправить",
    )

    class schema(BaseModel):
        """
        Класс для указания полей формы
        """

        action_type: str = Field(
            ..., title="User ID пользователя"
        )  # TODO - Тут нужен ENUM с пополнением/списанием
        user_id: str = Field(..., title="User ID пользователя")
        value: int = Field(..., title="User ID пользователя")

    async def handle(
        self, request: Request, data: schema, **kwargs
    ) -> BaseApiOut[Any]:
        """
        Запускается при отправке формы
        """
        # TODO - Нужен колбек обработки отправки формы
        return BaseApiOut(status=-1, msg=data.json())


@site.register_admin
class InfoLoyaltyCard(admin.FormAdmin):
    """
    Получение информации по программе лояльности
    """

    page_schema = "Статус программы лояльности"
    form = Form(
        title="Статус программы лояльности",
        submitText="Отправить",
    )

    class schema(BaseModel):
        """
        Класс для указания полей формы
        """

        user_id: str = Field(..., title="User ID пользователя")

    async def handle(
        self, request: Request, data: schema, **kwargs
    ) -> BaseApiOut[Any]:
        """
        Запускается при отправке формы
        """
        # TODO - Нужен колбек обработки отправки формы
        return BaseApiOut(status=-1, msg=data.json())
