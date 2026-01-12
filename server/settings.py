from ayon_server.settings import BaseSettingsModel, SettingsField

from .imageio import MariImageIOModel

DEFAULT_VALUES = {
    "imageio": {
        "activate_host_color_management": True,
        "file_rules": {
            "enabled": False,
            "rules": []
        }
    },
}


class MariSettings(BaseSettingsModel):
    imageio: MariImageIOModel = SettingsField(
        default_factory=MariImageIOModel,
        title="Color Management (ImageIO)"
    )
