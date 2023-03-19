import os
import traceback
import matplotlib.pyplot as plot
import gc
import time
import threading

DIRECTORY = "PREPROCESSED_DATA_1"

FILE_PREFIXES = ["TOTAL_PRECIPITATION", "HUMIDITY", "SURFACE_PRESSURE",
                 "SEA_LEVEL_PRESSURE", "TEMPERATURE", "VISIBILITY",
                 "WIND_U_COMPONENT", "WIND_V_COMPONENT",
                 "WIND_U_COMPONENT_2", "WIND_V_COMPONENT_2"]

DESTINATION = "PREPROCESSED_DATA_2"

MAX_THREADS = 16

def MERGE_DATA(location) :

    global DIRECTORY
    global DESTINATION
    global FILE_PREFIXES

    location_data = {}

    file_handle = open(os.path.join(DIRECTORY, FILE_PREFIXES[0], FILE_PREFIXES[0]+str(location)+".csv"), "r")
    file_handle.readline()
    while True :
        line = file_handle.readline()
        if line != "" :
            if line[-1] == "\n" :
                line = line[:-1]
            line_data = line.split(",")
            line_data[0] = eval(line_data[0])
            line_data[1] = eval(line_data[1])
            if line_data[0] not in location_data :
                location_data[line_data[0]] = {}
                for _ in range(len(FILE_PREFIXES)) :
                    location_data[line_data[0]][_] = 0
                    #location_data[line_data[0]][_] = None
        else :
            break
    file_handle.close()

    for _ in range(len(FILE_PREFIXES)) :
        file_handle = open(os.path.join(DIRECTORY, FILE_PREFIXES[_], FILE_PREFIXES[_]+str(location)+".csv"), "r")
        file_handle.readline()
        while True :
            line = file_handle.readline()
            if line != "" :
                if line[-1] == "\n" :
                    line = line[:-1]
                line_data = line.split(",")
                line_data[0] = eval(line_data[0])
                line_data[1] = eval(line_data[1])
                if line_data[0] in location_data :
                    location_data[line_data[0]][_] = line_data[1]
            else :
                break
        file_handle.close()

    # WRITING O/P to new location

    file_handle = open(os.path.join(DESTINATION, str(location)+".csv"), "a")
    header = "TIME,"
    for _ in FILE_PREFIXES :
        header += _+","
    header = header[:-1]
    header += "\n"
    file_handle.write(header)

    for _ in list(location_data.keys()) :
        valid_data = True
        for __ in list(location_data[_].keys()) :
            if location_data[_][__] == None :
                valid_data = False
                break

        if valid_data :
            data = str(_)+","
            for __ in range(len(FILE_PREFIXES)) :
                data += str(location_data[_][__])+","
            data = data[:-1]
            data += "\n"
            file_handle.write(data)

def CREATE_DIRS() :
    if not os.path.isdir(DESTINATION) :
        os.mkdir(DESTINATION)

def LOAD_LOCATIONS() :
    global LOCATIONS

    temp = open("locations.txt", "r")
    LOCATIONS = eval(temp.read())
    temp.close()

def PRE_PROCESS() :
    global LOCATIONS

    CREATE_DIRS()
    LOAD_LOCATIONS()

    thread_pool = []

    n_th_being_processed = 1
    total = len(LOCATIONS)

    while LOCATIONS != [] :
        thread_pool = []
        for _ in range(MAX_THREADS) :
            if LOCATIONS != [] :
                location = LOCATIONS.pop(0)
                thread_pool.append(threading.Thread(target=MERGE_DATA, args=(location,)))
                print("[$] PROCESSING {0: 5} OUT OF {1: 5} : {2}".format(n_th_being_processed, total, location))
                n_th_being_processed += 1
            else :
                break
        for _ in thread_pool :
            _.start()
        for _ in thread_pool :
            _.join()


if __name__ == "__main__" :
    PRE_PROCESS()
