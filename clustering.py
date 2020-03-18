from __future__ import print_function
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.manifold import MDS


#collect the data from the chosen csv file
#open a text file to write the result of the clusters to it
tweets = pd.read_csv("/Users/manish/Desktop/websci/database.csv", error_bad_lines=False)
file = open("Clusters.txt", "w")

# Extract the collected usernames from all of the tweets
collected_usernames = tweets['username']
# Extract the collected hashtags from all of the tweets
collected_hashtags = tweets['hashtags']
# Extract the collected text from all of the tweets
collected_text = tweets['text']

#Create a vector to transform the names into integer values so that the KMeans can be calculated
#Clusters cannot be created without first vectorising the strings
vectorizer = TfidfVectorizer(stop_words='english')
# Vectorise usernames
vect_username = vectorizer.fit_transform(collected_usernames.values.astype('U'))
# Vectorise hashtags
vect_hashtags = vectorizer.fit_transform(collected_hashtags.values.astype('U'))
# Vectorise text
vect_text = vectorizer.fit_transform(collected_text.values.astype('U'))

k = 10


# Cluster the usernames from the vector
kmeans_username = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
kmeans_username.fit(vect_username)


clusters = kmeans_username.labels_.tolist()

usernames = { 'username': collected_usernames, 'cluster': clusters }
frame = pd.DataFrame(usernames, index = [clusters] , columns = ['username', 'cluster'])

print(frame['cluster'].value_counts()) #number of usernames per cluster (clusters from 0 to 8)



# Print top 10 usernames per cluster
print("Top usernames per cluster:")
file.write("Top usernames per cluster:\n")
order_centroids = kmeans_username.cluster_centers_.argsort()[:, ::-1]
terms_username = vectorizer.get_feature_names()
for i in range(k):
    print ("Cluster %d:" % i)
    file.write("Cluster %d:" % i)
    file.write("\n")
    for ind in order_centroids[i, :10]:
        print (' %s' % terms_username[ind])
        file.write(' %s' % terms_username[ind])
        file.write("\n")


#set up colors per clusters using a dict
cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#1b5d9e', 6: '#9e1b52', 7: '#b8b21c', 8: '#52b041', 9: '#8541b0'}

#set up cluster names using a dict
cluster_names = {0: 'Cluster 0',
                 1: 'Cluster 1',
                 2: 'Cluster 2',
                 3: 'Cluster 3',
                 4: 'Cluster 4',
                 5: 'Cluster 5',
                 6: 'Cluster 6',
                 7: 'Cluster 7',
                 8: 'Cluster 8',
                 9: 'cluster 9'}





# Cluster the hashtags from the vector
kmeans_hashtags = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
kmeans_hashtags.fit(vect_hashtags)

clusters_hash = kmeans_hashtags.labels_.tolist()

hashtags = { 'hashtags': collected_hashtags, 'cluster': clusters_hash }
frame = pd.DataFrame(hashtags, index = [clusters_hash] , columns = ['hashtags', 'cluster'])

print(frame['cluster'].value_counts()) #number of hashtags per cluster (clusters from 0 to 8)

# Print top 10 hashtags per cluster
print("Top hashtags per cluster:")
file.write("\nTop hashtags per cluster:\n")
order_centroids = kmeans_hashtags.cluster_centers_.argsort()[:, ::-1]
terms_hashtags = vectorizer.get_feature_names()
for i in range(k):
    print ("Cluster %d:" % i)
    file.write("Cluster %d:" % i)
    file.write("\n")
    for ind in order_centroids[i, :10]:
        print (' %s' % terms_hashtags[ind])
        file.write(' %s' % terms_hashtags[ind])
        file.write("\n")

print("\n")



# Cluster the text from the vector
kmeans_text = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
kmeans_text.fit(vect_text)

clusters_text = kmeans_text.labels_.tolist()

text = { 'text': collected_text, 'cluster': clusters_text }
frame = pd.DataFrame(text, index = [clusters_text] , columns = ['text', 'cluster'])

print(frame['cluster'].value_counts()) #number of text per cluster (clusters from 0 to 8)


# Print top 10 text per cluster
print("Top text per cluster:")
file.write("\nTop text per cluster:\n")
order_centroids = kmeans_text.cluster_centers_.argsort()[:, ::-1]
terms_text = vectorizer.get_feature_names()
for i in range(k):
    print ("Cluster %d:" % i)
    file.write("Cluster %d:" % i)
    file.write("\n")
    for ind in order_centroids[i, :10]:
        print (' %s' % terms_text[ind])
        file.write(' %s' % terms_text[ind])
        file.write("\n")

# convert two components as we're plotting points in a two-dimensional plane
# "precomputed" because we provide a distance matrix
# we will also specify `random_state` so the plot is reproducible.
mds = MDS(n_components=2, dissimilarity="euclidean", random_state=1)

pos = mds.fit_transform(vect_username.toarray()) # shape (n_components, n_samples)

xs, ys = pos[:, 0], pos[:, 1]
print()
print()


df = pd.DataFrame(dict(x=xs, y=ys, label=clusters_text, text=collected_text))

#group by cluster
groups = df.groupby('label')


# set up plot
fig, ax = plt.subplots(figsize=(17, 9)) # set size
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

#iterate through groups to layer the plot
#note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
            label=cluster_names[name], color=cluster_colors[name],
            mec='none')
    ax.set_aspect('auto')
    ax.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params(\
        axis= 'y',         # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelleft='off')

ax.legend(numpoints=1)  #show legend with only 1 point


plt.show() #show the plot


file.close()
