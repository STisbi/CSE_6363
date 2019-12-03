from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy

class PotassiumMeans:
    def __init__(self, clusters, number_of_samples, mean_1, mean_2, mean_3, sigma):
        self.clusters = clusters
        self.number_of_samples = number_of_samples
        self.mean_1 = mean_1
        self.mean_2 = mean_2
        self.mean_3 = mean_3
        self.sigma = sigma

        self.distribution_1_x = np.zeros(self.number_of_samples)
        self.distribution_1_y = np.zeros(self.number_of_samples)
        self.distribution_2_x = np.zeros(self.number_of_samples)
        self.distribution_2_y = np.zeros(self.number_of_samples)
        self.distribution_3_x = np.zeros(self.number_of_samples)
        self.distribution_3_y = np.zeros(self.number_of_samples)

        self.k_means_data = np.zeros((self.number_of_samples * 3, 2))

        self.result = None
        self.centroids = np.zeros((self.clusters, 2))

        self.confusion_matrix = None
        self.cost_matrix = None

    def Generate_Distributions(self):
        for index in range(self.number_of_samples):
            self.distribution_1_x[index], self.distribution_1_y[index] = np.random.normal(self.mean_1, self.sigma)
            self.distribution_2_x[index], self.distribution_2_y[index] = np.random.normal(self.mean_2, self.sigma)
            self.distribution_3_x[index], self.distribution_3_y[index] = np.random.normal(self.mean_3, self.sigma)

        # Put the x values in the first column and y values in the second column
        self.k_means_data[:, 0] = np.concatenate([self.distribution_1_x, self.distribution_2_x, self.distribution_3_x])
        self.k_means_data[:, 1] = np.concatenate([self.distribution_1_y, self.distribution_2_y, self.distribution_3_y])


    def Run_K_Means(self):
        # This is hacky but for now, whatever
        temp_x = np.concatenate([self.distribution_1_x, self.distribution_2_x, self.distribution_3_x])
        temp_y = np.concatenate([self.distribution_1_y, self.distribution_2_y, self.distribution_3_y])

        # Put the x values in the first column and y values in the second column
        self.k_means_data[:, 0] = temp_x
        self.k_means_data[:, 1] = temp_y

        kmeans = KMeans(n_clusters=self.clusters)
        kmeans.fit(self.k_means_data)
        self.result = kmeans.predict(self.k_means_data)

        self.centroids[:, 0] = kmeans.cluster_centers_[:, 0]
        self.centroids[:, 1] = kmeans.cluster_centers_[:, 1]

    def Plot_Distributions(self, title, before_k_means=False):
        if before_k_means:
            plt.scatter(self.distribution_1_x, self.distribution_1_y, c='r', label="Mean at " + str(self.mean_1))
            plt.scatter(self.distribution_2_x, self.distribution_2_y, c='g', label="Mean at " + str(self.mean_2))
            plt.scatter(self.distribution_3_x, self.distribution_3_y, c='b', label="Mean at " + str(self.mean_3))
        else:
            # Plot the distribution, using the result of the k means as the color differentiator
            plt.scatter(self.k_means_data[:, 0], self.k_means_data[:, 1], c=self.result)

            # Plots the centroids
            plt.scatter(self.centroids[:, 0], self.centroids[:, 1], c='k', s=200, alpha=.5, label="K-Means Centroids")

        # Plot the axis
        plt.plot([0 for x in range(-20, 20)], [x for x in range(-20, 20)], c='k')
        plt.plot([y for y in range(-20, 20)], [0 for y in range(-20, 20)], c='k')

        # Set the boundaries
        plt.xlim(-15, 15)
        plt.ylim(-15, 15)

        # Set the legend and title
        plt.legend()
        plt.title(title)

        # Show it
        plt.show()

#######################################################
#                        MAIN                         #
#######################################################
def main():
    pot_means = PotassiumMeans(3, 100, [3, 5], [-5, 2], [1, -4], 4)

    pot_means.Generate_Distributions()
    pot_means.Plot_Distributions("Before K-Means with Sigma 4", before_k_means=True)
    pot_means.Run_K_Means()
    pot_means.Plot_Distributions("After K-Means with Predicted Data with Sigma 4", before_k_means=False)

# The 0th argument is the file name
if __name__ == "__main__":
    main()