from git import Repo, GitCommandError 
from pathlib import Path


def clone_repo(
    url: str,
    directory: Path,
    branch: str = None
):
    directory = directory.absolute().expanduser().resolve(strict=False)

    directory.mkdir(parents=True, exist_ok=True)

    if directory.exists() and any(directory.iterdir()):
        raise FileExistsError("Directory is not empty")

    try:
        if branch:
            Repo.clone_from(url, directory, branch=branch)
        else:
            Repo.clone_from(url, directory)
    except GitCommandError as e:
        raise RuntimeError(f"Git clone failed: {e}") from e

