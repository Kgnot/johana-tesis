import flet as ft

class GenericText(ft.Text):
    def __init__(self, text:str,size:int=24,weight:str=None):
        ft.Text.__init__(self,text,size=size, weight=weight, color="black")