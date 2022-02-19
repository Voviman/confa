from aiogram.contrib.middlewares.i18n import I18nMiddleware
from config import I18N_DOMAIN, LOCALES_DIR
from aiogram import types
from typing import Tuple, Any


async def get_lang(user_id):
    pass


class ACLMidlleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user = types.User.get_current()
        return get_lang(user.id) or user.locale


def setup_midlleware(dp):
    i18n = ACLMidlleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n