import numpy as np
from sklearn.metrics import silhouette_score
from sklearn.cluster import Means
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


compress_data = np.load('compress_np.npy')
print('Data read with shape:', compress_data.shape)
compress_data, dummy = train_test_split(compress_data, test_size=0.5, random_state=42)

print('Random sample:', compress_data.shape)

range_n_clusters = range(10,100,4)

scores = []
for i in range_n_clusters:
	print("Processing cluster",i)
	km = Means(n_clusters = i, random_state = 24)
	km.fit(compress_data)
	scores.append(km.inertia_)

plt.figure(figsize = (5,5))
plt.plot(range_n_clusters, scores)
plt.xlabel('clusters')
plt.ylabel('inertia')
plt.title("Elbow method")
plt.show()