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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from datetime import datetime as dt
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs(adt):
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    data_structs = {
        'results': None,
        'goalscorers': None,
        'shootouts': None,
        'teams': None,
        'tournaments': None
    }
    data_structs['results'] = lt.newList(datastructure=adt, cmpfunction=compare_id)
    data_structs['goalscorers'] = lt.newList(datastructure=adt, cmpfunction=compare_id)
    data_structs['shootouts'] = lt.newList(datastructure=adt, cmpfunction=compare_id)
    data_structs['teams'] = lt.newList(datastructure=adt, cmpfunction=compare_team)
    data_structs['tournaments'] = lt.newList(datastructure=adt, cmpfunction=compare_team)
    return data_structs


# Funciones para agregar informacion al modelo

def add_results(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    lt.addLast(data_structs['results'], data)
    return data_structs

def add_goalscorers(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    lt.addLast(data_structs['goalscorers'], data)
    date = data['date']
    hometeam = data['home_team'].lower()
    awayteam = data['away_team'].lower()
    pos_result = binary_search_general(data_structs['results'], date, hometeam, awayteam)
    if pos_result != -1:
        result = lt.getElement(data_structs['results'], pos_result)
        result['team'] = data['team']
        result['scorer'] = data['scorer']
        result['minute'] = data['minute']
        result['own_goal'] = data['own_goal']
        result['penalty'] = data['penalty']
        lt.changeInfo(data_structs['results'], pos_result, result)
    return data_structs

def add_shootouts(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    lt.addLast(data_structs['shootouts'], data)
    date = data['date']
    hometeam = data['home_team'].lower()
    awayteam = data['away_team'].lower()
    pos_result = binary_search_general(data_structs['results'], date, hometeam, awayteam)
    if pos_result != -1:
        result = lt.getElement(data_structs['results'], pos_result)
        result['winner'] = data['winner']
        lt.changeInfo(data_structs['results'], pos_result, result)
    return data_structs

def load_auxiliar(data_structs, algorithm):
    for data in lt.iterator(data_structs['results']):
        add_teams(data_structs, data['home_team'], data)
        add_teams(data_structs, data['away_team'], data)
        add_tournaments(data_structs, data['tournament'], data)
    sort(data_structs, algorithm, 'teams')
    sort(data_structs, algorithm, 'tournaments')

def add_teams(data_structs, teamname, data):
    teams = data_structs['teams']
    posteam = lt.isPresent(teams, teamname)
    if posteam > 0:
        team = lt.getElement(teams, posteam)
    else:
        team = new_team(teamname)
        lt.addLast(teams, team)

    lt.addLast(team['results'], data)
    return data_structs

def add_tournaments(data_structs, name, data):
    tournaments = data_structs['tournaments']
    postournament = lt.isPresent(tournaments, name)
    if postournament > 0:
        tournament = lt.getElement(tournaments, postournament)
    else:
        tournament = new_tournament(name)
        lt.addLast(tournaments, tournament)
    lt.addLast(tournament['results'], data)

# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

def new_team(name):
    team = {'name': '', 'results': None}
    team['name'] = name
    team['results'] = lt.newList('ARRAY_LIST')
    return team

def new_tournament(name):
    tournament = {'name': '', 'results': None}
    tournament['name'] = name
    tournament['results'] = lt.newList('ARRAY_LIST')
    return tournament

def new_scorrer(name):
    scorrer = {'name': '', 'results': None}
    scorrer['name'] = name
    scorrer['results'] = lt.newList('ARRAY_LIST')
    return scorrer



# Funciones de consulta

def get_data(data_structs, file, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    return lt.getElement(data_structs[file], id)


def data_size(data_structs, file):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    return lt.size(data_structs[file])

def get_first_last_three_datastructs(data_structs, file):
    filtered = lt.newList("ARRAY_LIST")
    for i in range(1, 4):
        lt.addLast(filtered, get_data(data_structs, file, i))
    size = data_size(data_structs, file)
    for i in range((size - 2), size + 1):
        lt.addLast(filtered, get_data(data_structs, file, i))

    return filtered

def get_first_last_three_list(list):
    filtered = lt.newList("ARRAY_LIST")
    for i in range(1, 4):
        lt.addLast(filtered, lt.getElement(list, i))
    for i in range(-2, 1):
        lt.addLast(filtered, lt.getElement(list, i))

    return filtered

def binary_search_general(data_structs, date, hometeam, awayteam):
    low = 1
    high = lt.size(data_structs)

    while low <= high:
        mid = (low + high) // 2
        result = lt.getElement(data_structs, mid)
        datemid = result['date']
        if datemid < date:
            high = mid -1
        elif datemid > date:
            low = mid + 1
        else:
            hometeam_mid = result['home_team'].lower()
            if hometeam_mid < hometeam:
                high = mid - 1
            elif hometeam_mid > hometeam:
                low = mid + 1
            else:
                awayteam_mid = result['away_team'].lower()
                if awayteam_mid < awayteam:
                    high = mid + 1
                elif awayteam_mid > awayteam:
                    low = mid + 1
                else:
                    return mid
    return -1

def binary_search_team(data_structs, name):
    low = 1
    high = lt.size(data_structs)

    while low <= high:
        mid = (low + high) // 2
        team = lt.getElement(data_structs, mid)
        mid_name = team['name'].lower()
        if mid_name == name:
            return mid
        elif mid_name < name:
            low = mid + 1
        else:
            high = mid - 1

def find_pos_start_date(data_structs, start):
    for i in range(lt.size(data_structs), 0, -1):
        data = lt.getElement(data_structs, i)
        if data['date'] >= start:
            return i
    return -1
def find_pos_finish_date(data_structs, finish):
    for i in range(1, lt.size(data_structs)):
        data = lt.getElement(data_structs, i)
        if data['date'] <= finish:
            return i
    return -1


def req_1(data_structs, team_name, condition):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    t_name = team_name.lower()
    results = data_structs["results"]
    filtered_list = lt.newList("ARRAY_LIST")

    for result in lt.iterator(results):
        if condition == "local":
            if t_name == result["home_team"].lower():
                lt.addLast(filtered_list, result)

        elif condition == "visitante":
            if t_name == result["away_team"].lower():
                lt.addLast(filtered_list, result)
        elif condition == "neutro":
            if (t_name == result["away_team"].lower()) or (t_name == result["home_team"].lower()):
                lt.addLast(filtered_list, result)
    
    return filtered_list



def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs, name, inicial, final):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    teams = data_structs['teams']

    pos_team = binary_search_team(teams, name)
    results_team = lt.getElement(teams, pos_team)

    pos_date_inicial = find_pos_start_date(results_team['results'], inicial)
    pos_date_final = find_pos_finish_date(results_team['results'], final)
    size = (pos_date_inicial - pos_date_final) + 1
    sublist = lt.subList(results_team['results'], pos_date_final, size)

    home = 0
    away = 0
    nlower = name.lower()
    for result in lt.iterator(sublist):
        if result['home_team'].lower() == nlower:
            home += 1
        else:
            away +=1
    
    return (sublist, home, away)

def req_4(control, nombre_torneo, fecha_inicial, fecha_final):
    """
    Función que soluciona el requerimiento 4
    """
    lista_results = control["model"]["results"]
    formato_fecha = "%Y-%m-%d"
    fecha_inicial = dt.strptime(fecha_inicial, formato_fecha)
    fecha_final = dt.strptime(fecha_final, formato_fecha)
    lista_final = lt.newList("ARRAY_LIST")

    for dato in lt.iterator(lista_results):
        fecha_dato = dato["date"]
        fecha_dato = dt.strptime(fecha_dato, formato_fecha)
        if fecha_dato <= fecha_final and fecha_dato >= fecha_inicial and dato["tournament"] == nombre_torneo:
            lt.addLast(lista_final, dato)

    lista_cities = lt.newList("ARRAY_LIST")
    lista_countries = lt.newList("ARRAY_LIST")
    for dato in lt.iterator(lista_final):
        ciudad_dato = dato["city"]
        pais_dato = dato["country"]
        if not lt.isPresent(lista_cities, ciudad_dato):
            lt.addLast(lista_cities, ciudad_dato)
        if not lt.isPresent(lista_countries, pais_dato):
            lt.addLast(lista_countries, pais_dato)

    num_ciudades = lt.size(lista_cities)
    num_paises = lt.size(lista_countries)
    total_matches = lt.size(lista_final)

    return lista_final, num_ciudades, num_paises, total_matches
    


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare_id(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    if data_1['id'] > data_2['id']:
        return 1
    elif data_1['id'] < data_2['id']:
        return -1
    else:
        return 0
    
def compare_team(team1, team2):
    t1 = team1.lower()
    t2 = team2['name'].lower()

    if t1 > t2:
        return 1
    elif t1 < t2:
        return -1
    else:
        return 0

# Funciones de ordenamiento


def cmp_partidos_by_fecha_y_pais(result1, result2):
    """
    Devuelve verdadero (True) si la fecha del resultado1 es menor que en el resultado2,
    en caso de que sean iguales tenga el nombre de la ciudad en que se disputó el partido,
    de lo contrario devuelva falso (False).
    Args:
    result1: información del primer registro de resultados FIFA que incluye 
    “date” y el “country” 
    result2: información del segundo registro de resultados FIFA que incluye 
    “date” y el “country” 
    """
    #TODO: Crear función comparadora para ordenar
    fecha1 = result1['date']
    fecha2 = result2['date']

    if fecha1 > fecha2:
        return True
    elif fecha1 < fecha2:
        return False
    else:
        hscore1 = result1['home_score']
        hscore2 = result2['home_score']

        if hscore1 > hscore2:
            return True
        elif hscore1 < hscore2:
            return False
        else:
            ascore1 = result1['away_score']
            ascore2 = result2['away_score']
            if ascore1 > ascore2:
                return True
            else: 
                return False

def cmp_goalscorers(scorer1, scorer2):

    fecha1 = scorer1['date']
    fecha2 = scorer2['date']

    if fecha1 > fecha2:
        return True
    elif fecha1 < fecha2:
        return False
    else:
        min1 = (scorer1['minute'])
        min2 = (scorer2['minute'])

        if min1 > min2:
            return True
        elif min1 < min2:
            return False
        else:
            player1 = scorer1['scorer'].lower()
            player2 = scorer2['scorer'].lower()
            if player1 > player2:
                return True
            else:
                return False

def cmp_shootouts(shoot1, shoot2):

    fecha1 = shoot1["date"]
    fecha2 = shoot2["date"]

    if fecha1 > fecha2:
        return True
    elif fecha1 < fecha2:
        return False
        
    else: 
        nombre_1_local = shoot1["home_team"].lower()
        nombre_2_local = shoot2["home_team"].lower()

        if nombre_1_local > nombre_2_local:
            return True
        elif nombre_1_local < nombre_1_local:
            return False
        
        else:
            nombre_1_visitante = shoot1["away_team"].lower()
            nombre_2_visitante = shoot2["away_team"].lower()

            if nombre_1_visitante > nombre_2_visitante:
                return True
            elif nombre_1_visitante < nombre_1_visitante:
                return False

def cmp_teams(team1, team2):

    t1 = team1['name'].lower()
    t2 = team2['name'].lower()

    if t1 < t2:
        return True
    else:
        return False
        
def sort(data_structs, algorithm, file):
    sort_algorithms = {
        'shell': sa.sort,
        'insertion': ins.sort,
        'selection': se.sort,
        'merge': merg.sort,
        'quick': quk.sort,
    }

    sort_algorithm = sort_algorithms.get(algorithm)

    if sort_algorithm:
        if file == 'results':
            sort_algorithm(data_structs['results'], cmp_partidos_by_fecha_y_pais)
        elif file == 'goalscorers':
            sort_algorithm(data_structs['goalscorers'], cmp_goalscorers)
        elif file == 'shootouts':
            sort_algorithm(data_structs['shootouts'], cmp_shootouts)
        elif file == 'teams':
            sort_algorithm(data_structs['teams'], cmp_teams)
            for team in lt.iterator(data_structs['teams']):
                sort_algorithm(team['results'], cmp_partidos_by_fecha_y_pais)
        elif file == 'tournaments':
            sort_algorithm(data_structs['tournaments'], cmp_teams)