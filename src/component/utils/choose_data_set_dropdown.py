from typing import List

import flet as ft

from src.component.utils import DropType


class ChooseDataSetDropdown(ft.Dropdown):
    OPTIONS: List[DropType] = [
        DropType("1", "Conjunto 1"),
        DropType("2", "Conjunto 2"),
        DropType("3", "Conjunto 3"),
        DropType("4", "Conjunto 4"),
    ]

    def __init__(self):
        # Convertir DropType a ft.dropdown.Option
        dropdown_options = [
            ft.dropdown.Option(option.key, option.text)
            for option in self.OPTIONS
        ]
        super().__init__(
            label="Conjunto de datos",
            width=200,
            options=dropdown_options,
            value="1"
        )