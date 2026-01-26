import shutil
from app.utils.ui import TextStyles, TableDisplay

def check_tool(tool_name: str) -> bool:

    """Checks if a tool is installed and available in PATH."""

    path = shutil.which(tool_name)

    if not path:
        # TextStyles().error_text(f"{tool_name} is missing!")
        return False

    return True


def init():
    """ Initializes the environment by verifying essential tools. """

    text = TextStyles()
    table_err = TableDisplay("", ["Tool", "Status", "Message"])
    table_ok = TableDisplay("", ["Tool", "Status", "Message"])

    text.style_text("DevMate - Initialization", style="white")
    text.style_text("Checking for essential tools...", style="white")

    all_good = True

    try:

        # 1. Check Git
        if not check_tool("git"):
            all_good = False
            table_err.add_row(["Git", "Missing", "Install git from https://git-scm.com/"], style="red")
        else:
            table_ok.add_row(["Git", "Installed", "Git is installed and available!"])

        # 2. Check Docker
        if not check_tool("docker"):
            all_good = False
            table_err.add_row(["Docker", "Missing", "Install Docker from https://www.docker.com/"], style="red")
        else:
            table_ok.add_row(["Docker", "Installed", "Docker is installed and available!"])
        
        # 3. Check Python
        if not check_tool("python3"):
            # Fallback check for 'python' if 'python3' isn't explicitly named
            if not check_tool("python"):
                all_good = False
                table_err.add_row(["Python", "Missing", "Install Python from https://www.python.org/"], style="red")
            else:
                table_ok.add_row(["Python", "Installed", "Python is installed and available!"])
        else:
            table_ok.add_row(["Python", "Installed", "Python is installed and available!"])

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