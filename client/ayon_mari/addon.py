import os
from ayon_core.addon import AYONAddon, IHostAddon, IPluginPaths

from .version import __version__

MARI_ADDON_ROOT = os.path.dirname(os.path.abspath(__file__))


class MariAddon(AYONAddon, IHostAddon, IPluginPaths):
    name = "mari"
    version = __version__
    host_name = "mari"

    def add_implementation_envs(self, env, app):
        # Set default values if are not already set via settings
        defaults = {"AYON_LOG_NO_COLORS": "1"}
        for key, value in defaults.items():
            if not env.get(key):
                env[key] = value

        # Add the startup to PYTHONPATH
        env["MARI_SCRIPT_PATH"] = os.pathsep.join([
            os.path.join(MARI_ADDON_ROOT, "deploy"),
            env.get("MARI_SCRIPT_PATH", "")
        ])

    def get_workfile_extensions(self):
        return [".mari"]

    def get_loader_action_plugin_paths(self, host_name):
        if host_name != self.host_name:
            return []

        return [
            os.path.join(MARI_ADDON_ROOT, "plugins", "load_actions"),
        ]