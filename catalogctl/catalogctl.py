import click

from adapters import console
from commands import CommandUpdate


@click.group(help="CLI tool to manage kubernetes apps catalog")
def cli():
    pass


@cli.command("update")
def check():
    cmd = CommandUpdate()
    cmd.execute()

if __name__ == "__main__":
    cli()
