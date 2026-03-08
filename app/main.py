from typer import Typer
from rich.console import Console

from app.utils import PanelDisplay, TextDisplay
from app.commands import init, health, clone, up, deploy, logs, shell, down, status

console = Console()

app = Typer(
    name="mate",
    help="Your friendly local development companion.",
    add_completion=True,
    no_args_is_help=True,
    rich_markup_mode="rich"
)
# devmate init
app.command(
    name="init",
    short_help="Checks if essential tools are installed. (Alias: doctor)",
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

# devmate status
app.command(
    name="status",
    short_help="Shows a clean, beautiful table of running containers. (Alias: ps, info)",
)(status)

# ...... Alias ......
app.command(
    name="doctor",
    hidden=True,
    help="Alias for init"
)(init)

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

app.command(
    name="ps",
    hidden=True,
    help="Alias for status"
)(status)


# mate version
@app.command(
    name="version",
    help="Show the current [bold cyan]version[/bold cyan] of mate."
)
def version():
    TextDisplay.style_text("mate: 1.0.0", style="blue")


# mate about
@app.command(
    name="about",
    help="The [bold]about[/bold] command displays information about mate."
)
def about():
    PanelDisplay.print_panel(
        "About mate",
        """
        mate
        A powerful developer companion designed to streamline your local workflow,
        automating container management and orchestrating dev environments with ease.

        Features:
        • Works with Docker Compose and Dockerfile
        • Free and Open Source
        • Abstraction layer over Docker CLI
        """,
        border_style="gray50", 
        subtitle="Version 1.0.0"
    )

if __name__ == "__main__": 
    app()