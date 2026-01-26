from typer import Option
import shutil
from app.utils.ui import TextStyles, TableDisplay
from app.utils.verbose import vprint

def check_tool(tool_name: str, verbose: bool) -> bool:
    """Checks if a tool is installed and available in PATH."""

    path = shutil.which(tool_name)
    text = TextStyles()

    if not path:
        vprint(verbose, text.error_text, f"{tool_name} is missing!")
        return False

    vprint(verbose, text.success_text, f"{tool_name} is installed and available!")
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

    text = TextStyles()
    table_err = TableDisplay("", ["Tool", "Status", "Message"])
    table_ok = TableDisplay("", ["Tool", "Status", "Message"])

    text.style_text("DevMate - Initialization", style="white")
    text.style_text("Checking for essential tools...", style="white")

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
            vprint(verbose, text.success_text, "python3 is installed and available!")
            table_ok.add_row(["Python", "Installed", "Python is installed and available!"])
        elif check_tool("python", verbose):
            table_ok.add_row(["Python", "Installed", "Python is installed and available!"])
        else:
            all_good = False
            table_err.add_row(["Python", "Missing", "Install Python from https://www.python.org/"], style="red")

        if all_good:
            text.success_text("All tools are installed and available!")
            table_ok.show()
        else:
            text.info_text("\nSummary:")
            table_ok.show()
            text.error_text("\nSome tools are missing. Please install them and try again.")
            table_err.show()

    except Exception as e:
        text.error_text(str(e))