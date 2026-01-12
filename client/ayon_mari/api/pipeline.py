import os
import json
import logging
from typing import Any, Generator

import pyblish.api

from ayon_core.host import HostBase, IWorkfileHost, ILoadHost, IPublishHost
from ayon_core.lib import (
    register_event_callback,
    emit_event
)
from ayon_core.pipeline.load import any_outdated_containers
from ayon_core.resources import get_ayon_icon_filepath
from ayon_core.settings import get_project_settings
from ayon_core.pipeline import (
    register_loader_plugin_path,
    register_creator_plugin_path,
    get_current_context,
    get_current_project_name,
    AYON_CONTAINER_ID,
)
from ayon_core.pipeline.workfile import save_next_version
from ayon_core.tools.utils import host_tools

import ayon_mari
from .lib import lsattr

import mari
from qtpy import QtCore, QtGui

from . import lib

log = logging.getLogger("ayon_mari")

HOST_DIR = os.path.dirname(os.path.abspath(ayon_mari.__file__))
PLUGINS_DIR = os.path.join(HOST_DIR, "plugins")
PUBLISH_PATH = os.path.join(PLUGINS_DIR, "publish")
LOAD_PATH = os.path.join(PLUGINS_DIR, "load")
CREATE_PATH = os.path.join(PLUGINS_DIR, "create")

AYON_CONTEXT_DATA_KEY = "AYON_context"


def get_current_context_label() -> str:
    # Return folder path, task name
    context = get_current_context()
    folder_path = context["folder_path"]
    task_name = context["task_name"]
    return f"{folder_path}, {task_name}"


def install_menu(project_settings: dict):

    main_window = lib.get_main_window()
    menubar = main_window.menuBar()

    menu = menubar.addMenu("AYON")

    # Current context
    context_action = menu.addAction(
        QtGui.QIcon(get_ayon_icon_filepath()),
        "<context>"
    )
    context_action.setEnabled(False)

    def _update_context_label():
        context_action.setText(get_current_context_label())
    menu.aboutToShow.connect(_update_context_label)

    # Version Up workfile (if enabled)
    try:
        if project_settings["core"]["tools"]["ayon_menu"].get(
                "version_up_current_workfile"):
            menu.addSeparator()
            menu.addAction(
                "Version Up Workfile",
                lambda args: save_next_version()
            )
    except KeyError:
        print("Version Up Workfile setting not found in "
              "Core Settings. Please update Core Addon")

    # Workfiles
    menu.addAction(
        "Workfiles",
        lambda: host_tools.show_workfiles(parent=main_window)
    )

    # Tools
    menu.addSeparator()
    menu.addAction(
        "Create...",
        lambda: host_tools.show_publisher(
            parent=main_window,
            tab="create"
        )
    )
    menu.addAction(
        "Publish...",
        lambda: host_tools.show_publisher(
            parent=main_window,
            tab="publish"
        )
    )
    menu.addAction(
        "Load...",
        lambda: host_tools.show_loader(
            parent=main_window,
            use_context=True
        )
    )
    menu.addAction(
        "Manage...",
        lambda: host_tools.show_scene_inventory(parent=main_window)
    )

    menu.addSeparator()
    menu.addAction(
        "Experimental Tools...",
        lambda: host_tools.show_experimental_tools_dialog(parent=main_window)
    )

    # TODO: Add set workfile attributes actions
    # menu.addSeparator()
    # workfile_menu = menu.addMenu("Set workfile attributes")
    # workfile_menu.addAction("Set Frame Range", lib.reset_frame_range)
    # workfile_menu.addAction("Set Colorspace")


class MariHost(HostBase, IWorkfileHost, ILoadHost, IPublishHost):
    name = "mari"

    def install(self):
        pyblish.api.register_plugin_path(PUBLISH_PATH)
        pyblish.api.register_host("mari")

        register_loader_plugin_path(LOAD_PATH)
        register_creator_plugin_path(CREATE_PATH)

        project_name = get_current_project_name()
        project_settings = get_project_settings(project_name)

        # Install the menu after interface is initialized
        install_menu(project_settings)

        # Register event callbacks
        register_event_callback("open", on_open)
        register_event_callback("new", on_new)

        # Trigger load, save, new callbacks from Mari callbacks
        self._register_callbacks()

    def open_workfile(self, filepath):
        # TODO: Mari doesn't have regular workfiles, it has projects that tend
        #  to live on a local drive (for performance) and those projects are
        #  folders, not files. We can export/import "Sessions", but those also
        #  are folders.
        return mari.projects.open(filepath)

    def save_workfile(self, filepath=None):
        # TODO: Mari doesn't have regular workfiles, it has projects that tend
        #  to live on a local drive (for performance) and those projects are
        #  folders, not files. We can export/import "Sessions", but those also
        #  are folders.
        project = mari.projects.current()
        if not project:
            raise RuntimeError("No active project to save.")
        project.saveAs(filepath)

    def get_current_workfile(self) -> str:
        # TODO: Mari doesn't have regular workfiles, it has projects that tend
        #  to live on a local drive (for performance) and those projects are
        #  folders, not files. We can export/import "Sessions", but those also
        #  are folders.
        project = mari.projects.current()
        if project:
            return project.name()
        return ""

    def workfile_has_unsaved_changes(self) -> bool:
        project = mari.projects.current()
        if project:
            return project.isModified()
        return False

    def get_workfile_extensions(self):
        # TODO: Mari doesn't have regular workfiles, it has projects that tend
        #  to live on a local drive (for performance) and those projects are
        #  folders, not files. We can export/import "Sessions", but those also
        #  are folders.
        return [".mri"]

    def get_containers(self):
        return iter_containers()

    def update_context_data(self, data, changes):

        project = mari.projects.current()
        if project:
            data = json.dumps(data)
            project.setMetadata(AYON_CONTEXT_DATA_KEY, data)

        # lib.imprint(root, data)
        pass

    def get_context_data(self):
        project = mari.projects.current()
        if project:
            if not project.hasMetadata(AYON_CONTEXT_DATA_KEY):
                return {}

            value = project.metadata(AYON_CONTEXT_DATA_KEY)
            if not value:
                return {}
            try:
                return json.loads(value)
            except json.decoder.JSONDecodeError:
                return {}
        return {}

    def _register_callbacks(self):
        # TODO: Implement Mari scene callbacks to emit AYON events
        pass


def iter_containers() -> Generator[dict[str, Any], None, None]:
    """Yield all objects in the active document that have 'id' attribute set
    matching an AYON container ID"""
    # TODO: Implement
    raise NotImplementedError()


def imprint_container(
    container,
    name,
    namespace,
    context,
    loader
):
    """Imprints an object with container metadata and hides it from the user
    by adding it into a hidden layer.
    Arguments:
        container (Node): The object to imprint.
        name (str): Name of resulting assembly
        namespace (str): Namespace under which to host container
        context (dict): Asset information
        loader (str): Name of loader used to produce this container.
    """
    # TODO: Implement
    data = {
        "schema": "ayon:container-3.0",
        "id": AYON_CONTAINER_ID,
        "name": name,
        "namespace": namespace,
        "loader": str(loader),
        "representation": context["representation"]["id"],
        "project_name": context["project"]["name"],
    }

    lib.imprint(
        container,
        data
    )


def on_new():
    # TODO: Implement
    pass
    # lib.set_context_settings()


def on_open():
    from ayon_core.tools.utils import SimplePopup

    # Check for outdated containers in scene
    if any_outdated_containers():
        log.warning("Scene has outdated content.")

        # Find mari main window
        parent = lib.get_main_window()
        if parent is None:
            log.info("Skipping outdated content pop-up "
                     "because Mari window can't be found.")
        else:

            # Show outdated pop-up
            def _on_show_inventory():
                host_tools.show_scene_inventory(parent=parent)

            dialog = SimplePopup(parent=parent)
            dialog.setWindowTitle("Mari project has outdated content")
            dialog.set_message("There are outdated containers in "
                              "your Mari project.")
            dialog.on_clicked.connect(_on_show_inventory)
            dialog.show()