from app.utils import TextDisplay

def vprint(message: str, verbose: bool = False, style: str = "cyan") -> None: 
    if verbose:
        TextDisplay.style_text(message, style=style)
