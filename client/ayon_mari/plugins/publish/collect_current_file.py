import pyblish.api
from ayon_core.pipeline import registered_host


class CollectMariCurrentFile(pyblish.api.ContextPlugin):
    """Inject the current working file into context"""

    order = pyblish.api.CollectorOrder - 0.5
    label = "Mari Current File"
    hosts = ["mari"]

    def process(self, context):
        """Inject the current working file"""
        host = registered_host()
        current_file = host.get_current_workfile()
        context.data['currentFile'] = current_file
        if not current_file:
            self.log.warning(
                "Current file is not saved. Save the file before continuing."
            )
