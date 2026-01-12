import os
import pyblish.api

from ayon_core.pipeline import OptionalPyblishPluginMixin
from ayon_core.pipeline.workfile import save_next_version
from ayon_core.host.interfaces import SaveWorkfileOptionalData
from ayon_mari.api import plugin


class IncrementCurrentFile(plugin.MariContextPlugin,
                           OptionalPyblishPluginMixin):
    """Increment the current file.

    Saves the current scene with an increased version number.
    """
    label = "Increment current file"
    order = pyblish.api.IntegratorOrder + 9.0
    families = ["*"]
    hosts = ["mari"]
    optional = True

    def process(self, context):
        if not self.is_active(context.data):
            return

        current_filepath: str = context.data["currentFile"]
        current_filename = os.path.basename(current_filepath)
        save_next_version(
            description=(
                f"Incremented by publishing from {current_filename}"
            ),
            # Optimize the save by reducing needed queries for context
            prepared_data=SaveWorkfileOptionalData(
                project_entity=context.data["projectEntity"],
                project_settings=context.data["project_settings"],
                anatomy=context.data["anatomy"],
            )
        )
