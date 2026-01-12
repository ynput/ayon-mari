"""Mari specific plugin definitions."""
from abc import abstractmethod

import pyblish.api

from ayon_core.pipeline import (
    load,
    publish
)


SETTINGS_CATEGORY = "mari"


class MariLoader(load.LoaderPlugin):
    """Base class for Mari load plugins."""

    hosts = ["mari"]
    settings_category = SETTINGS_CATEGORY


class MariNodeLoader(MariLoader):

    @property
    @abstractmethod
    def node_type(self) -> str:
        """Node type to create on load."""
        pass

    @property
    @abstractmethod
    def file_attr(self) -> str:
        """Node parameter to set the filepath at"""
        pass

    def load(self, context, name=None, namespace=None, options=None):

        # TODO: Implement
        raise NotImplementedError()

        # TODO: Create node/container
        # TODO: Set filepath
        # TODO: Imprint with custom data
        #  imprint_container(
        #      node,
        #      name=name,
        #      namespace=namespace or "",
        #      context=context,
        #      loader=self.__class__.__name__,
        #  )
        #  return node

    def update(self, container, context):
        node = container["_node"]
        path = self.filepath_from_context(context)
        node.getParameter(self.file_attr).setValue(path, 0.0)

        # Update representation id
        node.getParameter("AYON.representation").setValue(
            context["representation"]["id"], 0.0
        )

    def remove(self, container):
        node = container["_node"]
        node.delete()

    def switch(self, container, context):
        # Support switching to different contexts
        self.update(container, context)


class MariInstancePlugin(pyblish.api.InstancePlugin):
    """Base class for Mari instance publish plugins."""

    hosts = ["mari"]
    settings_category = SETTINGS_CATEGORY


class MariContextPlugin(pyblish.api.ContextPlugin):
    """Base class for Mari context publish plugins."""

    hosts = ["mari"]
    settings_category = SETTINGS_CATEGORY


class MariExtractorPlugin(publish.Extractor):
    """Base class for Mari extract plugins.

    Note:
        The `MariExtractorPlugin` is a subclass of `publish.Extractor`,
            which in turn is a subclass of `pyblish.api.InstancePlugin`.
        Should there be a requirement to create an extractor that operates
            as a context plugin, it would be beneficial to incorporate
            the functionalities present in `publish.Extractor`.
    """

    hosts = ["mari"]
    settings_category = SETTINGS_CATEGORY
