from typing import Dict, Callable

import bs4


class Handlers:
    """
    Stores the handlers for each HTML tag.

    A handler is thereby a function that takes a BeautifulSoup Tag object and yields LaTeX code.
    You may yield two strings or list of lines, the first one being the LaTeX code *before* processing the children,
    and the second one being the code *after* processing the children. You are allowed to omit the second yield,
    if you don't need it.
    """

    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        """A dictionary mapping tag names to functions that handle them."""

    def register(self):
        """This decorator registers its decorated function as a handler for HTML tags named exactly like the
        function."""

        def decorator(func: Callable):
            handler_for_tag = func.__name__
            self.handlers[handler_for_tag] = func
            return func

        return decorator


default_handlers = Handlers()


@default_handlers.register()
def head(node: bs4.element.Tag):
    yield "%%%%%% HEAD START %%%%%%"
    yield "%%%%%% HEAD END %%%%%%"


@default_handlers.register()
def body(node: bs4.element.Tag):
    yield [
        "%%%%%% MAIN DOCUMENT START %%%%%%",
        r"\begin{document}",
        r"\maketitle",
    ]
    yield [
        r"\end{document}",
        "%%%%%% MAIN DOCUMENT END %%%%%%"
    ]


@default_handlers.register()
def title(node: bs4.element.Tag):
    yield f"\\title{{{node.text}}}"


@default_handlers.register()
def meta(node: bs4.element.Tag):
    name = node.attrs['name'] if 'name' in node.attrs else None
    if name == 'author':
        yield r"\author{%s}" % node.attrs['content']
    elif name == 'date':
        yield r"\date{%s}" % node.attrs['content']
    elif name == "link":
        if node.attrs['rel'] == 'icon':
            yield r"\logo{\includegraphics{%s}}" % node.attrs['href']


@default_handlers.register()
def h1(node: bs4.element.Tag):
    section_name = node.string
    section_id = node.attrs['id']
    yield [
        r"\section{%s}" % section_name,
        r"\label{%s}" % section_id,
    ]


@default_handlers.register()
def p(node: bs4.element.Tag):
    yield f"{node.string}"


@default_handlers.register()
def img(node: bs4.element.Tag):
    yield f"\\includegraphics{{{node.attrs['src']}}}"
