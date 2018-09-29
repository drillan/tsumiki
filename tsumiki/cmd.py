import pathlib

import click
from tsumiki import Tsumiki


def make_output_path(input_path, ext=".html"):
    p = pathlib.Path(input_path)
    filename = pathlib.PurePath(input_path).stem + ext
    return p.resolve().parent / filename


def convert_to_html(input_path):
    with open(input_path, "r", encoding="utf8") as f:
        source = f.read()
        return Tsumiki(source).html


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path(exists=True))
def tsumiki(input_path, output_path=None):
    click.echo(input_path)
    filename = click.format_filename(input_path, shorten=True)
    click.echo(filename)
    html = convert_to_html(input_path)

    if output_path:
        p = pathlib.Path(output_path)
    else:
        p = make_output_path(input_path)
    
    with p.open("w", encoding="utf8") as f:
        f.write(html)
