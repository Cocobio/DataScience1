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

save_original = True

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

            # for i in range(63):
            #     fibers_all[i].append(fib[i])
            fibers_all.append([x for x in fiber.ravel()])
        # break
    # break
print('lectura lista')

from sklearn import decomposition
pca = decomposition.PCA(n_components=5)

pca.fit(fibers_all)

compress_data = pca.transform(fibers_all)


compress_np = np.array(compress_data, dtype=np.float32)
np.save('compress_np', compress_np)


if save_original:
    original = np.array(fibers_all, dtype=np.float32)
    np.save('original', original)
    print(original.shape)





