import numpy as np
from os import listdir
from os.path import isfile, join
import pandas as pd
import matplotlib.pyplot as plt
from FFClust import IOFibers
import os
import shutil

Cluster_F = "FFClust"

def get_list_of_files(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    dirs = [f for f in listdir(directory) if not isfile(join(directory, f))]
    return files, dirs

# directory = '/home/cocobio/Documents/ARCHI_Database/'
directory = 'D:/Codes/UDEC/Database/2020/ARCHI/'
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
    
    fibers = [f for f in fibers if f.endswith('.bundles') and f.find("to_21") != -1 and f.find("centroids") == -1]

    for f_path in fibers:
        f = subject_fibers_path + f_path

        # print("python FFClust/main.py --infile "+f+" --outdir "+subject_fibers_path+Cluster_F+f_path)
        os.system("python FFClust/main.py --infile "+f+" --outdir "+subject_fibers_path+Cluster_F+f_path[:f_path.rindex('.')])

        f_cluster = f[:f.find('.bundles')]+"_centroids"+f[f.find('.bundles'):]
        # os.system("mv "+subject_fibers_path+Cluster_F+"/centroids.bundles "+f_cluster)
        # os.system("mv "+subject_fibers_path+Cluster_F+"/centroids.bundlesdata "+f_cluster+"data")

        shutil.move(subject_fibers_path+Cluster_F+f_path[:f_path.rindex('.')]+"/centroids.bundles", f_cluster)
        shutil.move(subject_fibers_path+Cluster_F+f_path[:f_path.rindex('.')]+"/centroids.bundlesdata", f_cluster+"data")

        # Originalmente estaba borrando los datos, pero lo necesito para verificar los clusters usando los ids de los centroides que escupa mi modelo 
        # os.system("rm -r "+subject_fibers_path+Cluster_F)
        # shutil.rmtree(subject_fibers_path+Cluster_F)
        
    #     break
    # break