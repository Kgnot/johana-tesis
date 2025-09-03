from typing import List

import flet as ft


class DropType:
    def __init__(self, key: str, text: str):
        self.key = key
        self.text = text

    def get_key(self):
        return self.key

    def get_text(self):
        return self.text


class GenericDropdown(ft.Dropdown):
    def __init__(self, lab: str, options: List[DropType], val: str):
        dropdown_options = [ft.dropdown.Option(option.get_key(), option.get_text()) for option in options]
        super().__init__(
            label=lab,
            width=200,
            options=dropdown_options,
            value=val
        )
