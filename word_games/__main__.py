"""Console script for word_games."""

import click

from .bot.printer_bot import application


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")

@cli.command()
def bot():
    click.echo("Uruchamianie interfejsu Orlowskiego")
    application.run_polling()
    click.echo("Zamknięto interfejs Orlowskiego")

if __name__ == "__main__":
    cli()  # pragma: no cover
