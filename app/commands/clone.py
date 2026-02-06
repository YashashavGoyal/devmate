from pathlib import Path
from typer import Argument, Option, Exit

from app.services import clone_repo
from app.utils import TextDisplay

def clone(
    url: str = Argument(..., help="URL of the git repository to clone"),
    local_dir: str | None = Option(None, "-d", "--dir", "--directory", help="Directory where the repository will be cloned"),
):
    try:
        if local_dir:
            target_dir = Path(local_dir)
        else:
            repo_name = url.rstrip("/").split("/")[-1]
            if repo_name.endswith(".git"):
                repo_name = repo_name[:-4]

            target_dir = Path.cwd() / repo_name

        clone_repo(url, target_dir)

        TextDisplay.success_text(f"Repository cloned into {target_dir}")

    except Exception as e:
        TextDisplay.error_text(f"Error: {e}")
        Exit(1)