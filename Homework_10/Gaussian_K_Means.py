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

        self.distribution_1_x = [None] * self.number_of_samples
        self.distribution_1_y = [None] * self.number_of_samples
        self.distribution_2_x = [None] * self.number_of_samples
        self.distribution_2_y = [None] * self.number_of_samples
        self.distribution_3_x = [None] * self.number_of_samples
        self.distribution_3_y = [None] * self.number_of_samples

        self.confusion_matrix = None
        self.cost_matrix = None

    def Generate_Distributions(self):
        for index in range(self.number_of_samples):
            self.distribution_1_x[index], self.distribution_1_y[index] = np.random.normal(self.mean_1, self.sigma)
            self.distribution_2_x[index], self.distribution_2_y[index] = np.random.normal(self.mean_2, self.sigma)
            self.distribution_3_x[index], self.distribution_3_y[index] = np.random.normal(self.mean_3, self.sigma)

    def Plot_Distributions(self):
        # Plot the distributions
        plt.scatter(self.distribution_1_x, self.distribution_1_y, c='r')
        plt.scatter(self.distribution_2_x, self.distribution_2_y, c='g')
        plt.scatter(self.distribution_3_x, self.distribution_3_y, c='b')

        # Plot the axis
        plt.plot([0 for x in range(-20, 20)], [x for x in range(-20, 20)], c='k')
        plt.plot([y for y in range(-20, 20)], [0 for y in range(-20, 20)], c='k')

        # Set the boundaries
        plt.xlim(-15, 15)
        plt.ylim(-15, 15)

        # Show it
        plt.show()

    def Get_Confusion_Matrix(self):
        return self.confusion_matrix

    def Get_Cost_Matrix(self):
        return self.cost_matrix

    def Get_Accuracy(self):
        return np.trace(self.cost_matrix) / np.sum(self.cost_matrix)

    def Print_Confusion_Matrix(self):
        print("********** Confusion Matrix **********\n", self.Get_Confusion_Matrix(), "\n**************************************")

    def Print_Cost_Matrix(self):
        print("************ Cost Matrix *************\n", self.Get_Cost_Matrix(), "\n**************************************")

    def Print_Accuracy(self):
        print("Accuracy =", self.Get_Accuracy())

#######################################################
#                        MAIN                         #
#######################################################
def main():
    pot_means = PotassiumMeans(3, 100, [5, 5], [-5, 5], [-5, -5], 2)

    pot_means.Generate_Distributions()
    pot_means.Plot_Distributions()

    # pot_means.Run_K_Means()
    #
    # pot_means.Print_Confusion_Matrix()
    # pot_means.Print_Cost_Matrix()
    # pot_means.Print_Accuracy()

# The 0th argument is the file name
if __name__ == "__main__":
    main()