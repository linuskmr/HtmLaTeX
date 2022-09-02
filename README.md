# HtmLaTeX

*Work in Progress*

Like HTML, but not LaTeX? HtmLaTeX compiles HTML code to LaTeX.

For example, the following HTML code:

```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>My Paper</title>
    <meta name="date" content="2022-09-02">
    <meta name="author" content="Linus">
    <link rel="icon" type="image/png" href="logo.png">
</head>
<body>
<div>
    <a href="#">link</a>
</div>
<h1 id="section-1">Hello World</h1>
<p>This is a paragraph.</p>

<img src="a">

</body>
</html>
```

...compiles to the following LaTeX code:

```latex
%%%%%% HEAD START %%%%%%

	\title{My Paper}

	\date{2022-09-02}

	\author{Linus}

%%%%%% HEAD END %%%%%%

%%%%%% MAIN DOCUMENT START %%%%%%
\begin{document}
\maketitle

	\section{Hello World}
	\label{section-1}

	This is a paragraph.

	\includegraphics{a}

\end{document}
%%%%%% MAIN DOCUMENT END %%%%%%
```

## Installation

```bash
$ pip install HtmLaTeX
```

## Usage

### As binary

```bash
$ python3 -m htmlatex paper.html
```

This will create a file called `paper.tex` in the current directory.

### As library

```python
import io
import bs4
from htmlatex import Handlers, htmlatex

# Declare handlers for HTML tags

# Collection of handlers for HTML tags
handlers = Handlers()


# Register a handler for the <h1> tag
@handlers.register()
def h1(node: bs4.element.Tag):
    section_name = node.string
    section_id = node.attrs['id']
    yield [
        r"\section{%s}" % section_name,
        r"\label{%s}" % section_id,
    ]


# ... more handlers ...

# Destination for generated LaTeX
generated_latex = io.StringIO()
# HTML to be converted
html = "..."
# And compile
htmlatex(html, generated_latex, handlers=handlers)
```
