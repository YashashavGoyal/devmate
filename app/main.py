from typer import Typer, Option
from rich.console import Console
from app.utils.ui import PanelDisplay, TextStyles
from app.commands import init

console = Console()

app = Typer(
    name="devmate",
    help="Your friendly local development companion.",
    add_completion=True,
    no_args_is_help=True,
    rich_markup_mode="rich"
)

app.command(
    name="init",
    short_help="Checks if essential tools are installed.",
)(init.init)

@app.command(
    name="version",
    help="Show the current [bold cyan]version[/bold cyan] of devmate."
)
def version(
    help="Show the current [bold cyan]version[/bold cyan] of devmate."
):
    TextStyles().style_text("devmate 0.1.0", style="blue")


@app.command(
    name="about",
    help="The [bold]about[/bold] command displays information about devmate."
)
def about():
    PanelDisplay().print_panel(
        "About devmate",
        """
        devmate
        A versatile CLI tool built to enhance your local development experience,
        providing a suite of utilities to manage your projects more efficiently.
        """, 
        border_style="gray50", 
        subtitle="Version 0.1.0"
    )

if __name__ == "__main__": 
    app()