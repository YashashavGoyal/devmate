from typer import Typer
from rich.console import Console

from app.utils import PanelDisplay, TextDisplay
from app.commands import init, health, clone, up, deploy, logs, shell, down

console = Console()

app = Typer(
    name="devmate",
    help="Your friendly local development companion.",
    add_completion=True,
    no_args_is_help=True,
    rich_markup_mode="rich"
)
# devmate init
app.command(
    name="init",
    short_help="Checks if essential tools are installed.",
)(init)

# devmate health
app.command(
    name="health",
    short_help="Checks if the local application is running and responding.",
)(health)

# devmate clone
app.command(
    name="clone",
    short_help="Clones the git repository in your local system"
)(clone)

# devmate up
app.command(
    name="up",
    short_help="Start the application services. (Alias: run)",
)(up)

# devmate deploy
app.command(
    name="deploy",
    short_help="Clones a repo and starts it. (Alias: dep)",
)(deploy)

# devmate logs
app.command(
    name="logs",
    short_help="Shows the logs of the application. (Alias: log)",
)(logs)

# devmate down
app.command(
    name="down",
    short_help="Stops the application services. (Alias: stop)",
)(down)

# devmate shell
app.command(
    name="shell",
    short_help="Opens a shell in the application container. (Alias: sh)",
)(shell)

# ...... Alias ......
app.command(
    name="dep", 
    hidden=True,
    help="Alias for deploy"
)(deploy)

app.command(
    name="run", 
    hidden=True,
    help="Alias for up"
)(up)  

app.command(
    name="log",
    hidden=True,
    help="Alias for logs"
)(logs)

app.command(
    name="sh",
    hidden=True,
    help="Alias for shell"
)(shell)

app.command(
    name="stop",
    hidden=True,
    help="Alias for down"
)(down) 

# devmate version
@app.command(
    name="version",
    help="Show the current [bold cyan]version[/bold cyan] of devmate."
)
def version():
    TextDisplay.style_text("devmate: 0.7.0", style="blue")


# devmate about
@app.command(
    name="about",
    help="The [bold]about[/bold] command displays information about devmate."
)
def about():
    PanelDisplay.print_panel(
        "About devmate",
        """
        devmate
        A powerful developer companion designed to streamline your local workflow,
        automating container management and orchestrating dev environments with ease.

        Features:
        • Works with Docker Compose and Dockerfile
        • Free and Open Source
        • Abstraction layer over Docker CLI
        """,
        border_style="gray50", 
        subtitle="Version 0.7.0"
    )

if __name__ == "__main__": 
    app()