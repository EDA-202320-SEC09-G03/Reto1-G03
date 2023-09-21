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
import traceback
import threading

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

    file1 = 'results'
    table_results = controller.get_first_last_three_datastructs(control, file1)
    keys_result = ['date', 'home_team', 'away_team', 'home_score', 'away_score', 'country', 'city', 'tournament']
    reduced_table = []
    for dict in table_results['elements']:
        line = []
        for key in keys_result:
            line.append(dict[key])
        reduced_table.append(line)
    print(tabulate(reduced_table, headers=keys_result, tablefmt="grid"), "\n")

    print("Primeros y ultimos 3 anotadores: \n")

    file2 = "goalscorers"
    table_goalscorers = controller.get_first_last_three_datastructs(control, file2)
    print(tabulate(table_goalscorers['elements'], headers="keys", tablefmt="grid"), "\n")

    print("Primeros y ultimos 3 goles:\n")

    file3 = "shootouts"
    table_shootouts = controller.get_first_last_three_datastructs(control, file3)
    print(tabulate(table_shootouts['elements'], headers="keys", tablefmt="grid"), "\n")
    
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


def print_req_1(control, n_results, team_name, condition):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    list, size = controller.req_1(control, team_name, condition)
    if size > 6:
        sublist = lt.subList(list, 1, n_results)
        table_req_1 = controller.get_first_last_three_list(sublist)
        print(tabulate(table_req_1['elements'], headers="keys", tablefmt="grid"), "\n")
    else:
        print(tabulate(list['elements'], headers="keys", tablefmt="grid"), '\n')
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control, name, inicial, final):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    list, size, home, away = controller.req_3(control, name, inicial, final)
    print('Numero de datos encontrados: ', size)
    print('Numero de datos como local: ', home)
    print('Numero de datos como visitante: ', away)
    
    if size > 6:
        sublist = lt.subList(list, 1, n_results)
        table_req_1 = controller.get_first_last_three_list(sublist)
        print(tabulate(table_req_1['elements'], headers="keys", tablefmt="grid"), "\n")
    else:
        print(tabulate(list['elements'], headers="keys", tablefmt="grid"), '\n')
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    nombre_torneo = input("Diga el nombre del torneo: ")
    fecha_inicial = input("Ingrese la fecha inicial: ")
    fecha_final = input("Ingrese la fecha final: ")
    data, ciudades, paises, total_matches = controller.req_4(control, nombre_torneo, fecha_inicial, fecha_final)

    if total_matches > 6:
        sublist = controller.get_first_last_three_list(data)
    else:
        sublist = data

    print(tabulate(sublist['elements'], headers='keys', tablefmt="grid"), '\n')
    print('Ciudades:', ciudades)
    print('Paises:',paises)


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    n_equipos = input('Ingrese el numero de equipos para la consulta: ')
    torneo = input('Ingrese el nombre del torneo: ')
    fecha_inicial = input("Ingrese la fecha inicial: ")
    fecha_final = input("Ingrese la fecha final: ")
    data = controller.req_6(control, n_equipos, torneo, fecha_final, fecha_final)
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


 # Se crea el controlador asociado a la vista
control = None
file_size = None
adt = None
sort = None

# main del reto
if __name__ == "__main__":
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
                file_size = choose_size()
            if adt == None:
                adt = choose_adt()
            if sort == None:
                sort = choose_sort()

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
            condition = int(input())
            if condition == 1:
                print_req_1(control, n_results, team_name, 'local')
            elif condition == 2:
                print_req_1(control, n_results, team_name, 'visitante')
            elif condition == 3:
                print_req_1(control, n_results, team_name, 'neutro')
            else:
                print("Por favor seleccione una opción válida")

        elif int(inputs) == 3:
            print_req_2(control)

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
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            file_size = choose_size()
            adt = choose_adt()
            sort = choose_sort()

            print('\n' + "-"*10 + 'Ejecuta la opción 1 para actualizar los cambios' + '-'*10 + '\n')

        elif int(inputs) == 10:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
