from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.json import JSON
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

console = Console()

class TextDisplay:
    INFO = "blue"
    WARNING = "yellow"
    ERROR = "red"
    SUCCESS = "green"

    @staticmethod
    def style_text(text: str, style: str):
        console.print(f"[{style}]{text}[/{style}]")
    
    @staticmethod
    def success_text(text: str, style: str = ""):
        style_n = f"{style} {TextDisplay.SUCCESS}".strip()
        TextDisplay.style_text(text, style_n)

    @staticmethod
    def warn_text(text: str, style: str = ""):
        style_n = f"{style} {TextDisplay.WARNING}".strip()
        TextDisplay.style_text(text, style_n)
    
    @staticmethod
    def error_text(text: str, style: str = ""):
        style_n = f"{style} {TextDisplay.ERROR}".strip()
        TextDisplay.style_text(text, style_n)
    
    @staticmethod
    def info_text(text: str, style: str = ""):
        style_n = f"{style} {TextDisplay.INFO}".strip()
        TextDisplay.style_text(text, style_n) 
    
    @staticmethod
    def print_json( json:dict, style: str = "White"):
        json_obj = JSON.from_data(json, indent=4)
        console.print(json_obj, style=style)
    
    @staticmethod
    def print_panel(title: str, content: str, border_style: str = "blue", subtitle: str = None, subtitle_align: str = "right"):
        panel = Panel(content, title=title, title_align="left", border_style=border_style, style="white", subtitle=subtitle, subtitle_align=subtitle_align)
        console.print(panel)

class PanelDisplay:
    ERROR = "bold red"
    SUCCESS = "bold green"
    INFO = "bold blue"
    WARNING = "bold yellow"    

    @staticmethod
    def print_panel(title: str, content: str, border_style: str = "blue", subtitle: str = None, subtitle_align: str = "right"):
        panel = Panel(content, title=title, title_align="left", border_style=border_style, style="white", subtitle=subtitle, subtitle_align=subtitle_align)
        console.print(panel)

    @staticmethod
    def print_error(title: str, content: str):
        PanelDisplay.print_panel(title, content, border_style=PanelDisplay.ERROR)

    @staticmethod
    def print_success(title: str, content: str):
        PanelDisplay.print_panel(title, content, border_style=PanelDisplay.SUCCESS)
    
    @staticmethod
    def print_info(title: str, content: str):
        PanelDisplay.print_panel(title, content, border_style=PanelDisplay.INFO)
    
    @staticmethod
    def print_warning(title: str, content: str):
        PanelDisplay.print_panel(title, content, border_style=PanelDisplay.WARNING)

    @staticmethod
    def print_json( title: str, json: dict, content: str = "", title_align: str = "left", border_style:str = "gray50"):
        body = Group(
            content,
            JSON.from_data(json, indent=4)
        )
        panel = Panel(
            body,
            title=title,
            title_align=title_align,
            border_style=border_style,
        )
        console.print(panel)

    @staticmethod
    def print_multi_style_panel(
            title: str, 
            content_parts: list, 
            border_style: str = "blue bold",
            title_align: str = "left",
        ):
        combined_content = Text()
        for part, style in content_parts:
            combined_content.append(str(part), style=style)

        panel = Panel(
            combined_content,
            title=title,
            title_align=title_align,
            border_style=border_style,
        )
        console.print(panel)

class Prompt:
    @staticmethod
    def ask(question: str, choices: list = None) -> str:
        if choices:
            choice_str = "/".join(choices)
            prompt = f"{question} ({choice_str}): "
            while True:
                response = console.input(prompt)
                if response in choices:
                    return response
                TextDisplay.error_text(f"Invalid choice. Please choose from: {', '.join(choices)}")
        else:
            prompt = f"{question}: "
            return console.input(prompt)
    
    @staticmethod
    def confirm(question: str) -> bool:
        response = console.input(f"{question} (y/n): ").strip().lower()
        while response not in ['y', 'yes', 'n', 'no']:
             TextDisplay.error_text("Invalid input. Please enter 'y' or 'n'.")
             response = console.input(f"{question} (y/n): ").strip().lower()
        return response in ['y', 'yes']
    
    @staticmethod
    def password(prompt: str) -> str:
        from getpass import getpass
        return getpass(prompt + ": ")
    
    @staticmethod
    def select(question: str, options: list) -> str:
        console.print(f"{question}")
        for idx, option in enumerate(options, start=1):
            console.print(f"[{idx}] {option}")
        
        while True:
            try:
                choice = int(console.input("Select an option by number: "))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    TextDisplay.error_text(f"Please enter a number between 1 and {len(options)}.")
            except ValueError:
                TextDisplay.error_text("Invalid input. Please enter a number.")

class ProgressBar:
    def __init__(self, total: int, description: str = "Processing", console=None):
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
        )
        self.task = self.progress.add_task(description, total=total)

    def __enter__(self):
        self.progress.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.progress.stop()
        return False

    def advance(self, step: int = 1):
        self.progress.advance(self.task, step)

    def update(self, completed: int):
        self.progress.update(self.task, completed=completed)

    def set_description(self, description: str):
        self.progress.update(self.task, description=description)

    def finish(self):
        task = self.progress.tasks[0]
        self.progress.update(task.id, completed=task.total)

class TableDisplay:
    def __init__(self, title: str, columns: list, style: str = "cyan"):
        self.table = Table(title=title)
        for col in columns:
            self.table.add_column(col, style=style, no_wrap=True)

    def add_row(self, row: list, style: str = "cyan"):
        self.table.add_row(*row, style=style)

    def show(self):
        console.print(self.table)

