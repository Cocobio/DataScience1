import numpy as np
from os import listdir
from os.path import isfile, join
import pandas as pd
import matplotlib.pyplot as plt
from FFClust import IOFibers
import os

Cluster_F = "FFClust"

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
    
    fibers = [f for f in fibers if f.endswith('.bundles') and f.find("to_21") != -1]

    for f_path in fibers:
        f = subject_fibers_path + f_path

        # print("python3 FFClust/main.py --infile "+f+" --outdir "+subject_fibers_path+Cluster_F)
        os.system("python3 FFClust/main.py --infile "+f+" --outdir "+subject_fibers_path+Cluster_F)

        f_cluster = f[:f.find('.bundles')]+"_centroids"+f[f.find('.bundles'):]
        os.system("mv "+subject_fibers_path+Cluster_F+"/centroids.bundles "+f_cluster)
        os.system("mv "+subject_fibers_path+Cluster_F+"/centroids.bundlesdata "+f_cluster+"data")

        os.system("rm -r "+subject_fibers_path+Cluster_F)
        
    #     break
    # break