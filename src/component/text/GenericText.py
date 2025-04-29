
import flet as ft


class GenericText(ft.Text):
    def __init__(self, text:str,size:int=16,weight=None,color = "black"):
        ft.Text.__init__(self,text,size=size, weight=weight, color=color)