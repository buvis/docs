import click

from commands import CommandDiscover, CommandUpdate


@click.group(help="CLI tool to manage kubernetes apps catalog")
def cli():
    pass


@cli.command("discover")
def discover():
    cmd = CommandDiscover()
    cmd.execute()


@cli.command("update")
def update():
    cmd = CommandUpdate()
    cmd.execute()


if __name__ == "__main__":
    cli()
