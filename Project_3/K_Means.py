from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
import copy

class PotassiumMeans:
    def __init__(self, data_file, clusters, number_of_samples=None):
        self.data = pd.read_csv(data_file, header=None)
        self.clusters = clusters

        if number_of_samples:
            self.number_of_samples = number_of_samples
        else:
            self.number_of_samples = len(self.data.columns)

        self.confusion_matrix = None
        self.cost_matrix = None

    def Run_K_Means(self):
        # Transpose the matrix so that each row is a data instance
        transp_data = self.data.transpose()

        # Each row is a data instance and the first column is the true class label
        # Get the first n rows without the first columns
        passed_in_data = transp_data.iloc[:self.number_of_samples, 1: ]

        # This is the first column of n samples
        targets = (transp_data.iloc[:self.number_of_samples, 0:1]).to_numpy().flatten()

        kmeans = KMeans(n_clusters=self.clusters)
        kmeans.fit(passed_in_data)

        # Get the confusion matrix where the column is the true class and the row is the predicted
        self.confusion_matrix = confusion_matrix(targets, kmeans.labels_)
        self.cost_matrix = copy.deepcopy(self.confusion_matrix)

        for index, column in enumerate(self.confusion_matrix.argmax(axis=0)):
            if index != column:
                self.cost_matrix[:, column] = self.confusion_matrix[:, index]

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

    # Example taken from professors slides
    def Confusion_To_Cost_Example(self):
        import numpy as np
        x = np.array(
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 3, 2, 3, 2,
             2, 3, 2,
             3, 2, 2])
        y = np.array(
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4,
             4, 4, 4,
             4, 4, 4])
        conf_mat = confusion_matrix(y, x)
        cost_mat = copy.deepcopy(conf_mat)
        for index, column in enumerate(conf_mat.argmax(axis=0)):
            if index != column:
                cost_mat[:, column] = conf_mat[:, index]

        print("****** Example Confusion Matrix ******\n", conf_mat, "\n**************************************")
        print("******** Example Cost Matrix *********\n", cost_mat, "\n**************************************")
        print("Example Accuracy =", np.trace(cost_mat) / np.sum(cost_mat))

        # This library will transform the confusion matrix to a cost matrix and compute the accuracy all at once
        # from coclust.evaluation.external import accuracy
        # print(accuracy(y, x))

#######################################################
#                        MAIN                         #
#######################################################
def main():
    data_files = ["ATNTFaceImages400.txt", "HandWrittenLetters.txt"]
    pot_means = PotassiumMeans(data_files[0], 10, 100)

    pot_means.Run_K_Means()

    pot_means.Print_Confusion_Matrix()
    pot_means.Print_Cost_Matrix()
    pot_means.Print_Accuracy()

    pot_means.Confusion_To_Cost_Example()


# The 0th argument is the file name
if __name__ == "__main__":
    main()