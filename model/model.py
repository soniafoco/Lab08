import copy

from database.DAO import DAO

class Model:
    def __init__(self):
        self._soluzioneOttima = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self._soluzioni = []


    def worstCase(self, nerc, maxY, maxH):

        self.loadEvents(nerc)
        self._soluzioni = []
        self.ricorsione([], maxY, maxH, 0)

        """
        for i in range(len(self._soluzioni)):
            print(f"Soluzione {i+1}:")
            for sol in self._soluzioni[i]:
                print(sol.__str__())
        """

        self.soluzione_ottima()

        print("Soluzione ottima:")
        for sol in self._soluzioneOttima:
            print(sol.__str__())

        return self._soluzioneOttima, self.count_customers(), self.count_hours()


    def ricorsione(self, parziale, maxY, maxH, index):

        if parziale!=[]:
            self._soluzioni.append(copy.deepcopy(parziale))  # Aggiungiamo una copia della combinazione corrente alla lista delle combinazioni
        for i in range(index, len(self._listEvents)):
            parziale.append(self._listEvents[i])  # Aggiungiamo l'elemento corrente alla combinazione corrente
            if self.is_valida(parziale, maxY, maxH):
                self.ricorsione(parziale, maxY, maxH, i+1)  # Chiamata ricorsiva per l'elemento successivo
            parziale.pop()  # Ripristiniamo lo stato precedente per esplorare altre possibilità


    def is_valida(self, parziale, maxY, maxH):
        countHours = 0
        for event in parziale:
            countHours += event.time
        if countHours > maxH:
            return False

        max = 0
        min = 2014

        for event in parziale:
            if event.date_event_began.year > max:
                max = event.date_event_began.year
            if event.date_event_began.year < min:
                min = event.date_event_began.year

        if max-min > maxY:
            return False

        return True

    def soluzione_ottima(self):
        max = 0
        i = 0
        for soluzione in self._soluzioni:
            sum_people = 0
            for sol in soluzione:
                sum_people += sol.customers_affected
            if sum_people > max:
                max = sum_people
                self._soluzioneOttima = soluzione

    def count_customers(self):
        sum = 0
        for sol in self._soluzioneOttima:
            sum += sol.customers_affected
        return sum

    def count_hours(self):
        sum = 0
        for sol in self._soluzioneOttima:
            sum += sol.time
        return sum

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    @property
    def listNerc(self):
        return self._listNerc



