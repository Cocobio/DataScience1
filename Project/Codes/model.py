import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
# import hdbscan

method = "KMeans"
# method = "DBSCAN"
# method = "HDBSCAN"

# outputfile = method+"_on_PCA"
outputfile = method+"_on_UMAP"

# compress_file = 'compress_np.npy' ## PCA
compress_file = 'compress_umap.npy'

compress_data = np.load(compress_file)
print('Data read with shape:', compress_data.shape)

for i in range(compress_data.shape[1]):
	print('dimension:',i)
	print(compress_data[:,i].min())
	print(compress_data[:,i].max())
	print(compress_data[:,i].mean())
	print(compress_data[:,i].std())

cluster = KMeans(60, random_state=24).fit(compress_data)
# cluster = DBSCAN(eps=0.05, min_samples=30).fit(compress_data)
# cluster = hdbscan.RobustSingleLinkage(cut=0.125, k=7)

# hierarchy = cluster.cluster_hierarchy_
# alt_labels = hierarchy.get_clusters(0.100, 5)
# hierarchy.plot()

# labels = cluster.fit_predict(compress_data)
labels = cluster.labels_

print(type(labels))
print(labels.shape)
print(labels.dtype)
print(labels.min())
print(labels.max())
print((labels!=-1).sum()/len(compress_data))


np.save(outputfile, labels)