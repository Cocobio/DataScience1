import numpy as np
from os import listdir
from os.path import isfile, join
import pandas as pd
import matplotlib.pyplot as plt
from FFClust import IOFibers

def get_list_of_files(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    dirs = [f for f in listdir(directory) if not isfile(join(directory, f))]
    return files, dirs

directory = '/home/cocobio/Documents/ARCHI Database/'
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
        bundles, name = IOFibers.read_bundles(f)
        for fibra in bundles[0]:
            length = 0.0
            for i in range(1, len(fibra)):
                length = length + np.linalg.norm(fibra[i] - fibra[i - 1])
            distance.append(length)
            n_fibers.append(len(fibra))

headers = ["Distance", "N Fibers"]
fibers = [distance, n_fibers]
new_table = pd.DataFrame()
for i in range(len(headers)):
    new_table[headers[i]] = fibers[i]
new_table = pd.DataFrame({"Distance":distance, "N Fibers":n_fibers})

new_table.to_csv('Tabla de Datos')

print(new_table)
print(new_table.info())
print(new_table.describe())
new_table.hist(bins=50, figsize=(20,15))
plt.show()