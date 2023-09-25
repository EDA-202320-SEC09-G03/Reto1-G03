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
from datetime import timedelta
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
        'scorers': None,
        'teams': None,
        'tournaments': None,
        'official_results': None,
        'official_teams': None
    }
    data_structs['results'] = lt.newList(datastructure=adt, cmpfunction=compare_id)
    data_structs['goalscorers'] = lt.newList(datastructure=adt, cmpfunction=compare_id)
    data_structs['shootouts'] = lt.newList(datastructure=adt, cmpfunction=compare_id)
    data_structs['scorers'] = lt.newList(datastructure=adt, cmpfunction=compare_name)
    data_structs['teams'] = lt.newList(datastructure=adt, cmpfunction=compare_name)
    data_structs['tournaments'] = lt.newList(datastructure=adt, cmpfunction=compare_name)
    data_structs['official_results'] = lt.newList(datastructure=adt, cmpfunction=compare_name)
    data_structs['official_teams'] = lt.newList(datastructure=adt, cmpfunction=compare_name)
    return data_structs


# Funciones para agregar informacion al modelo

def add_results(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista results
    """
    #TODO: Crear la función para agregar elementos a una lista
    lt.addLast(data_structs['results'], data)
    return data_structs

def add_goalscorers(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista goalscorers
    """
    #TODO: Crear la función para agregar elementos a una lista

    #Añadir a data_struct goalscorers
    lt.addLast(data_structs['goalscorers'], data)

    #Obtención de datos para buscar el partido que coincide en results
    date = data['date']
    hometeam = data['home_team'].lower()
    awayteam = data['away_team'].lower()

    #Posición del partido que coincide en results
    pos_result = binary_search_general(data_structs['results'], date, hometeam, awayteam)
    if pos_result != -1:

        #Cambio de datos según los obtenidos en goalscorers
        result = lt.getElement(data_structs['results'], pos_result)
        result['team'] = data['team']
        result['scorer'] = data['scorer']
        result['minute'] = data['minute']
        result['own_goal'] = data['own_goal']
        result['penalty'] = data['penalty']

        #Añadir la información en results
        lt.changeInfo(data_structs['results'], pos_result, result)
    return data_structs

def add_shootouts(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista shootouts
    """
    #TODO: Crear la función para agregar elementos a una lista

    #Añadir información al data_struct shootouts
    lt.addLast(data_structs['shootouts'], data)

    #Datos para encontrar el archivo que coincide en results
    date = data['date']
    hometeam = data['home_team'].lower()
    awayteam = data['away_team'].lower()

    #Posición del partido que coincide en results
    pos_result = binary_search_general(data_structs['results'], date, hometeam, awayteam)

    if pos_result != -1:
        result = lt.getElement(data_structs['results'], pos_result)
        result['winner'] = data['winner']

        #Actualizar la información en el data_struct results
        lt.changeInfo(data_structs['results'], pos_result, result)
    return data_structs

def load_auxiliar(data_structs, algorithm):
    """
    Función para crear las estructuras de datos auxiliares
    """
    #Recorrer cada linea de resultados para crear estructuras auxiliares
    for data in lt.iterator(data_structs['results']):

        #Partidos por goleador
        if data['scorer'] != 'Unknown':
            add_scorer(data_structs, data['scorer'], data)

        #Partidos por equipos
        add_teams(data_structs, data['home_team'], data)
        add_teams(data_structs, data['away_team'], data)

        #Partidos por torneos
        add_tournaments(data_structs, data['tournament'], data)

        #Solo resultados de partidos oficiales (no amistosos)
        if data['tournament'] != 'Friendly':
            add_officialresults(data_structs, data)
            add_official_teams(data_structs, data['home_team'], data)
            add_official_teams(data_structs, data['away_team'], data)

    #Ordenar estructuras auxiliares
    merg.sort(data_structs['scorers'], cmp_name)
    sort(data_structs, algorithm, 'teams')
    sort(data_structs, algorithm, 'tournaments')
    merg.sort(data_structs['official_results'], cmp_partidos_by_fecha_y_pais)
    merg.sort(data_structs['official_teams'], cmp_name)

def add_scorer(catalog, name, data):
    """
    Función para agregar nuevos elementos a la lista separada por goleadores
    """

    scorers = catalog['scorers']
    posscorer = lt.isPresent(scorers, name)
    if posscorer > 0:
        scorer = lt.getElement(scorers, posscorer)
    else:
        scorer = new_scorer(name)
        lt.addLast(scorers, scorer)

    lt.addLast(scorer['results'], data)
    return catalog

def add_teams(catalog, teamname, data):
    """
    Función para agregar nuevos elementos a la lista separada por equipos
    """

    teams = catalog['teams']
    posteam = lt.isPresent(teams, teamname)
    if posteam > 0:
        team = lt.getElement(teams, posteam)
    else:
        team = new_team(teamname)
        lt.addLast(teams, team)

    lt.addLast(team['results'], data)
    return catalog

def add_tournaments(data_structs, name, data):
    """
    Función para agregar nuevos elementos a la lista separada por torneos
    """

    tournaments = data_structs['tournaments']
    postournament = lt.isPresent(tournaments, name)
    if postournament > 0:
        tournament = lt.getElement(tournaments, postournament)
    else:
        tournament = new_tournament(name)
        lt.addLast(tournaments, tournament)
    lt.addLast(tournament['results'], data)

def add_officialresults(data_structs, data):
    lt.addLast(data_structs['official_results'], data)

def add_official_teams(data_structs, name, data):
    official_teams = data_structs['official_teams']
    posteam = lt.isPresent(official_teams, name)
    if posteam > 0:
        team = lt.getElement(official_teams, posteam)
    else:
        team = new_team(name)
        lt.addLast(official_teams, team)
    lt.addLast(team['results'], data)

# Funciones para creacion de datos

def new_scorer(name):
    """
    Crea una nueva estructura para modelar los datos por goleadores
    """
    scorer = {'name': '', 'results': None}
    scorer['name'] = name
    scorer['results'] = lt.newList('ARRAY_LIST')
    return scorer

def new_team(name):
    """
    Crea una nueva estructura para modelar los datos por equipos
    """
    team = {'name': '', 'results': None}
    team['name'] = name
    team['results'] = lt.newList('ARRAY_LIST')
    return team

def new_tournament(name):
    """
    Crea una nueva estructura para modelar los datos por torneos
    """
    tournament = {'name': '', 'results': None}
    tournament['name'] = name
    tournament['results'] = lt.newList('ARRAY_LIST')
    return tournament

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

def get_first_last_three(list):
    """
    Retorna una lista con los tres primeros y tres últimos elementos
    """
    filtered = lt.newList("ARRAY_LIST")
    for i in range(1, 4):
        lt.addLast(filtered, lt.getElement(list, i))
    for i in range(-2, 1):
        lt.addLast(filtered, lt.getElement(list, i))

    return filtered

def binary_search_general(data_structs, date, hometeam, awayteam):

    """
    Retorna la posición del partido en el que coinciden la fecha, el equipo local y el equipo visitante
    """

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

def binary_search_by_name(data_structs, name):
    """
    Busqueda binaria para encontrar un nombre en una lista
    """

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
    
    return -1

def binary_search_start_date(data_structs, start):
    """
    Busqueda binaria para encontrar una fecha de inicio
    """
    low = 1
    high = lt.size(data_structs)

    recent = (lt.firstElement(data_structs))['date']
    oldest = (lt.lastElement(data_structs))['date']
    i = lt.size(data_structs)

    #Confirmar que la fecha está en la lista
    if start >= oldest and start <= recent:

        #Buscar un día antes para evitar errores no encontrar la fecha mínima que coincide
        prev = start - timedelta(days=1)

        #Busqueda binaria
        while low <= high:
            mid = (low + high) // 2
            team = lt.getElement(data_structs, mid)
            mid_date = team['date']
            if mid_date == prev:
                i = mid
                pass
            elif mid_date > prev:
                low = mid + 1
            else:
                high = mid - 1
            
            if low == high:
                i = mid
            i = mid
                
        find = False
        #Iterar hacia atrás para encontrar la primera fecha que coincide
        while not find:
            result = lt.getElement(data_structs, i)
            date = result['date']
            if date >= start:
                return i
            else:
                i -= 1
            if i == 0:
                find = True
    else:
        return lt.size(data_structs)

def binary_search_end_date(data_structs, end):
    """
    Busqueda binaria para encontrar una fecha de final
    """
    low = 1
    high = lt.size(data_structs)

    recent = (lt.firstElement(data_structs))['date']
    oldest = (lt.lastElement(data_structs))['date']

    #Confirmar que la fecha está en la lista
    if end >= oldest and end <= recent:

        #Buscar un día después para evitar errores no encontrar la fecha máxima que coincide
        next = end + timedelta(days=1)

        next_id = None
        while low <= high:
            mid = (low + high) // 2
            team = lt.getElement(data_structs, mid)
            mid_date = team['date']
            if mid_date == next:
                next_id = mid
                pass

            elif mid_date > next:
                low = mid + 1
            else:
                high = mid - 1
            
            if low == high:
                next_id = mid
                pass
        
        find = False
        i = next_id

        #Iterar hacia adelante para encontrar la primera fecha que coincide
        while not find:
            date = (lt.getElement(data_structs, i))['date']
            if date <= end:
                return i
            else:
                i += 1
    else:
        return 1



def req_1(data_structs, n_results, team_name, condition):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    t_name = team_name.lower()

    #Estructura separada por equipos
    teams = data_structs['teams']

    #Busqueda binaria para encontrar el equipo que busca el usuario
    pos_team = binary_search_by_name(teams, t_name)

    #Solo los partidos del equipo
    team_data = (lt.getElement(data_structs['teams'], pos_team))['results']

    #Creación lista auxiliar
    filtered_list = lt.newList("ARRAY_LIST")

    #Filtrar búsqueda por condición
    for result in lt.iterator(team_data):
        if condition == "local":
            if t_name == result["home_team"].lower():
                lt.addLast(filtered_list, result)
        elif condition == "visitante":
            if t_name == result["away_team"].lower():
                lt.addLast(filtered_list, result)
        else:
            lt.addLast(filtered_list, result)

    #Filtrar ultimos N partidos
    sublist = lt.subList(filtered_list, 1, n_results)
    total = lt.size(filtered_list)
    
    return sublist, total



def req_2(data_structs, n_goals, name):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2

    #Filtrar los partidos del jugador
    scorers = data_structs['scorers']
    posscorer = binary_search_by_name(scorers, name)
    results = (lt.getElement(scorers, posscorer))['results']

    #Lista auxiliar
    goals = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compare_id)

    #Iteración hacia atrás para obtener de más antiguo a más reciente
    size = lt.size(results)
    for i in range(size, (size - n_goals) + 1, -1):
        if i < 1:
            #Caso en el que se llega al final de la lista
            return goals, lt.size(goals)
        else:
            result = lt.getElement(results, i)
            lt.addLast(goals, result)
    return None, -1


def req_3(data_structs, name, inicial, final):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3

    #Estructura separada por equipos
    teams = data_structs['teams']

    #Búsqueda del equipo deseado
    pos_team = binary_search_by_name(teams, name)
    results_team = (lt.getElement(teams, pos_team))['results']

    #Búsqueda de rangos de fechas
    pos_date_inicial = binary_search_start_date(results_team, inicial)
    pos_date_final = binary_search_end_date(results_team, final)

    #Iniciar contadores de local y visitante
    home = 0
    away = 0
    nlower = name.lower()

    #Sublista filtrada
    sublist = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compare_id)

    #Añadir resultados y sumar contadores
    for i in range(pos_date_final, pos_date_inicial + 1):

        result = lt.getElement(results_team, i)
        if result['home_team'].lower() == nlower:
            home += 1
        else:
            away +=1
        lt.addLast(sublist, result)
    
    return (sublist, home, away)

def req_4(control, nombre_torneo, fecha_inicial, fecha_final):
    """
    Función que soluciona el requerimiento 4
    """
    lista_results = control["model"]["results"]
    lista_shootouts = control["model"]["shootouts"]

    formato_fecha = "%Y-%m-%d"
    fecha_inicial = dt.strptime(fecha_inicial, formato_fecha)
    fecha_final = dt.strptime(fecha_final, formato_fecha)
    lista_final_results = lt.newList("ARRAY_LIST")
    lista_final_shootouts = lt.newList("ARRAY_LIST")

    for dato in lt.iterator(lista_results):
        fecha_dato = dato["date"]
        fecha_dato = dt.strptime(fecha_dato, formato_fecha)
        if fecha_dato <= fecha_final and fecha_dato >= fecha_inicial and dato["tournament"] == nombre_torneo:
            dato["winner"] = "Unknown"
            lt.addLast(lista_final_results, dato)

    for dato in lt.iterator(lista_shootouts):
        fecha_dato = dato["date"]
        fecha_dato = dt.strptime(fecha_dato, formato_fecha)
        if fecha_dato <= fecha_final and fecha_dato >= fecha_inicial :
            lt.addLast(lista_final_shootouts, dato)

    penaltis = 0
    for dato in lt.iterator(lista_final_shootouts):
        for dato_result in lt.iterator(lista_final_results):
            if dato["home_team"] == dato_result["home_team"] and dato["away_team"] == dato_result["away_team"]:
                penaltis += 1
                dato_result["winner"] = dato["winner"]

    lista_cities = lt.newList("ARRAY_LIST")
    lista_countries = lt.newList("ARRAY_LIST")
    for dato in lt.iterator(lista_final_results):
        ciudad_dato = dato["city"]
        pais_dato = dato["country"]
        if not lt.isPresent(lista_cities, ciudad_dato):
            lt.addLast(lista_cities, ciudad_dato)
        if not lt.isPresent(lista_countries, pais_dato):
            lt.addLast(lista_countries, pais_dato)

    num_ciudades = lt.size(lista_cities)
    num_paises = lt.size(lista_countries)
    total_matches = lt.size(lista_final_results)

    return lista_final_results, num_ciudades, num_paises, total_matches, penaltis
    


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs, n_equipos, torneo, fecha_inicial, fecha_final):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6

    #Data struct con la información separada por torneos
    tournaments = data_structs['tournaments']

    #Posiciones del torneo
    pos_tourn = binary_search_by_name(tournaments, torneo.lower())

    #Resultados en el torneo
    results = (lt.getElement(tournaments, pos_tourn))['results']

    #Posiciones para el rango de fechas
    pos_start = binary_search_start_date(results, fecha_inicial)
    pos_end = binary_search_end_date(results, fecha_final)


    #Listas auxiliares
    meetings = {'cities' : lt.newList('ARRAY_LIST', cmpfunction=compare_name), 'countries': lt.newList('ARRAY_LIST', cmpfunction=compare_name)}
    teams = lt.newList(datastructure="ARRAY_LIST", cmpfunction=compare_name)
    
    n_results = 0
    for i in range(pos_end, pos_start + 1):

        #Obtención de posición en teams y creación si no existe
        result = lt.getElement(results, i)
        poshome = add_team_req6(teams, result['home_team'])
        posaway = add_team_req6(teams, result['away_team'])
        
        #Cambiar la información con la nueva de la iteración
        changedhome = change_info_req6(teams, poshome, 'home', result)
        changedaway = change_info_req6(teams, posaway, 'away', result)
        
        #Añadir los cambios en teams
        lt.changeInfo(teams, poshome, changedhome)
        lt.changeInfo(teams, posaway, changedaway)

        #Contadores de paises y ciudades

        #Obtención de la posición y creación si no existe
        poscountry = lt.isPresent(meetings['countries'], result['country'])
        poscity = lt.isPresent(meetings['cities'], result['city'])

        if poscity > 0:
            city = lt.getElement(meetings['cities'], poscity)

        else:

            city = {'name': result['city'], 'meetings': 0}
            lt.addLast(meetings['cities'], city)
            poscity = lt.size(meetings['cities'])
        
        #Actualización de encuentros en esa ciudad
        city['meetings'] += 1

        #Añadir cambios a meetings en la sección de ciudades
        lt.changeInfo(meetings['cities'], poscity, city)

        #Lo mismo de arriba pero con paises
        if poscountry > 0:
            country = lt.getElement(meetings['countries'], poscountry)
        else:
            country = {'name': result['country'], 'meetings': 0}
            lt.addLast(meetings['countries'], country)
            poscountry = lt.size(meetings['countries'])
        country['meetings'] += 1
        lt.changeInfo(meetings['countries'], poscountry, country)
    
        n_results += 1

    #Ordenamiento de teams por orden de puntos
    sort(teams, 'merge', 'req6')
    #Ordenamiento de ciudades por cantidad de encuentros
    merg.sort(meetings['cities'], cmp_cities)

    #Tamaño de datos para devolver en el return
    n_teams = lt.size(teams)
    n_countries = lt.size(meetings['countries'])
    n_cities = lt.size(meetings['cities'])
    #Ciudad con más encuentros
    mostmatches = (lt.getElement(meetings['cities'], 1))['name']

    #Sublista con los N mejores equipos
    sublist = lt.subList(teams, 1, n_equipos)

    #Ciclo para obtener el mejor jugador en cada equipo
    for team in lt.iterator(sublist):

        if lt.size(team['scorers']) > 0:
            merg.sort(team['scorers'], cmp_top_scorer)
            team['top_scorer'] = lt.getElement(team['scorers'], 1)

    return sublist, n_teams, n_results, n_countries, n_cities, mostmatches

def add_team_req6(data_struct, name):
    posteam = lt.isPresent(data_struct, name)
    if posteam > 0:
        info = lt.getElement(data_struct, posteam)
    else:
        info = {
            'name': name,
            'total_points': 0,
            'penalty_points': 0,
            'matches': 0,
            'own_goal_points':0,
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'goals_for':0,
            'goals_against':0,
            'top_scorer': {'name': '', 'goals': 0, 'matches': 0, 'avg_time': 0, 'temp_time': 0},
            'scorers': lt.newList("ARRAY_LIST", cmpfunction=compare_name),
            'own_goals': 0,
            'goal_difference': 0
        }
        lt.addLast(data_struct, info)
        posteam = lt.size(data_struct)
    return posteam

def change_info_req6(data_struct, pos, condition, data):
    againstcondition = None
    if condition == 'home':
        againstcondition = 'away'
    else:
        againstcondition = 'home'
    changed = lt.getElement(data_struct, pos)
    name = data[(condition) + '_team']
    #Total points + Wins + Losses + Draws
    if data[(condition + '_score')] > data[(againstcondition + '_score')]:
        changed['total_points'] += 3
        changed['wins'] += 1
    elif data[(condition + '_score')] < data[(againstcondition + '_score')]:
        changed['losses'] += 1
    else:
        changed['total_points'] += 1
        changed['draws'] += 1
    #Goals for + Goals Against
    changed['goals_for'] += data[(condition) + '_score']
    changed['goals_against'] += data[(againstcondition) + '_score']
    #Penalty points
    if data['winner'] == name or (data['penalty'] == "True" and data['team'] == name):
        changed['penalty_points'] += 1
    #Matches
    changed['matches'] += 1
    #Own goal points
    if data['own_goal'] == 'True' and data['team'] == data[(againstcondition + '_team')]:
        changed['own_goal_points'] += 1
    else:
        changed['own_goals'] += 1
    #Goal difference
    changed['goal_difference'] = changed['goals_for'] - changed['goals_against']

    #Change Info Scorers
    if data['scorer'] != 'Unknown' and data['team'] == name:

        #Encontrar / crear el goleador
        scorers = changed['scorers']
        posscorer = lt.isPresent(scorers, data['scorer'])

        if posscorer > 0:
            infoscorer = lt.getElement(data_struct, posscorer)
        else:
            infoscorer = {'name': data['scorer'], 'goals': 0, 'matches': 0, 'avg_time': 0, 'temp_time': 0}
            lt.addLast(scorers, infoscorer)
            posscorer = lt.size(scorers)

        
        scorer = lt.getElement(scorers, posscorer)
        changedscorer = scorer
        changedscorer['matches'] += 1
        changedscorer['goals'] += 1
        changedscorer['temp_time'] += data['minute']
        changedscorer['avg_time'] = changedscorer['temp_time'] / changedscorer['matches']
        lt.changeInfo(scorers, posscorer, changedscorer)
    
    return changed

def req_7(data_structs, fecha_inicial, fecha_final, top_jugadores):
    """
    Función que soluciona el requerimiento 7
    """
   
    #Data_struct con solo torneos oficiales
    results = data_structs['official_results']

    #Encontrar rangos de fechas
    posstart = binary_search_start_date(results, fecha_inicial)
    posend = binary_search_end_date(results, fecha_final)

    #Creación de lista donde se guardará la información de cada scorer
    scorers = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compare_name)
    tournaments = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compare_name)
    
    num_partidos = 0
    num_goles = 0
    num_penales = 0
    num_autogoles = 0
    #Iterar solo en el rango de fechas
    for i in range(posend, posstart + 1):
        result = lt.getElement(results, i)
        if result['scorer'] != 'Unknown':

            posscorer = add_scorer_req7(scorers, result['scorer'])
            #Cambio de información en la iteración
            changed = change_info_scorer(scorers, posscorer, result)
            lt.changeInfo(scorers, posscorer, changed)

            #Cambiar datos
            num_partidos += 1
            num_goles += result['home_score'] + result['away_score']
            if result['penalty'] == 'True':
                num_penales += 1
            if result['own_goal'] == 'True':
                num_autogoles += 1
            
            #Añadir si es necesario el torneo para obtener el total de torneos
            postournament = lt.isPresent(tournaments, result['tournament'])
            if postournament != 0:
                lt.addLast(tournaments, {'name': result['tournament']})
    
    for scorer in lt.iterator(scorers):
        scorer

    merg.sort(scorers, cmp_scorer_points)
    sublist = lt.subList(scorers, 1, top_jugadores)

    num_jugadores = lt.size(scorers)
    num_tourns = lt.size(tournaments)

    return sublist, num_jugadores, num_partidos, num_goles, num_penales, num_autogoles, num_tourns

def add_scorer_req7(data_struct, name):
    posscorer = lt.isPresent(data_struct, name)
    if posscorer <= 0:
        #Esqueleto scorer desde 0
        scorer = {
            'name': name,
            'total_points': 0,
            'total_goals': 0,
            'penalty_goals':0,
            'own_goals': 0,
            'avg_time': 0,
            'total_time': 0,
            'total_tournaments': 0,
            'tournaments': lt.newList(datastructure='ARRAY_LIST', cmpfunction=compare_name),
            'scored_in_wins': 0,
            'scored_in_losses': 0,
            'scored_in_draws': 0,
            'last_goal': None,
        }
        lt.addLast(data_struct, scorer)
        posscorer = lt.size(data_struct)
    return posscorer

def change_info_scorer(data_struct, pos, data):
    changed = lt.getElement(data_struct, pos)

    #penalty_points
    if data['penalty'] == 'True':
        changed['penalty_goals'] += 1
    
    #own_goals
    if data['own_goal'] == 'True':
        changed['own_goals'] += 1
    
    #Comprobar si el goleador es del home_team o del away_team
    condition = None
    againstcondition = None
    if data['team'] == data['home_team']:
        condition = 'home'
        againstcondition = 'away'
    else:
        condition = 'away'
        againstcondition = 'home'

    #Scores in Wins - Draws - Losses
    selfscore = data[(condition) + '_score']
    againstscore = data[(againstcondition + '_score')]
    if selfscore > againstscore:
        changed['scored_in_wins'] += 1
    elif selfscore < againstscore:
        changed['scored_in_losses'] += 1
    else:
        changed['scored_in_draws'] += 1
    
    #Total goals
    changed['total_goals'] = changed['scored_in_wins'] + changed['scored_in_losses'] + changed['scored_in_draws']

    #Total points
    changed['total_points'] = changed['total_goals'] + changed['penalty_goals'] - changed['own_goals']

    #Avg time
    changed['total_time'] += data['minute']
    changed['avg_time'] = changed['total_time'] / changed['total_goals']

    #Total tournaments
    postournament = lt.isPresent(changed['tournaments'], data['tournament'])
    if postournament != 0:
        lt.addLast(changed['tournaments'], {'name': data['tournament']})
    changed['total_tournaments'] = lt.size(changed['tournaments'])

    #Last goal
    if changed['last_goal'] == None:
        changed['last_goal'] = data

    return changed

def req_8(data_structs, equipo1, equipo2, inicial, final):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    official_teams = data_structs['official_teams']
    
    sublist1, home1, away1 = req_3({'teams': official_teams}, equipo1, inicial, final)
    sublist2, home2, away2 = req_3({'teams': official_teams}, equipo2, inicial, final)

    years = {'team1': lt.newList('ARRAY_LIST', cmpfunction=compare_year), 'team2': lt.newList('ARRAY_LIST', cmpfunction=compare_year)}

    for result in lt.iterator(sublist1):
        year1 = result['date'].year
        pos_year1 = add_team_req6(years['team1'], year1)
        if result['home_team'].lower() == equipo1:
            condition = 'home'
        else:
            condition = 'away'
        changed = change_info_req6(years['team1'], pos_year1, condition, result)
        lt.changeInfo(years['team1'], pos_year1, changed)
    
    for result in lt.iterator(sublist2):
        year2 = result['date'].year
        pos_year2 = add_team_req6(years['team2'], year2)
        if result['home_team'].lower() == equipo2:
            condition = 'home'
        else:
            condition = 'away'
        changed = change_info_req6(years['team2'], pos_year2, condition, result)
        lt.changeInfo(years['team2'], pos_year2, changed)

    merg.sort(years['team1'], cmp_year)    
    merg.sort(years['team2'], cmp_year)
        
    for year in lt.iterator(years['team1']):

        if lt.size(year['scorers']) > 0:
            merg.sort(year['scorers'], cmp_top_scorer)
            year['top_scorer'] = lt.getElement(year['scorers'], 1)

    for year in lt.iterator(years['team2']):

        if lt.size(year['scorers']) > 0:
            merg.sort(year['scorers'], cmp_top_scorer)
            year['top_scorer'] = lt.getElement(year['scorers'], 1)

    return years
    



# Funciones utilizadas para comparar elementos dentro de una lista

def compare_id(data_1, data_2):
    """
    Función encargada de comparar dos datos por id
    """
    #TODO: Crear función comparadora de la lista
    if data_1['id'] > data_2['id']:
        return 1
    elif data_1['id'] < data_2['id']:
        return -1
    else:
        return 0
    
def compare_name(team1, team2):
    """
    Función encargada de comparar dos datos por nombre
    """
    t1 = team1.lower()
    t2 = team2['name'].lower()

    if t1 > t2:
        return 1
    elif t1 < t2:
        return -1
    else:
        return 0

def compare_year(data1, data2):
    if data1 > data2['name']:
        return 1
    elif data1 < data2['name']:
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

def cmp_name(team1, team2):

    t1 = team1['name'].lower()
    t2 = team2['name'].lower()

    if t1 < t2:
        return True
    else:
        return False
    
def cmp_stats(team1, team2):
    points1 = team1['total_points']
    points2 = team2['total_points']

    if points1 > points2:
        return True
    elif points1 < points2:
        return False
    else:
        difgoals1 = team1['goal_difference']
        difgoals2 = team2['goal_difference']
        if difgoals1 > difgoals2:
            return True
        elif difgoals1 < difgoals2:
            return False
        else:
            penaltgoals1 = team1['penalty_points']
            penaltygoals2 = team2['penalty_points']
            if penaltgoals1 > penaltygoals2:
                return True
            elif penaltgoals1 < penaltygoals2:
                return False
            else:
                matches1 = team1['matches']
                matches2 = team2['matches']
                if matches1 < matches2:
                    return True
                elif matches1 > matches2:
                    return False
                else:
                    owngoals1 = team1['own_goals']
                    owngoals2 = team2['own_goals']
                    if owngoals1 < owngoals2:
                        return True
                    else:
                        return False
                    
def cmp_top_scorer(scorer1, scorer2):
    if scorer1['goals'] > scorer2['goals']:
        return True
    elif scorer1['goals'] < scorer2['goals']:
        return False
    else:
        if scorer1['avg_time'] < scorer2['avg_time']:
            return True
        elif scorer1['avg_time'] > scorer2['avg_time']:
            return False
        else:
            if scorer1['name']  < scorer2['name']:
                return True
            else:
                return False
    
def cmp_cities(city1, city2):
    if city1['meetings'] > city2['meetings']:
        return True
    elif city1['meetings'] < city2['meetings']:
        return False
    else:
        if city1['name'] < city2['name']:
            return True
        else:
            return False

def cmp_scorer_points(scorer1, scorer2):
    if scorer1['total_points'] > scorer2['total_points']:
        return True
    elif scorer1['total_points'] < scorer2['total_points']:
        return False
    else:
        if scorer1['total_goals'] > scorer2['total_goals']:
            return True
        elif scorer1['total_goals'] < scorer2['total_goals']:
            return False
        else:
            if scorer1['penalty_goals'] > scorer2['penalty_goals']:
                return True
            elif scorer1['penalty_goals'] < scorer2['penalty_goals']:
                return False
            else:
                if scorer1['own_goals'] < scorer2['own_goals']:
                    return True
                elif scorer1['own_goals'] > scorer2['own_goals']:
                    return False
                else:
                    if scorer1['avg_time'] < scorer2['avg_time']:
                        return True
                    elif scorer1['avg_time'] > scorer2['avg_time']:
                        return False
                    else:
                        if scorer1['name'] < scorer2['name']:
                            return True
                        else:
                            return False                    

def cmp_year(year1, year2):
    if year1['name'] > year2['name']:
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
            sort_algorithm(data_structs['teams'], cmp_name)
        elif file == 'tournaments':
            sort_algorithm(data_structs['tournaments'], cmp_name)
        elif file == 'req6':
            sort_algorithm(data_structs, cmp_stats)
        