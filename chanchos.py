import random
import json
import matplotlib.pyplot as plt
import numpy
import os

def main():
    #simularHasta(20,1000)    #Sacar # para simular todos los jusgos hasta X jugadores tantas veces como setee en la funcion para las dos variantes
    playGames(1000, 4, True)  #Sacar # para simular X cant de veces con X cant de jugadores, True para lobo tira toda la casa y False para tirar solo una pared
    playGames(1000, 4, False)
    displayData(4,False)      #Sacar # para mostrar estadisticas para X cant de jugadores con o sin "loboTiraTodo o dejar vacia la segunda variable para mostrar y comparar ambos casos"
    #emptyCache()             #Sacar # para resetear estadisticas

class Player:

    def __init__(self, loboTiraTodo):
        self.state = {"verde": 0, "azul": 0, "colorado": 0, "amarillo": 0, "violeta": 0}
        self.loboTiraTodo = loboTiraTodo

    def throwDice(self):
        return random.randint(1, 6)

    def jugarRonda(self):
        dado = self.throwDice()
        if dado == 1:
            if self.loboTiraTodo:
                self.state = {"verde": 0, "azul": 0, "colorado": 0, "amarillo": 0, "violeta": 0}
            else:
                cantParedesActualmente = 0
                for value in self.state.values():
                    if value == 1:
                        cantParedesActualmente += 1
                paredATirar = random.randint(0, cantParedesActualmente)
                i = 0
                for key, val in self.state.items():
                    if val != 0:
                        if i == paredATirar:
                            self.state[key] = 0
                            break
                        i += 1
        elif dado == 2:
            self.state["verde"] = 1
        elif dado == 3:
            self.state["azul"] = 1
        elif dado == 4:
            self.state["amarillo"] = 1
        elif dado == 5:
            self.state["violeta"] = 1
        elif dado == 6:
            if self.state == {"verde": 1, "azul": 1, "colorado": 0, "amarillo": 1, "violeta": 1}:
                self.state["colorado"] = 1

class Game:

    def __init__(self, cantidadDeJugadores, loboTiraTodo):
        self.cantidadDeJugadores = cantidadDeJugadores
        self.loboTiraTodo = loboTiraTodo

        self.turn = 0
        self.gameStart = False
        self.gameOver = False
        self.jugadores = []

    def playGame(self):
        for i in range(self.cantidadDeJugadores):
            self.createPlayer()

        delay = 0
        counter = 0
        while random.randint(1, 6) != 1:
            delay += 1

        while self.gameOver == False:
            self.turn += 1
            for jugador in self.jugadores:
                if counter < delay:
                    counter += 1
                else:
                    assert isinstance(jugador, Player)
                    jugador.jugarRonda()

                    if jugador.state == {"verde": 1, "azul": 1, "colorado": 1, "amarillo": 1, "violeta": 1}:
                        self.gameOver = True
                        return self.turn

        return "error"

    def resetGame(self):
        self.turn = 0
        self.gameStart = False
        self.gameOver = False
        self.jugadores = []

    def createPlayer(self):
        self.jugadores.append(Player(self.loboTiraTodo))


def playGames(numOfGames, cantDeJugadores, loboTiraTodo):

    newStats = {}

    for i in range(numOfGames):
        juego = Game(cantDeJugadores, loboTiraTodo)
        cantRondas = juego.playGame()
        if str(cantRondas) in list(newStats.keys()):
            newStats[str(cantRondas)] += 1
        else:
            newStats[str(cantRondas)] = 1

    newStats["loboTiraTodo"] = loboTiraTodo
    newStats['cantDeJugadores'] = cantDeJugadores

    saveGames(newStats)


def saveGames(newStat):
    if os.path.isfile('Estadisticas Chanchos.txt') == False:
        oldstats = []
    else:
        f = open('Estadisticas Chanchos.txt', 'r')

        lines = f.read()
        f.close()

        if lines != "":
            oldstats = json.loads(lines)
        else:
            oldstats = []

    newStat = json.loads(json.dumps(newStat))

    nostat = True
    for oldStat in oldstats:
        if oldStat["cantDeJugadores"] == newStat["cantDeJugadores"] and oldStat["loboTiraTodo"] == newStat["loboTiraTodo"]:
            nostat = False
            for newKey, newValue in list(newStat.items()):
                if newKey in list(oldStat.keys()) and newKey not in ["cantDeJugadores","loboTiraTodo"]:
                    oldStat[newKey] += newStat[newKey]
                else:
                    if newKey not in ["cantDeJugadores", "loboTiraTodo"]:
                        oldStat[newKey] = newStat[newKey]

    if nostat:
        oldstats.append(newStat)

    f = open('Estadisticas Chanchos.txt', 'w')
    f.write(json.dumps(oldstats))
    f.close()

def emptyCache():
    f = open('Estadisticas Chanchos.txt', 'w')
    f.write("")
    f.close()

def displayData(cant,loboTiraTodo = None):
    if os.path.isfile('Estadisticas Chanchos.txt') == False:
        print("No hay estadisticas")
    else:
        f = open('Estadisticas Chanchos.txt', 'r')

        lines = f.read()
        f.close()

        if lines == "":
            print("No hay estadisticas")
            return
        stats = json.loads(lines)

        if loboTiraTodo != None:
            nostat = True
            for stat in stats:
                if stat["cantDeJugadores"] == cant and stat["loboTiraTodo"] == loboTiraTodo:
                    nostat = False

                    veces = 0
                    purStat = {}

                    for key, value in list(stat.items()):
                        if key not in ["cantDeJugadores", "loboTiraTodo"]:
                            veces += value
                            purStat[int(key)] = int(value)


                    print("Cantidad de jugadores: " + str(cant))
                    if loboTiraTodo:
                        label = "Lobo tira todo"
                        print("Lobo tira todo: Si")
                    else:
                        label = "Lobo no tira todo"
                        print("Lobo tira todo: No")
                    print("Tamano de la muestra: " + str(veces))

                    maxValue = 0
                    maxKey = 0
                    lista = []
                    for key, value in list(purStat.items()):
                        if value > maxValue:
                            maxValue = value
                            maxKey = key
                        for j in range(value):
                            lista.append(key)

                    print("La moda es: " + str(maxKey) + " con " + str(maxValue) + " apariciones, " + str(
                        maxValue * 100 / veces)[:4] + "% del total de la muestra")
                    print("La media es: " + str(numpy.mean(lista))[:5])
                    print("La mediana es: " + str(numpy.median(lista))[:5])
                    print("El Desvio Estandar es: " + str(numpy.std(lista))[:5])

                    plt.bar(list(purStat.keys()), list(purStat.values()), color='g', label=label)
                    plt.legend(loc='upper right')
                    plt.show()

            if nostat:
                print("no hay estadisticas")
        else:
            nostat = True
            purStatCon = {}
            purStatSin = {}
            vecesCon = 0
            vecesSin = 0
            for stat in stats:
                if stat["cantDeJugadores"] == cant and stat["loboTiraTodo"] == True:
                    nostat = False

                    for key, value in list(stat.items()):
                        if key not in ["cantDeJugadores", "loboTiraTodo"]:
                            vecesCon += value
                            purStatCon[int(key)] = int(value)

                if stat["cantDeJugadores"] == cant and stat["loboTiraTodo"] == False:
                    nostat = False

                    for key, value in list(stat.items()):
                        if key not in ["cantDeJugadores", "loboTiraTodo"]:
                            vecesSin += value
                            purStatSin[int(key)] = int(value)

            if nostat:
                print("no hay estadisticas")
            else:
                if purStatCon == {} or purStatSin == {}:
                    print("no hay estadisticas")
                else:
                    # print stats
                    print("Cantidad de jugadores: " + str(cant))
                    print("")

                    print("Lobo tira todo: Si")
                    print("Tamano de la muestra: " + str(vecesCon))

                    maxValueCon = 0
                    maxKeyCon = 0
                    listaCon = []
                    for key, value in list(purStatCon.items()):
                        if value > maxValueCon:
                            maxValueCon = value
                            maxKeyCon = key
                        for j in range(value):
                            listaCon.append(key)

                    maxValueSin = 0
                    maxKeySin = 0
                    listaSin = []
                    for key, value in list(purStatSin.items()):
                        if value > maxValueSin:
                            maxValueSin = value
                            maxKeySin = key
                        for j in range(value):
                            listaSin.append(key)

                    print("La moda es: " + str(maxKeyCon) + " con " + str(maxValueCon) + " apariciones, " + str(
                        maxValueCon * 100 / vecesCon)[:4] + "% del total de la muestra")
                    print("La media es: " + str(numpy.mean(listaCon))[:5])
                    print("La mediana es: " + str(numpy.median(listaCon))[:5])
                    print("El Desvio Estandar es: " + str(numpy.std(listaCon))[:5])
                    print("")

                    print("Lobo tira todo: No")

                    print("Tamano de la muestra: " + str(vecesSin))



                    print("La moda es: " + str(maxKeySin) + " con " + str(maxValueSin) + " apariciones, " + str(
                        maxValueSin * 100 / vecesSin)[:4] + "% del total de la muestra")
                    print("La media es: " + str(numpy.mean(listaSin))[:5])
                    print("La mediana es: " + str(numpy.median(listaSin))[:5])
                    print("El Desvio Estandar es: " + str(numpy.std(listaSin))[:5])

                    plt.bar(list(purStatCon.keys()), list(purStatCon.values()), color='g', alpha = 0.4, label='Lobo tira todo') #con = verde
                    plt.bar(list(purStatSin.keys()), list(purStatSin.values()), color='b', alpha = 0.4, label='Lobo no tira todo') #sin = azul
                    plt.legend(loc='upper right')
                    plt.show()


def simularHasta(cantidadDeJugadores, cantidadDeVeces): #Con las dos variantes del juego
    for i in range(1,cantidadDeJugadores + 1):
        playGames(cantidadDeVeces,i,False)
        playGames(cantidadDeVeces, i, True)


if __name__ == '__main__':
    main()

