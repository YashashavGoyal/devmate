from typer import Typer, Context
from pathlib import Path
from app.utils.ui import print_markdown, TextDisplay

docs = Typer()

def show_doc(filename: str):
    """Displays the markdown documentation for a given filename."""
    docs_path = Path(__file__).parent / "content" / filename
    try:
        print_markdown(docs_path)
    except FileNotFoundError as fnfe:
        TextDisplay.error_text(f"Error: {fnfe}")

# callback for docs
@docs.callback(
    epilog="""
    EXAMPLES\n
    mate docs\n
    mate docs clone\n
    mate docs deploy\n
    """,
    invoke_without_command=True
)
def docs_callback(ctx: Context):
    """
    Show documentation for mate commands.
    """
    if ctx.invoked_subcommand is None:
        show_doc("main.md")

@docs.command()
def clone():
    """Clone documentation"""
    show_doc("clone.md")

@docs.command()
def deploy():
    """Deploy documentation"""
    show_doc("deploy.md")

@docs.command()
def down():
    """Down documentation"""
    show_doc("down.md")

@docs.command()
def health():
    """Health documentation"""
    show_doc("health.md")

@docs.command()
def init():
    """Init documentation"""
    show_doc("init.md")

@docs.command()
def logs():
    """Logs documentation"""
    show_doc("logs.md")

@docs.command()
def shell():
    """Shell documentation"""
    show_doc("shell.md")

@docs.command()
def status():
    """Status documentation"""
    show_doc("status.md")

@docs.command()
def up():
    """Up documentation"""
    show_doc("up.md")

@docs.command()
def workflow():
    """Workflow documentation"""
    show_doc("workflow.md")