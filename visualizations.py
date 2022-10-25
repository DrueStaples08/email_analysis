from sklearn.decomposition import PCA
from email_data_analysis import extract_email
# from preprocessing.Word2VecAnalogy import word_embeddings
from preprocessing import Word2VecAnalogy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def two_dim_decomp(email_vectors):
    email_vectors = np.array(list(email_vectors.values()))
    # res = []
    # print(email_vectors)
    # print('EMAIL VECTOR INFO', email_vectors.shape, type(email_vectors))
    model = PCA(n_components=2)
    scaled_data = model.fit_transform(email_vectors)
    # for key, ev in email_vectors.items():
    #     try:
            # res.append(model.fit_transform(email_vectors))
    #     except TypeError:
    #         pass
    
    return scaled_data, model

    # return res

# def plot_emails(email_vectors):
#     scaled_data, model = two_dim_decomp(email_vectors)
#     plt.scatter(scaled_data[:, 0], scaled_data[:, 1])
#     plt.show()
#     plt.savefig('PCA_emails.png')
#     return 'PCA Plot Saved!'



def elbow_plot_run(email_vectors):
    scaled_data, pca_model = two_dim_decomp(email_vectors)
    f = plt.figure(1)
    n_clusters = []
    for i in range(1,10):
        model = KMeans(n_clusters=i)
        model.fit(X=scaled_data.astype('double'))
        n_clusters.append(model.inertia_)
    plt.plot(range(1,len(n_clusters)+1), n_clusters, '-o')
    plt.title('Elbow Plot using KMeans')
    f.savefig('elbow_plot.png')
    plt.show()



def kmeans_run(email_vectors, cluster_quantity=3):
        scaled_data, pca_model = two_dim_decomp(email_vectors)
        model = KMeans(n_clusters=cluster_quantity)
        model.fit(X=scaled_data.astype('double'))
        labels = model.labels_
        test_example = np.array([[.0498259477, .159357786]], dtype='double')
        predictions = model.predict(test_example)
        cluster_centers = model.cluster_centers_

        print('model', model)
        print('predictions', predictions)
        print('cluster_centers', cluster_centers)
        print('labels', labels)
        g = plt.figure(2)
        plt.scatter(scaled_data[:, 0], scaled_data[:, 1], c=labels)
        plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], c='red', marker='+', s=50)
        plt.title(f'KMeans with {cluster_quantity} clusters. Silhouette Score {silhouette_score(scaled_data, labels)}')
        g.savefig('kmeans_scatter.png')
        plt.show()

    # plot cluster centers
    # title the kmeans scatter plot with metrics (what are metrics to kmeans? Distance from each node to its respective cluster)
    # Use TDA KepplerMapper tool to visualize data in higher dimensions
    
    #



    # print(scaled_data)
    # print('kmeans run')

if __name__ == '__main__':
    ee = extract_email()
    wa = Word2VecAnalogy(ee)
    we = wa.word_embeddings()
    # tdd = two_dim_decomp(we)
    # print(tdd)
    # pe = plot_emails(we)


    kr = elbow_plot_run(we)
    km = kmeans_run(we)
    print('Now testing the inertia on a range of cluster quantities')
    print(kr)
    print('Elbow Plot Created')
    print('-------------')
    print('Now separating data by clusters found by the elbow plot above')
    print(km)
    print('Data Clustered')
