import os
import traceback
import matplotlib.pyplot as plot
import gc
import time

FILE = "V_Component_of_Wind_2021.csv"
DIRECTORY = "DATA"
FILE_PREFIX = "WIND_V_COMPONENT_2"
DESTINATION = "PREPROCESSED_DATA_1"

def LOAD_DATA() :
    global FILE, DIRECTORY
    global FIELDS
    global LOCATION_DATA
    global DESTINATION
    global FILE_PREFIX

    if not os.path.isdir(DESTINATION) :
        os.path.mkdir(DESTINATION)

    if not os.path.isdir(os.path.join(DESTINATION, FILE_PREFIX)) :
        os.mkdir(os.path.join(DESTINATION, FILE_PREFIX))
    DESTINATION = os.path.join(DESTINATION, FILE_PREFIX)

    file_handle = open(os.path.join(DIRECTORY, FILE), "r")
    fields = file_handle.readline()
    if fields[-1] == "\n" :
        fields = fields[:-1]
    fields = fields.split(",")

    FIELDS = []
    for _ in fields :
        FIELDS.append(_.upper())

    LOCATION_DATA = {}

    while True :
        try :
            line = file_handle.readline()
            if line == "" :
                break
            if line[-1] == "\n" :
                line = line[:-1]

            line_data = line.split(",")
            for _ in range(len(line_data)) :
                if "-" not in line_data[_] :
                    line_data[_] = eval(line_data[_])
                else :
                    num = ""
                    for __ in line_data[_] :
                        if __ != "-" and __ != ":" and __ != " " :
                            num += __
                    line_data[_] = eval(num)

            if tuple(line_data[1:3]) not in LOCATION_DATA :
                LOCATION_DATA[tuple(line_data[1:3])] = []
            LOCATION_DATA[tuple(line_data[1:3])].append([line_data[0], line_data[3]])

        except :
            traceback.print_exc()
            break

    print(list(LOCATION_DATA.keys()))

    for _ in range(10) :
        gc.collect()
        gc.set_threshold(0,0,0)
        time.sleep(1)

    # WRITING PREPROCESSED DATA TO CSV
    for _ in list(LOCATION_DATA.keys()) :
        file_handle = open(os.path.join(DESTINATION, FILE_PREFIX+str(_)+".csv"), "a")
        header = FIELDS[0]+","+FIELDS[3]
        header = header+"\n"
        file_handle.write(header)

        for __ in range(len(LOCATION_DATA[_])) :
            file_handle.write(str(LOCATION_DATA[_][__][0])+","+str(LOCATION_DATA[_][__][1])+"\n")
            file_handle.flush()
        file_handle.close()

if __name__ == "__main__" :
    LOAD_DATA()
