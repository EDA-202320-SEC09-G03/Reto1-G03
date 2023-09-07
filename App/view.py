﻿"""
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

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
   
    control = controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    results, goalscorers, shootouts = controller.load_data(control)

    print("Primeros y ultimos 3 resultados: \n")

    file1 = 'results'
    table_results = controller.get_first_last_three_datastructs(control, file1)
    print(tabulate(table_results['elements'], headers="keys", tablefmt="grid"), "\n")

    print("Primeros y ultimos 3 anotadores: \n")

    file2 = "goalscorers"
    table_goalscorers = controller.get_first_last_three_datastructs(control, file2)
    print(tabulate(table_goalscorers['elements'], headers="keys", tablefmt="grid"), "\n")

    print("Primeros y ultimos 3 goles:\n")

    file3 = "shootouts"
    table_shootouts = controller.get_first_last_three_datastructs(control, file3)
    print(tabulate(table_shootouts['elements'], headers="keys", tablefmt="grid"), "\n")
    
    return results, goalscorers, shootouts


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

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


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


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
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            rsize, gsize, ssize = load_data(control)
            print('Total de encuentros cargados: ' + str(rsize))
            print('Total de anotaciones cargadas: ' + str(gsize))
            print('Total de goles marcados desde el punto penal cargados: ' + str(ssize))
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
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
