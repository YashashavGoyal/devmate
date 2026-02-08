from typer import Option
import shutil
from app.utils import TextDisplay, TableDisplay
from app.utils import vprint

def check_tool(tool_name: str, verbose: bool) -> bool:
    """Checks if all the required tools are installed and available in PATH or guide user to install them."""

    path = shutil.which(tool_name)

    if not path:
        vprint(f"{tool_name} is missing!", verbose=verbose, style="red")
        return False

    vprint(f"{tool_name} is installed and available!", verbose=verbose, style="green")
    return True


def init(
    verbose: bool = Option(False, "--verbose", "-v", help="Show verbose output."),
):
    """
    Initialize the [bold green]devmate[/bold green] environment.\n
    This command performs the following checks:
    * :white_check_mark: Checks if [bold]Git[/bold] is installed.
    * :white_check_mark: Checks if [bold]Docker[/bold] is installed.
    * :white_check_mark: Checks if [bold]Python[/bold] is available.
    If any tools are missing, it will guide you on how to install them.
    """

    table_err = TableDisplay("", ["Tool", "Status", "Message"])
    table_ok = TableDisplay("", ["Tool", "Status", "Message"])

    TextDisplay.style_text("DevMate - Initialization", style="white")
    TextDisplay.style_text("Checking for essential tools...", style="white")

    all_good = True

    try:

        # 1. Check Git
        if not check_tool("git", verbose):
            all_good = False
            table_err.add_row(["Git", "Missing", "Install git from https://git-scm.com/"], style="red")
        else:
            table_ok.add_row(["Git", "Installed", "Git is installed and available!"])

        # 2. Check Docker
        if not check_tool("docker", verbose):
            all_good = False
            table_err.add_row(["Docker", "Missing", "Install Docker from https://www.docker.com/"], style="red")
        else:
            table_ok.add_row(["Docker", "Installed", "Docker is installed and available!"])

        # 3. Check Python
        if check_tool("python3", False):
            vprint("python3 is installed and available!", verbose=verbose, style="green")
            table_ok.add_row(["Python", "Installed", "Python is installed and available!"])
        elif check_tool("python", verbose):
            table_ok.add_row(["Python", "Installed", "Python is installed and available!"])
        else:
            all_good = False
            table_err.add_row(["Python", "Missing", "Install Python from https://www.python.org/"], style="red")

        if all_good:
            TextDisplay.success_text("\nAll tools are installed and available!")
            table_ok.show()
        else:
            TextDisplay.info_text("\nSummary:")
            table_ok.show()
            TextDisplay.error_text("\nSome tools are missing. Please install them and try again.")
            table_err.show()

    except Exception as e:
        TextDisplay.error_text(str(e))