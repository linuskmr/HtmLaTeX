from typing import Optional, Iterator, TextIO

import bs4

from htmlatex.handlers import Handlers


class NodeHandler:
    """
    Handles a specific node in the HTML tree.
    Based on the handler function, it writes the corresponding LaTeX code before entering and after leaving the
    node.
    """

    def __init__(self, *, node: bs4.element.Tag, depth: int, output: TextIO, handlers: Handlers):
        self.node = node
        self.depth = depth
        self.output = output
        self.handler = self._get_handler(handlers)

    def _get_handler(self, handlers: Handlers) -> Optional[Iterator[str]]:
        # Get the handler for the current node
        try:
            generator_function = handlers.handlers[self.node.name]
        except KeyError as err:
            # No handler for this tag, so simply ignore it
            # Probably some of its children has a handler
            return None

        # Calling a generator function returns a generator object.
        # This, in turn, can be called with next() to get values.
        generator = generator_function(self.node)
        return generator

    def _exec_handler(self):
        """
        Executes the handler by driving the generator one step forward.
        Indents the yielded text by the current depth and prints it to self.output.
        """

        if self.handler is None:
            return

        try:
            text = next(self.handler)
        except KeyError as missing_key:
            raise ValueError(f"Handler for {self.node.name} needs argument {missing_key}")
        except StopIteration:
            # The handler only yields once (could also yield never),
            # so it does not produce anything after its children were handled.
            # This is totally fine. Not every handler needs to do something afterwards
            return

        if isinstance(text, list):
            text = "\n".join(text)

        # Indent *all* lines produced by the handler by the current depth
        indent = '\t' * self.depth
        # Indent the first line
        text = indent + text
        # Indent all following lines
        text = text.replace('\n', '\n' + indent)
        self.output.write(text + '\n\n')

    def __enter__(self):
        # Preamble: Drive the handler to the first yield statement
        self._exec_handler()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # "Postamble": Drive the handler to the second yield statement
        self._exec_handler()
