import flet as ft

#Logic
from logic.openSim.openSim import execModelo
# SRC
from src.component.sidebar.Sidebar import Sidebar
from src.component.variableComponent.ContentContainer import ContentContainer
from src.frame.Frame import Frame
from src.views.ActivityRecognition import ActivityRecognition
from src.views.HomeView import HomeView
from src.views.ManualView import ManualView
from src.views.VelocityView import VelocityView
from src.views.gaitParameters import GaitParameters


class ModelApp:

    def __init__(self):
        self.frame:Frame = None
        #Principales del frame
        self.sidebar:Sidebar = None
        self.content_container:ContentContainer = None
        # Vistas y páginas:
        self.homePage:HomeView = HomeView()
        self.velocityView:VelocityView = VelocityView()
        self.activityRecognition:ActivityRecognition = ActivityRecognition()
        self.gaitParameter: GaitParameters = GaitParameters()
        self.manualView:ManualView = ManualView("https://bibliotecadigital.ilce.edu.mx/Colecciones/CuentosMas/Cenicienta.pdf",
                                     "https://www.youtube.com/watch?v=QB0tJajDvMw")

    def start(self):
        ft.app(target=self.run)

    def run(self, page: ft.Page):
        self.frame = Frame(page) #Creamos el frame
        self.content_container = ContentContainer()
        self.sidebar = Sidebar(w=200, color="white", on_change=self.on_nav_change) # Creamos el slidebar

        self.frame.add(self.sidebar, self.content_container) # añadimos el slidebar

    def on_nav_change(self, e):
        print(f"Cambiando a la página {e.control.selected_index}")

        new_content = None
        if e.control.selected_index == 5:
            execModelo()
        elif e.control.selected_index == 0:
            new_content = self.homePage
        elif e.control.selected_index == 1:
            new_content = self.velocityView
        elif e.control.selected_index == 2:
            new_content = self.gaitParameter
        elif e.control.selected_index == 3:
            new_content = self.activityRecognition
        elif e.control.selected_index == 4:
            new_content = self.manualView

        if new_content:
            self.content_container.content = new_content
            self.content_container.update()


