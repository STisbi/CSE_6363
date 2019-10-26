import math
import sys
import numpy as np
import matplotlib.pyplot as plt

# Class to hold all information pertaining to function
class Function:
    x_range = None
    equation = None
    scatter = False
    line = False
    color = None
    name = None


# A class to graph a function, along with some helper functions
class Graph:
    def graph(self, functionList):
        for delay, function in enumerate(functionList):
            if function.scatter:
                plt.scatter(function.x_range, function.equation, c=function.color, label=function.name)
            elif function.line:
                plt.plot(function.x_range, function.equation, function.color, label=function.name)
            plt.legend()
            plt.ylim(-4, 4)
            plt.pause(5)

        plt.show()


    # Multiplies two lists/arrays/tuples/nparrays together
    def multiply(self, x, y):
        factor_1 = np.array(x)
        factor_2 = np.array(y)
        product = np.multiply(factor_1, factor_2)

        return product


    # Takes the sum of two lists/arrays/tuples/nparrays
    def sigma(self, x, y):
        addend_1 = np.array(x)
        addend_2 = np.array(y)
        summation = np.sum(self.multiply(addend_1, addend_2))

        return summation

# A class to manage all linear equations that will be part of the graph
class LinearEq:
    # Gives an nparray of w values using equation derivative solution to equation 1.4 by
    # solving for w at a given M.
    def regularization(self, M, N, X, T, r_lambda):
        matrixA = np.zeros((M + 1, M + 1))

        # The left-hand side of the equation
        # Sigma from j = 0 to M of (Sigma from n = 1 to N of (((X at n) ^ (j + i)) + lambda))
        for i in range(M + 1):
            for j in range(M + 1):
                for n in range(N):
                    matrixA[i][j] += (X[n] ** (i + j) + r_lambda)

        vectorT = np.zeros((M + 1))

        # The right-hand side of the equation
        # Sigma from n = 1 to N of (((X at n) ^ i) * T at n)
        for m in range(M + 1):
            for n in range(N):
                vectorT[m] += (X[n] ** m) * T[n]

        # Solves for w in the equation A*w = T
        # Where A is a matrix and T is a vector
        w = np.linalg.solve(matrixA, vectorT)

        return w


    # Gives a nparray of y values using equation 1.1
    def poly(self, M, W, X):
        equation = np.zeros((X.size))

        # Sigma from j = 0 to M of ((W at j) * (X at j))
        for x in range(X.size):
            for j in range(M + 1):
                equation[x] += (W[j] * (X[x] ** j))

        return equation


def main():
    graph = Graph()
    linEq = LinearEq()

    # Keeps the random value to a constant random value
    np.random.seed(31)

    functionList = []

    # The original function, 2*pi*x
    original = Function()
    original.x_range = np.arange(0, 1, 0.01)
    original.equation = np.sin(2 * np.pi * original.x_range)
    original.line = True
    original.scatter = False
    original.color = 'g'
    original.name = "Orignal Function No Noise"
    functionList.append(original)

    y = []
    for x in np.linspace(0,1,10):
        y.append(np.sin(2 * np.pi * x) + (-1**x) * (0.2 * np.random.random()))


    # The original function with noise, 2*pi*x + noise
    noise = Function()
    noise.x_range = np.arange(0, 1, 0.1)
    noise.equation = np.array(y)
    noise.line = False
    noise.scatter = True
    noise.color = 'b'
    noise.name = "Points with Noise"
    functionList.append(noise)

    M = 9
    lambda_list = [0, 10**(-20), 10**(-10), 10**(-6), 10**(-4), 10**(-2), 1]
    color_list = ['r', 'c', 'm', 'k', 'y', 'c', 'm']

    for index, r_lambda, in enumerate(lambda_list):
        # Solve for W
        W = linEq.regularization(M, noise.x_range.size, noise.x_range, noise.equation, r_lambda)

        print("W for Lambda = ", str(r_lambda), " is: ", W)

        # Use the W values to get the new polynomial
        polynomial = Function()
        polynomial.x_range = np.arange(0, 1, 0.01)
        polynomial.equation = linEq.poly(M, W, polynomial.x_range)
        polynomial.line = True
        polynomial.scatter = False
        polynomial.color = color_list[index]
        polynomial.name = "Polynomial where lambda = " + str(r_lambda)

        functionList.append(polynomial)

    graph.graph(functionList)


if __name__ == "__main__":
    main()
