import io

from htmlatex import __version__, htmlatex


def test_version():
    assert __version__ == '0.1.0'


def test_htmlatex():
    html = r"""
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
    """

    latex = r"""
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

    """

    generated_latex = io.StringIO()
    htmlatex(html, generated_latex)
    # Since the multi-line strings declared above have extra linebreaks,
    # we only compare whether the expected latex contains the generated_latex.
    assert generated_latex.getvalue() in latex
