class PromoException(Exception):
    """
    Не указаны все параметры для отправки
    """


class RequestException(Exception):
    """
    Ошибка при отправке HTTP запроса
    """
