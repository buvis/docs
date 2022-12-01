import click

from commands import CommandDiscover, CommandScrape


@click.group(help="CLI tool to manage kubernetes apps catalog")
def cli():
    pass


@cli.command("discover")
def discover():
    cmd = CommandDiscover()
    cmd.execute()


@cli.command("scrape")
def scrape():
    cmd = CommandScrape()
    cmd.execute()


if __name__ == "__main__":
    cli()
