import numpy as np
from os import listdir
from os.path import isfile, join
import pandas as pd
import matplotlib.pyplot as plt
from FFClust import IOFibers
import os

MIN_LENGTH = 10 #mm
POINTS_PER_FIBER = 21

def get_list_of_files(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    dirs = [f for f in listdir(directory) if not isfile(join(directory, f))]
    return files, dirs

directory = '/home/cocobio/Documents/ARCHI_Database/'
fiber_dir = '/OverSampledFibers/'
files, subjects = get_list_of_files(directory)
subjects.sort()
fiber_data = []
distance = []
n_fibers = []

for subject in subjects:
    print('Processing', subject)
    subject_fibers_path = directory + subject + fiber_dir
    fibers, tmp = get_list_of_files(subject_fibers_path)
    del tmp
    fibers = [f for f in fibers if f.endswith('.bundles')]
    for f_path in fibers:
        f = subject_fibers_path + f_path

        # Eliminamos las fibras muy pequenias
        f_filtered = f[:f.find('.bundles')]+"_filtered_under_"+str(MIN_LENGTH)+f[f.find('.bundles'):]
        # print(    "python3 filtering/filtering.py "+f+" "+f_filtered+" "+str(MIN_LENGTH))
        os.system("python3 filtering/filtering.py "+f+" "+f_filtered+" "+str(MIN_LENGTH))

        f = f_filtered

        # Resampling a 21 puntos
        output_f = f[:f.find('.bundles')]+"_filtered_to_"+str(POINTS_PER_FIBER)+f[f.find('.bundles'):]
        # print(    "./resampling/resampling "+f+" "+output_f+" "+str(POINTS_PER_FIBER))
        os.system("./resampling/resampling "+f+" "+output_f+" "+str(POINTS_PER_FIBER))

        # Borramos el archivo con los datos filtrados, de esta forma solo queda el filtrado y resampleado
        os.system("rm "+f)
        os.system("rm "+f+"data")
        
    #     break
    # break