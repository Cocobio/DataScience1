import numpy as np
from os import listdir
from os.path import isfile, join
from FFClust import IOFibers
import os
import pandas as pd

def get_list_of_files(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    dirs = [f for f in listdir(directory) if not isfile(join(directory, f))]
    return files, dirs

# directory = '/home/cocobio/Documents/ARCHI_Database/'
directory = 'D:/Codes/UDEC/Database/2020/ARCHI/'
fiber_dir = '/OverSampledFibers/Final/'

files, subjects = get_list_of_files(directory)
subjects.sort()
# fibers_all = [[] for i in range(63)]
fibers_all = []

for subject in subjects:
    print('Processing', subject)
    subject_fibers_path = directory + subject + fiber_dir

    fibers, tmp = get_list_of_files(subject_fibers_path)
    del tmp
    
    fibers = [f for f in fibers if f.endswith('.bundles')]

    for f_path in fibers:
        f = subject_fibers_path + f_path
        # print(f)

        bundles, name = IOFibers.read_bundles(f)

        for fiber in bundles[:,0]:
            fib = fiber.ravel()

            fibers_all.append(fiber.ravel())


### Escritura de las fibras
from save_bundle import saveBundle

data = np.array(fibers_all, dtype=np.float32).ravel()
curves_count = len(fibers_all)
sizes = np.ones(curves_count,dtype=np.int32)*21
names = ['centroids']
start = [0,curves_count]

saveBundle(data,sizes,names,start,curves_count,'all_centroids.bundles')