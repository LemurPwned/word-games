"""Console script for word_games."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("word-games")
    click.echo("=" * len("word-games"))
    click.echo("Various word games to play in the terminal")


if __name__ == "__main__":
    main()  # pragma: no cover
