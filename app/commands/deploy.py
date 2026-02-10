from pathlib import Path
from typing import List
from typer import Argument, Option, Exit
from rich.console import Console

from app.services import clone_repo
from app.commands import up
from app.utils import TextDisplay

console = Console()

def deploy(
    repo_url: str = Argument(..., help="The Git URL to clone"),
    name: str = Option(None, "-n", "--name", help="Custom folder name for the clone"),
    branch: str = Option(None, "-b", "--branch", help="Specific branch to clone"),
    port: List[str] = Option([], "-p", "--port", help="Port mappings to pass to the up command"),
    force: bool = Option(False, "-f", "--force", help="Force rebuild/restart"),
    location: str = Option(".", "-l", "--location", help="location of folder inside repo where Config files are present [default = '.']")
):
    if name:
        target_name = name
    else:
        target_name = repo_url.rstrip("/").split("/")[-1]
        if target_name.endswith(".git"):
            target_name = target_name[:-4]
    
    target_path = Path.cwd() / target_name
    
    if target_path.exists() and any(target_path.iterdir()):
        TextDisplay.error_text(f"Error: Directory '{target_name}' already exists and is not empty.")
        Exit(1)
        
    try:
        with console.status(f"[bold green]Cloning {repo_url}..."):
            clone_repo(repo_url, target_path, branch=branch)
        TextDisplay.success_text(f"Successfully cloned into {target_name}")
    except Exception as e:
        TextDisplay.error_text(f"Cloning failed: {e}")
        Exit(1)
        
    config_path = target_path / location
    
    if not config_path.exists():
         TextDisplay.warn_text(f"Warning: Config location {config_path} does not exist. 'up' command might fail.")

    TextDisplay.info_text(f"Starting deployment in {config_path}...")
    
    up(path=str(config_path), port=port, force=force)
