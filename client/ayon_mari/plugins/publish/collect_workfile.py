import os
import pyblish.api


class CollectWorkfileData(pyblish.api.InstancePlugin):
    """Inject data into Workfile instance"""

    order = pyblish.api.CollectorOrder - 0.01
    label = "Mari Workfile"
    families = ["workfile"]

    def process(self, instance):
        """Inject the current working file"""
        context = instance.context
        current_file = context.data["currentFile"]
        if not current_file:
            self.log.warning(
                "Current file is not saved. Save the file before continuing."
            )
            return

        folder, file = os.path.split(current_file)
        filename, ext = os.path.splitext(file)

        instance.data.setdefault("representations", []).append({
            'name': ext.lstrip("."),
            'ext': ext.lstrip("."),
            'files': file,
            "stagingDir": folder,
        })

        self.log.debug(f"Workfile: {current_file}")