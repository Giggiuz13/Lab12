import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        self._listYear = self._model.Anni()
        self._listCountry = self._model.Nazioni()
        for y in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(key=y))
        for y in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(key=y))


    def handle_graph(self, e):
        naz= self._view.ddcountry.value
        ann= self._view.ddyear.value
        self._model.buildGraph(naz,ann)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente con {len(self._model._grafo.nodes)} nodi e {len(self._model._grafo.edges)} archi", color = "green"))
        self._view.update_page()



    def handle_volume(self, e):
        volumi = self._model.getVolume()
        for i in range(6):
            self._view.txtOut2.controls.append(ft.Text(f"{volumi[i][0]} --> {volumi[i][1]}"))
        self._view.update_page()



    def handle_path(self, e):
        num = int(self._view.txtN.value)
        percmax = self._model.trova_ciclo_massimo(num)
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {percmax[1]}"))
        count = 1
        for p in percmax[0]:
            if count == len(percmax[0]):
                break
            peso = self._model._grafo[p][percmax[0][count]]["weight"]
            self._view.txtOut3.controls.append(ft.Text(f"{p} ---> {percmax[0][count]}, peso : {peso}"))
            count = count + 1
        self._view.update_page()
