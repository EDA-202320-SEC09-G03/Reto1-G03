"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
assert cf
from tabulate import tabulate
from datetime import datetime as dt
import traceback
import threading
default_limit = 1000

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller(adt):
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
   
    control = controller.new_controller(adt)
    return control


def print_menu():
    print("Bienvenido\n")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Cambiar tamaño, ADT y algoritmo de ordenamiento")
    print("10- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control, file_size, algorithm):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    results, goalscorers, shootouts, d_time = controller.load_data(control,file_size, algorithm)

    print('Total de encuentros cargados: ' + str(results))
    print('Total de anotaciones cargadas: ' + str(goalscorers))
    print('Total de goles marcados desde el punto penal cargados: ' + str(shootouts))

    print('Tiempo de ordenamiento: ', d_time)

    print("Primeros y ultimos 3 resultados: \n")

    keys_result = ['date', 'home_team', 'away_team', 'home_score', 'away_score', 'country', 'city', 'tournament']
    table_results = print_tabulate(control['model']['results'], keys_result)
    print(table_results, "\n")

    print("Primeros y ultimos 3 anotadores: \n")

    keys_goalscorers = ['date', 'home_team', 'away_team', 'scorer', 'team', 'minute', 'penalty', 'own_goal']
    table_goalscorers = print_tabulate(control['model']['goalscorers'], keys_goalscorers)
    print(table_goalscorers, "\n")

    print("Primeros y ultimos 3 goles:\n")

    keys_shootouts = ['date', 'home_team', 'away_team', 'winner']
    table_shootouts = print_tabulate(control['model']['shootouts'], keys_shootouts)
    print(table_shootouts, "\n")
    
    return d_time


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def choose_adt():
    print("Por favor elije el ADT que prefieras: ")
    print('1. Array List')
    print('2. Single Linked List')
    user = input("Selecciona una opción: ")
    if int(user) == 1:
        return 'ARRAY_LIST'
    elif int(user) == 2:
        return 'SINGLE_LINKED'
    else:
        return None
    
def choose_size():
    print('Por favor elija el tamaño de archivo a cargar: ')
    print('1. Small')
    print('2. Large')
    print('3. 5pct')
    print('4. 10pct')
    print('5. 20pct')
    print('6. 30pct')
    print('7. 50pct')
    print('8. 80pct')

    choice = int(input('Seleccione una opción: '))

    if choice == 1:
        return 'small'
    elif choice == 2:
        return 'large'
    elif choice == 3:
        return '5pct'
    elif choice == 4:
        return '10pct'
    elif choice == 5:
        return '20pct'
    elif choice == 6:
        return '30pct'
    elif choice == 7:
        return '50pct'
    elif choice == 8:
        return '80pct'
    else:
        return None

def choose_sort():
    print('Por favor elija el algoritmo de ordenamiento que desea:')
    print('1. Shell Sort')
    print('2. Insertion Sort')
    print('3. Selection Sort')
    print('4. Merge Sort')
    print('5. Quick Sort')

    choice = int(input('Seleccione una opción: '))

    if choice == 1:
        return 'shell'
    elif choice == 2:
        return 'insertion'
    elif choice == 3:
        return 'selection'
    elif choice == 4:
        return 'merge'
    elif choice == 5:
        return 'quick'
    else:
        return None
    
def print_tabulate(data_struct, columns):
    data = data_struct

    #Filtrar solo ultimos y primeros 3 datos si es muy grande la lista
    if lt.size(data_struct) > 6:
        data = controller.get_first_last_three(data_struct)
        print('Se encontraron más de 6 resultados...')

    #Lista vacía para crear la tabla
    reduced = []

    #Iterar cada línea de la lista
    for result in data['elements']:
        line = []
        #Iterar las columnas para solo imprimir las deseadas
        for column in columns:

            #Creación de subtabla para el requerimiento 6
            if column == 'top_scorer':
                topscorer = []
                keys_scorer = ['name', 'goals', 'matches', 'avg_time']
                for column_scorer in keys_scorer:
                    topscorer.append(result[column][column_scorer])
                list = [keys_scorer, topscorer]
                table_scorer = tabulate(list, headers='firstrow', tablefmt='grid')
                line.append(table_scorer)

            #Creación de subtabla para el requerimiento 7
            elif column == 'last_goal':
                last_goal = []
                keys = ['date', 'tournament', 'home_team', 'away_team', 'home_score', 'away_score', 'minute', 'penalty', 'own_goal']
                for key in keys:
                    last_goal.append(result[column][key])
                list = [keys, last_goal]
                subtable = tabulate(list, headers='firstrow', tablefmt='grid')
                line.append(subtable)
            else:
                line.append(result[column])

        reduced.append(line)
    table = tabulate(reduced, headers=columns, tablefmt="grid")
    return table


def print_req_1(control, n_results, team_name, condition):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    list, total, d_time = controller.req_1(control, n_results, team_name, condition)
    print(("="*15) + "Req No. 1 Inputs" + ("="*15))
    print('Team name:', team_name)
    print('Team condition:', condition + '\n')

    print(("="*15) + "Req No. 1 Results" + ("="*15))
    print('Total matches found:', str(total))
    print('Selecting', str(n_results), 'matches...' + '\n')

    columns = ['date', 'home_team', 'away_team', 'home_score', 'away_score', 'country', 'city', 'tournament']
    table = print_tabulate(list, columns)
    print(table)
    print('')
    d_time = f'{d_time:.3f}'
    print('Tiempo de ejecución:', str(d_time), 'ms')

def print_req_2(control, n_goals, name):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    data, total, d_time = controller.req_2(control, n_goals, name)
    keys = ['date', 'home_team', 'away_team', 'team', 'scorer', 'minute', 'own_goal', 'penalty']
    table = print_tabulate(data, keys)
    print('Total scorers found:', total, '\n')
    print(table)
    d_time = f'{d_time:.3f}'
    print('Tiempo de ejecución:', str(d_time), 'ms')


def print_req_3(control, name, inicial, final):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    list, size, home, away,d_time = controller.req_3(control, name, inicial, final)
    print(("="*15) + "Req No. 3 Inputs" + ("="*15))
    print('Team name:', name)
    print('Start date:', inicial)
    print('End date:', final, '\n')

    print(("="*15) + "Req No. 3 Results" + ("="*15))
    print(name, 'Total games:', str(size))
    print(name, 'Total home games:', str(home))
    print(name, 'Total away games:', str(away), '\n')

    columns = ['date', 'home_score', 'away_score', 'home_team', 'away_team', 'country', 'city', 'tournament', 'penalty', 'own_goal']
    table = print_tabulate(list, columns)
    print(table)
    d_time = f'{d_time:.3f}'
    print('Tiempo de ejecución:', str(d_time), 'ms')


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    nombre_torneo = "Copa América" #input("Diga el nombre del torneo: ")
    fecha_inicial =  "1955-06-01" #input("Ingrese la fecha inicial: ")
    fecha_final = "2022-06-30" #input("Ingrese la fecha final: ")
    data, ciudades, paises, total_matches, penaltis, d_time = controller.req_4(control, nombre_torneo, fecha_inicial, fecha_final)
    partidos = lt.size(data)

    print("Partidos: ", partidos)
    print('Paises:',paises)
    print('Ciudades:', ciudades)
    print("Penaltis: ", penaltis)

    # Se filtran los datos para que queden en orden como en el pdf 
    lista_llaves = ["date", "tournament", "country", "city", "home_team", "away_team", "home_score", "away_score", "winner"]
    lista_ultimate = print_tabulate(data, lista_llaves)
    print(lista_ultimate)
    d_time = f'{d_time:.3f}'
    print('Tiempo de ejecución:', str(d_time), 'ms')


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control, n_equipos, torneo, fecha_inicial, fecha_final):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    data, n_teams, n_results, n_countries, n_cities, mostmatches,d_time = controller.req_6(control, n_equipos, torneo, fecha_inicial, fecha_final)
    keys = ['name', 'total_points', 'goal_difference', 'penalty_points', 'matches', 'own_goal_points', 'wins', 'draws', 'losses', 'goals_for', 'goals_against', 'top_scorer']
    print(torneo, 'Total teams:', str(n_teams))
    print(torneo, 'Total matches:', str(n_results))
    print(torneo, 'Total countries:', str(n_countries))
    print(torneo, 'Total cities:', str(n_cities))
    print(torneo, 'with most matches:', mostmatches)
    table = print_tabulate(data, keys)
    print(table)
    d_time = f'{d_time:.3f}'
    print('Tiempo de ejecución:', str(d_time), 'ms')  


def print_req_7(control, fecha_inicial, fecha_final, top_jugadores):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    sublist, num_jugadores, num_partidos, num_goles, num_penales, num_autogoles, num_tourns, d_time = controller.req_7(control, fecha_inicial, fecha_final, top_jugadores)
    keys = ['name', 'total_points', 'total_goals', 'penalty_goals', 'own_goals', 'avg_time', 'total_tournaments', 'scored_in_wins', 'scored_in_losses', 'scored_in_draws', 'last_goal']
    table = print_tabulate(sublist, keys)
    print(table)
    d_time = f'{d_time:.3f}'
    print('Tiempo de ejecución:', str(d_time), 'ms')


def print_req_8(control, equipo1, equipo2, inicial, final):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    data, common, new1, new2, nc, infot1, infot2, infocommon = controller.req_8(control, equipo1, equipo2, inicial, final)
    keys = ['name', 'total_points', 'goal_difference', 'penalty_points', 'matches', 'wins', 'draws', 'losses', 'goals_for', 'goals_against', 'top_scorer']
    keysn1 = ['date', 'home_team', 'away_team', 'home_score', 'away_score', 'country', 'city', 'tournament']

    tablen1 = print_tabulate(new1, keysn1)
    tablen2 = print_tabulate(new2, keysn1)
    tableteam1 = print_tabulate(data['team1'], keys)
    tableteam2 = print_tabulate(data['team2'], keys)
    tablecommon = print_tabulate(common, keysn1)
    tablenc = print_tabulate(nc, keysn1)

    print('-'*10, equipo1, 'Statistics', '-'*10)
    print('Years:', str(infot1['years']))
    print('Total matches:', str(infot1['matches']))
    print('Total home matches:', str(infot1['home']))
    print('Total away matches:', str(infot1['away']))
    print('Oldest match date:', infot1['oldest'], '\n')

    print(tablen1, '\n')
    print('+'*10, 'yearly statistics', '+'*10)
    print(tableteam1, '\n')

    print(tablen2)
    print(tableteam2)
    print(tablenc)
    print(tablecommon)

 # Se crea el controlador asociado a la vista
control = None
file_size = None
adt = None
sort = None

# main del reto
def menu_cycle(control, file_size, adt, sort):
    """
    Menu principal
    """
    default_limit = 1000
    working = True
    threading.stack_size(67108864*2) # 128MB stack
    sys.setrecursionlimit(default_limit*1000000)
    #thread = threading.Thread(target=menu_cycle)
    #thread.start()
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('\nSeleccione una opción para continuar: ')
        if int(inputs) == 1:
            if file_size == None:
                file_size = 'small'
            if adt == None:
                adt = 'ARRAY_LIST'
            if sort == None:
                sort = 'merge'

            if file_size != None and sort != None and sort != None:

                control = new_controller(adt)
                print("Cargando información de los archivos ....\n")

                d_time = load_data(control, file_size, sort)
                d_time = f'{d_time:.3f}'

                print('Tamaño de archivo:', file_size)
                print('ADT:', adt)
                print('Algoritmo de ordenamiento:', sort)
                print('Tiempo de ordenamiento:', d_time)

            else:
                print('Por favor selecciona una opción válida')

        elif int(inputs) == 2: 
            n_results = int(input('Numero de partidos de consulta: '))
            team_name = input('Ingrese el nombre del equipo: ')
            print('Por favor elija alguna de las siguientes opciones:')
            print('1. Local')
            print('2. Visitante')
            print('3. Indiferente')
            condition = int(input('Digite su opción: '))
            if condition == 1:
                print_req_1(control, n_results, team_name, 'local')
            elif condition == 2:
                print_req_1(control, n_results, team_name, 'visitante')
            elif condition == 3:
                print_req_1(control, n_results, team_name, 'neutro')
            else:
                print("Por favor seleccione una opción válida")

        elif int(inputs) == 3:
            n_goals = int(input('Numero de goles: '))
            name = input('Nombre completo del jugador: ')
            print_req_2(control, n_goals, name)

        elif int(inputs) == 4:
            name = input('Ingrese el nombre del equipo: ')
            print('Por favor coloque las fechas en el siguiente formato: YYYY-MM-DD')
            inicial = input('Ingrese la fecha inicial: ')
            final = input('Ingrese la fecha final: ')
            print_req_3(control, name, inicial, final)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            n_equipos = int(input('Digite la cantidad de equipos para la consulta: '))
            torneo = input('Escriba el nombre del torneo: ')
            print('Por favor coloque las fechas en el siguiente formato: YYYY-MM-DD')
            inicial = input('Ingrese la fecha inicial: ')
            final = input('Ingrese la fecha final: ')
            print_req_6(control, n_equipos, torneo, inicial, final)

        elif int(inputs) == 8:
            top_jugadores = 17 #input("Diga el número (N) de jugadores para consulta: ")
            #print('Por favor coloque las fechas en el siguiente formato: YYYY-MM-DD')
            fecha_inicial =  "2002-03-25" #input("Ingrese la fecha inicial: ")
            fecha_final = "2021-11-23" #input("Ingrese la fecha final: ")
            print_req_7(control, fecha_inicial, fecha_final, top_jugadores)

        elif int(inputs) == 9:
            equipo1 = input('Nombre del primer equipo: ')
            equipo2 = input('Nombre del segundo equipo: ')
            print('Por favor coloque las fechas en el siguiente formato: YYYY-MM-DD')
            inicial = input('Ingrese la fecha inicial: ')
            final = input('Ingrese la fecha final: ')

            print_req_8(control, equipo1, equipo2, inicial, final)

        elif int(inputs) == 10:
            file_size = choose_size()
            adt = choose_adt()
            sort = choose_sort()

            print('\n' + "-"*10 + 'Ejecuta la opción 1 para actualizar los cambios' + '-'*10 + '\n')

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864*2) # 128MB stack
    sys.setrecursionlimit(default_limit*1000000)
    thread = threading.Thread(target=menu_cycle, args=[control, file_size, adt, sort])
    thread.start()