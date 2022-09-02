from typing import TextIO

import bs4

from htmlatex.handlers import Handlers
from htmlatex.node_handler import NodeHandler


class TreeWalker:
    """Walks the tree of HTML nodes and calls the handlers for each node."""

    def __init__(self, *, output: TextIO, handlers: Handlers):
        """
        :param output: The file to which the output is written
        :param handlers: The handlers for the HTML tags.
        """

        self.output_file = output
        self.handlers = handlers

    def _node_handler(self, node: bs4.element.Tag, depth: int = -1) -> NodeHandler:
        """Helper function helping by creating NodeHandlers. Automatically fills in the output_file and handlers."""

        return NodeHandler(node=node, depth=depth, output=self.output_file, handlers=self.handlers)

    def walk(self, node: bs4.element.Tag, depth: int = -1):
        """Walks the tree of HTML nodes and calls the handlers for each node."""

        # The NodeHandler is a context manager which calls the first part of the handler (preamble) when starting
        # entering the context and the second part (postamble) when exiting the context.
        # For example, a NodeHandler prints \section{...} when entering the context and \end{section} when exiting.
        with self._node_handler(node, depth) as node_handler:
            # Recursively traverse the children of this node
            for child in node.contents:
                if not isinstance(child, bs4.element.Tag):
                    # Normal text is not a tag, so we don't walk it
                    continue
                self.walk(child, depth + 1)
