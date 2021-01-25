import numpy as np
from os import listdir
from os.path import isfile, join
from FFClust import IOFibers
import os
import pandas as pd


# Only for graph with the PCA variance
chart = True



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

            # for i in range(63):
            #     fibers_all[i].append(fib[i])
            fibers_all.append([x for x in fib.astype(np.float32)])
        # break
    # break
print('lectura lista')

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

x=fibers_all

pca = PCA()
print('PCA fitting')
pca.fit_transform(x)
print('PCA fitted')
pca_variance = pca.explained_variance_ratio_


var_acum = 0

for i in range(len(pca_variance)):
    var_acum += pca_variance[i]

    if var_acum > 0.95:
        print("variance: ",var_acum)
        print("Numero de componentes principales: ",i+1)
        break


if chart:
	labels = [x+1 for x in range(63)]
	plt.figure(figsize=(8, 6))
	plt.bar(labels, pca_variance, alpha=0.5, align='center')
	plt.legend()
	plt.ylabel('Variance ratio')
	plt.xlabel('Principal components')


	print(labels)
	print(pca_variance)
	plt.show()