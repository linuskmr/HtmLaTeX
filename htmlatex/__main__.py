import argparse
from pathlib import Path

from htmlatex import htmlatex


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert HTML to LaTeX")
    parser.add_argument('html_file', type=Path, help="The HTML file to convert")
    return parser.parse_args()


def main():
    args = parse_args()
    html_file: Path = args.html_file
    latex_file = html_file.with_suffix('.tex')

    html_code = html_file.read_text()

    with open(latex_file, 'w+') as output_file:
        htmlatex(html_code, output_file)


if __name__ == "__main__":
    main()
