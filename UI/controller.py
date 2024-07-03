import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()
        self._nercId = None
        self._years = None
        self._hours = None

    def handleWorstCase(self, e):
        if ( self._nercId is None or self._years is None or self._hours is None
                or self._years=="" or self._hours=="" or isinstance(self._hours, str)
                or isinstance(self._years, str) ):
            self._view._txtOut.controls.append(ft.Text("Inserire tutte le opzioni!"))
        else:
            soluzione, customers, hours = self._model.worstCase(self._nercId, self._years, self._hours)
            self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {customers}"))
            self._view._txtOut.controls.append(ft.Text(f"Tot hours of outage: {hours}"))
            for sol in soluzione:
                self._view._txtOut.controls.append(ft.Text(sol.__str__()))
        self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc
        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(key=n._id, text=n._value, on_click=self.read_nerc))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v

    def read_years(self, e):
        self._years = int(e.control.value)

    def read_hours(self, e):
        self._hours = float(e.control.value)

    def read_nerc(self, e):
        self._nercId = e.control.key


