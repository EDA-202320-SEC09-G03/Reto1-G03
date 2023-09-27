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
from datetime import datetime


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller(adt):
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {
        'model': None
    }
    control['model'] = model.new_data_structs(adt)
    return control


# Funciones para la carga de datos

def load_data(control, file_size, algorithm):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    data_structs = control['model']

    results = load_results(data_structs, file_size)
    d_time1 = sort(control, algorithm, 'results')
    goalscorers = load_goalscorers(data_structs, file_size)
    d_time2 = sort(control, algorithm, 'goalscorers')
    shootouts = load_shootouts(data_structs, file_size)
    d_time3 = sort(control, algorithm, 'shootouts')
    model.load_auxiliar(data_structs, algorithm)

    return (results, goalscorers, shootouts, (d_time1 + d_time2 + d_time3))

def load_results(data_structs, file_size):

    results_file = cf.data_dir + 'football/results-utf8-' + file_size + '.csv'
    input_file = csv.DictReader(open(results_file, encoding='utf-8'))

    id = 1
    for result in input_file:

        changed = change_type(result)
        changed['id'] = id
        changed['scorers'] = 'Unknown'
        changed['winner'] = 'Unknown'
        changed['penalty'] = 'Unknown'
        changed['own_goal'] = 'Unknown'
        model.add_results(data_structs, changed)
        id += 1

    return model.data_size(data_structs, 'results')

def load_goalscorers(data_structs, file_size):

    goalscorers_file = cf.data_dir + 'football/goalscorers-utf8-' + file_size + '.csv'
    input_file = csv.DictReader(open(goalscorers_file, encoding='utf-8'))

    id = 1
    for goalscorer in input_file:
        
        if goalscorer['minute'] == "" or goalscorer['minute'] == None:
            goalscorer['minute'] = -1
        changed = change_type(goalscorer)
        changed['id'] = id
        model.add_goalscorers(data_structs, changed)
        id += 1

    return model.data_size(data_structs, 'goalscorers')

def load_shootouts(data_structs, file_size):

    shootouts_file = cf.data_dir + 'football/shootouts-utf8-' + file_size + '.csv'
    input_file = csv.DictReader(open(shootouts_file, encoding='utf-8'))

    id = 1
    for shootout in input_file:

        changed = change_type(shootout)
        changed['id'] = id
        model.add_shootouts(data_structs, changed)
        id += 1

    return model.data_size(data_structs, 'shootouts')

def change_type(data):

    changed = data
    formato_fecha = "%Y-%m-%d"
    changed['date'] = datetime.strptime(data['date'], formato_fecha)
    if changed.get('home_score'):
        changed['home_score'] = int(data['home_score']) 
        changed['away_score'] = int(data['away_score'])
        
    if changed.get('scorer'):
        if changed['minute'] != 'Unknown':
            changed['minute'] = float(data['minute'])
    
    return changed


# Funciones de ordenamiento

def sort(control, algorithm, file):
    data_structs = control['model']
    start_time = get_time()
    model.sort(data_structs, algorithm, file)
    end_time = get_time()
    d_time = delta_time(start_time, end_time)

    return d_time

# Funciones de consulta sobre el catálogo

def get_data(control, file, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    data = model.get_data(control['model'], file, id)
    return data


def req_1(control, n_results, team_name, condition):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = get_time()
    filtered_list, total = model.req_1(control['model'], n_results, team_name, condition)
    end_time = get_time()
    d_time = delta_time(start_time, end_time)
    return filtered_list, total, d_time


def req_2(control, n_goals, name):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    nlower = name.lower()
    start_time = get_time()
    data, total = model.req_2(control['model'], n_goals, nlower)
    end_time = get_time()
    d_time = delta_time(start_time, end_time)
    return data, total, d_time


def req_3(control, name, inicial, final):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    name = name.lower()
    formato_fecha = "%Y-%m-%d"
    inicial = datetime.strptime(inicial, formato_fecha)
    final = datetime.strptime(final, formato_fecha)
    start_time = get_time()
    if final >= inicial:
        filtered_list, home, away = model.req_3(control['model'], name, inicial, final)
        lt_size = model.lt.size(filtered_list)
        end_time = get_time()
        d_time = delta_time(start_time, end_time)
        return filtered_list, lt_size, home, away, d_time
    else:
        end_time = get_time()
        d_time = delta_time(start_time, end_time)
        return (None, 0, 0, 0, d_time)


def req_4(control, nombre_torneo, fecha_inicial, fecha_final ):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    formato_fecha = "%Y-%m-%d"
    inicial = datetime.strptime(fecha_inicial, formato_fecha)
    final = datetime.strptime(fecha_final, formato_fecha)
    start_time = get_time()
    if final >= inicial:
        data, ciudades, paises, total_matches, penaltis = model.req_4(control, nombre_torneo, inicial, final)
        end_time = get_time()
        d_time = delta_time(start_time, end_time)
    return data, ciudades, paises, total_matches, penaltis, d_time
     


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control, n_equipos, torneo, fecha_inicial, fecha_final):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    formato_fecha = "%Y-%m-%d"
    inicial = datetime.strptime(fecha_inicial, formato_fecha)
    final = datetime.strptime(fecha_final, formato_fecha)
    start_time = get_time()
    data, n_teams, n_results, n_countries, n_cities, mostmatches = model.req_6(control['model'], n_equipos, torneo, inicial, final)
    end_time = get_time()
    d_time = delta_time(start_time, end_time)
    return data, n_teams, n_results, n_countries, n_cities, mostmatches, d_time


def req_7(control, fecha_inicial, fecha_final, top_jugadores):
    """
    Retorna el resultado del requerimiento 7
    """
    formato_fecha = "%Y-%m-%d"
    inicial = datetime.strptime(fecha_inicial, formato_fecha)
    final = datetime.strptime(fecha_final, formato_fecha)
    start_time = get_time()
    sublist, num_jugadores, num_partidos, num_goles, num_penales, num_autogoles, num_tourns = model.req_7(control['model'], inicial, final, top_jugadores)
    end_time = get_time()
    d_time = delta_time(start_time, end_time)
    return sublist, num_jugadores, num_partidos, num_goles, num_penales, num_autogoles, num_tourns, d_time
    


def req_8(control, equipo1, equipo2, fecha_inicial, fecha_final):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    formato_fecha = "%Y-%m-%d"
    inicial = datetime.strptime(fecha_inicial, formato_fecha)
    final = datetime.strptime(fecha_final, formato_fecha)
    equipo1 = equipo1.lower()
    equipo2 = equipo2.lower()
    start_time = get_time()
    data, common, new1, new2, nc, infot1, infot2, infocommon = model.req_8(control['model'], equipo1, equipo2, inicial, final)
    end_time = get_time()
    d_time = delta_time(start_time, end_time)
    return data, common, new1, new2, nc,infot1, infot2, infocommon, d_time
    

def get_first_last_three(list):
    data = model.get_first_last_three(list)
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
