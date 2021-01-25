import numpy as np
from save_bundle import saveBundle

# labels_file = 'kmeans_on_UMAP.npy'
labels_file = 'HDBSCAN_on_UMAP.npy'

# data_file = 'original.npy'
data_file = 'original_yerke.npy'

output_bundle = 'HDBSCAN_on_UMAP.bundles'

labels = np.load(labels_file)
original_data = np.load(data_file)

print(original_data.shape)

names = [str(x) for x in range(labels.max()+1)]
start = [0,*[x for x in np.cumsum([(labels==i).sum() for i in range(labels.max()+1)])]]
curves_count = start[-1]
sizes = np.ones(curves_count,dtype=np.int32)*21
data = np.concatenate([original_data[labels==i] for i in range(labels.max()+1)]).ravel()

saveBundle(data,sizes,names,start,curves_count,output_bundle)

