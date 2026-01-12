from typing import Type

from ayon_server.addons import BaseServerAddon

from .settings import MariSettings, DEFAULT_VALUES


class MariAddon(BaseServerAddon):
    settings_model: Type[MariSettings] = MariSettings

    async def get_default_settings(self):
        settings_model_cls = self.get_settings_model()
        return settings_model_cls(**DEFAULT_VALUES)
