import click

from commands import CommandUpdate


@click.group(help="CLI tool to manage kubernetes apps catalog")
def cli():
    pass


@cli.command("update")
@click.option("-r",
              "--refresh",
              default=False,
              is_flag=True,
              help="Refresh list of apps")
def check(refresh):
    cmd = CommandUpdate()
    cmd.execute(refresh)


if __name__ == "__main__":
    cli()
