__version__ = '0.1.0'

from typing import TextIO

from bs4 import BeautifulSoup

from .handlers import Handlers, default_handlers
from .node_handler import NodeHandler
from .tree_walker import TreeWalker


def htmlatex(html: str, output: TextIO, handlers: Handlers = default_handlers):
    """Convert HTML to LaTeX.

    :param html: HTML string
    :param output: output stream
    :param handlers: handlers
    :return: LaTeX string
    """

    soup = BeautifulSoup(html, "html.parser")
    html_node = soup.html
    if html_node is None:
        raise ValueError("No <html> tag found")
    TreeWalker(output=output, handlers=handlers).walk(html_node)
