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

directory = '/home/cocobio/Documents/ARCHI_Database/'
fiber_dir = '/OverSampledFibers/Final/'

files, subjects = get_list_of_files(directory)
subjects.sort()
fibers_all = [[] for i in range(63)]

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

            for i in range(63):
                fibers_all[i].append(fib[i])
            # fibers_all.append([x for x in fiber.ravel()])
            # print(fiber.shape)
        # break
    # break
print('lectura lista')
new_table = pd.DataFrame(data=fibers_all)
print('DataFrame')
new_table.to_csv('AllCentroids')

# from sklearn import decomposition
# pca = decomposition.PCA(n_components=21)

# pca.fit(fibers_all)

# compress_data = pca.transform(fibers_all)

# print(len(compress_data),len(compress_data[0]))
# print(len(fibers_all),len(fibers_all[0]))

