from typer import Typer
from rich.console import Console

console = Console()

app = Typer(
    name="devmate",
    help="Your friendly local development companion.",
    add_completion=True,
    no_args_is_help=True
)

@app.command(
    name="version",
    help="Version of devmate"
)
def version():
    console.print("devmate 0.1.0")


@app.command(
    name="about",
    help="About devmate"
)
def about():
    console.print(
        """
        devmate 0.1.0
        A versatile CLI tool built to enhance your local development experience,
        providing a suite of utilities to manage your projects more efficiently.
        """
    )


if __name__ == "__main__": 
    app()