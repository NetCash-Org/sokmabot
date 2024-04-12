from loader import dp
from .admins import AdminFilter
from .isGroup import IsGroup
from .isPrivate import IsPrivate


if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
