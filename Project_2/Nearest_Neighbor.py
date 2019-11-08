import sys
import ReadFromFile as rff

class Neighbor():
    examples = {}
    attribute_names = []
    class_names = []

    def __init__(self, path):
        self.path = path

        # Utility that allows reading of the file contents
        self.util = rff.ReadFile()

        # Run the utility on the path given
        self.util.Run(self.path)

        # Separates each attribute type and it's examples into it's own list
        self.ExamplesToList()

    # Prints straight from the file
    def PrintTrainingFile(self):
        self.util.PrintStrList()

    def PrintData(self):
        for key in self.examples:
            print(key, ": ", self.examples[key])

    def ExamplesToList(self):
        # Data is an row by column array
        data = self.util.GetStrList()

        # Iterate over column
        for column in range(len(data[0])):
            key = ""
            value = []
            # Iterate over row
            for row in range(len(data)):
                # The first row has the names for the type of attribute in that column
                if row == 0:
                    self.attribute_names.extend(data[row][column])
                    key = data[row][column]
                else:
                    value.append(data[row][column])

            self.examples[key] = value


#######################################################
#                        MAIN                         #
#######################################################
def main(argv):
    if argv:
        knn = Neighbor(argv[0])
        # knn.PrintTrainingFile()
        knn.PrintData()
    else:
        raise Exception("Path not given")


# The 0th argument is the file name
if __name__ == "__main__":
    main(sys.argv[1:])