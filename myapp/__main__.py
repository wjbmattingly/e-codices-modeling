import pathlib

import typer
from bokeh.server.server import Server
from bokeh.util.browser import view
from tornado.ioloop import IOLoop

from bulk.text import bulk_text
from bulk.image import bulk_images

import os
import tornado.web


print(os.path.dirname(__file__))

extra_patterns = [("./bulk/", tornado.web.StaticFileHandler,
                   {"path": os.path.dirname(__file__)})]

print(extra_patterns)
app = typer.Typer(
    name="bulk",
    add_completion=False,
    help="Tools for bulk labelling.",
    no_args_is_help=True,
)


@app.command("version")
def version():
    print("0.1.0")


@app.command("text")
def text(path: pathlib.Path = typer.Argument(..., help="Path to .csv file", exists=True),
         keywords: str = typer.Option(None, help="Keywords to highlight")):
    """Bulk Labelling for Text"""
    if keywords:
        keywords = keywords.split(",")
    server = Server({"/": bulk_text(path, keywords=keywords)}, io_loop=IOLoop())
    server.start()
    host = "http://localhost:5006/"
    print(f"About to serve `bulk` over at {host}.")
    server.io_loop.add_callback(view, host)
    server.io_loop.start()

@app.command("images")
def text(path: pathlib.Path = typer.Argument(..., help="Path to .csv file", exists=True),
         keywords: str = typer.Option(None, help="Keywords to highlight")):
    """Bulk Labelling for Text"""
    if keywords:
        keywords = keywords.split(",")
    print(os.path.dirname(__file__))
    server = Server({"/": bulk_images(path, keywords=keywords)}, io_loop=IOLoop(), prefix="/")
    server.start()
    host = "http://localhost:5006/"
    print(f"About to serve `bulk` over at {host}.")
    server.io_loop.add_callback(view, host)
    server.io_loop.start()


if __name__ == '__main__':
    app()
