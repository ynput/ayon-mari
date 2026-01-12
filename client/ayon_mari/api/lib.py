"""Library functions for The Foundry Mari."""
from typing import Dict, List, Union, Any

import mari
from qtpy import QtWidgets

JSON_PREFIX: str = "JSON::"
IS_HEADLESS: bool = mari.app.inTerminalMode()


def get_main_window():
    """Get Qt main window of Mari."""
    return next((
        widget for widget in QtWidgets.QApplication.topLevelWidgets()
        if isinstance(widget, QtWidgets.QMainWindow)
        and widget.objectName() == "MainWindow"
    ), None)


def imprint(node, data) -> None:
    raise NotImplementedError()


def read(node, group=None, time=0.0) -> dict[str, Any]:
    raise NotImplementedError()


def lsattr(attr: str,
           value: Union[str, int, bool, List, Dict, None] = None) -> List:
    """Return nodes matching `attr` and `value`

    Arguments:
        attr: Name of Blender property
        value: Value of attribute. If none
            is provided, return all nodes with this attribute.

    Example:
        >>> lsattr("id", "myId")
        ...   [bpy.data.objects["myNode"]
        >>> lsattr("id")
        ...   [bpy.data.objects["myNode"], bpy.data.objects["myOtherNode"]]

    Returns:
        list
    """
    return lsattrs({attr: value})


def lsattrs(attrs: Dict) -> List:
    """Return nodes with the given attribute(s).

    Arguments:
        attrs: Name and value pairs of expected matches

    Example:
        >>> lsattrs({"age": 5})  # Return nodes with an `age` of 5
        # Return nodes with both `age` and `color` of 5 and blue
        >>> lsattrs({"age": 5, "color": "blue"})

    Returns a list.

    """
    raise NotImplementedError()
