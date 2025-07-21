import shutil


class LoggerHelper:
    @staticmethod
    def print_full_width(text: str, char: str = "="):
        width = shutil.get_terminal_size().columns
        text = f" {text} "
        banner = text.center(width, char)
        print(banner)
