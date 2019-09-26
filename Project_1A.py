import numpy as np
import matplotlib.pyplot as plt

class Function():
    x_range = None
    equation = None
    scatter = False
    line = False
    color = None


class Math():
    def __init__(self):
        pass

    def graph(self, functionList):
        for function in functionList:
            if function.scatter:
                plt.scatter(function.x_range, function.equation, c=function.color)
            elif function.line:
                plt.plot(function.x_range, function.equation, function.color)

        plt.show()


    def multiply(self, x, y):
        factor_1 = np.array(x)
        factor_2 = np.array(y)
        product = np.multiply(factor_1, factor_2)

        return product


    def sigma(self, x, y):
        addend_1 = np.array(x)
        addend_2 = np.array(y)
        summation = np.sum(self.multiply(addend_1, addend_2))

        return summation


def main():
    math = Math()

    np.random.seed(43)

    functionList = []

    original = Function()
    original.x_range = np.arange(0, 1, 0.01)
    original.equation = np.sin(2 * np.pi * original.x_range)
    original.line = True
    original.scatter = False
    original.color = 'g'
    functionList.append(original)

    noise = Function()
    noise.x_range = np.arange(0, 1, 0.1)
    noise.equation = np.sin(2 * np.pi * noise.x_range +  np.random.normal())
    noise.line = False
    noise.scatter = True
    noise.color = 'b'
    functionList.append(noise)

    math.graph(functionList)


if __name__ == "__main__":
    main()