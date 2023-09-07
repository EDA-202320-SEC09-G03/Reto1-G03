"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import time
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {
        'model': None
    }
    control['model'] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    data_structs = control['model']

    results = load_results(data_structs)
    goalscorers = load_goalscorers(data_structs)
    shootouts = load_shootouts(data_structs)

    sort_results(data_structs)
    sort_goalscorers(data_structs)
    sort_shootouts(data_structs)

    return results, goalscorers, shootouts

def load_results(data_structs):

    results_file = cf.data_dir + 'football/results-utf8-small.csv'
    input_file = csv.DictReader(open(results_file, encoding='utf-8'))

    for result in input_file:
        model.add_data(data_structs, result, 'results')

    return model.data_size(data_structs, 'results')

def load_goalscorers(data_structs):

    goalscorers_file = cf.data_dir + 'football/goalscorers-utf8-small.csv'
    input_file = csv.DictReader(open(goalscorers_file, encoding='utf-8'))

    for goalscorer in input_file:
        model.add_data(data_structs, goalscorer, 'goalscorers')

    return model.data_size(data_structs, 'goalscorers')

def load_shootouts(data_structs):

    shootouts_file = cf.data_dir + 'football/shootouts-utf8-small.csv'
    input_file = csv.DictReader(open(shootouts_file, encoding='utf-8'))

    for shootout in input_file:
        model.add_data(data_structs, shootout, 'shootouts')

    return model.data_size(data_structs, 'shootouts')


# Funciones de ordenamiento

def sort_results(data_structs):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    model.sort_results(data_structs)

def sort_goalscorers(data_structs):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    model.sort_goalscorers(data_structs)

def sort_shootouts(data_structs):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    model.sort_shootouts(data_structs)

# Funciones de consulta sobre el catálogo

def get_data(control, file, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    data = model.get_data(control['model'], file, id)
    return data


def req_1(control, team_name, condition):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    filtered_list = model.req_1(control['model'], team_name, condition)
    lt_size = model.lt.size(filtered_list)
    return filtered_list, lt_size


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass

def get_first_last_three_datastructs(control, file):
    data = model.get_first_last_three_datastructs(control['model'], file)
    return data

def get_first_last_three_list(list):
    data = model.get_first_last_three_list(list)
    return data


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
