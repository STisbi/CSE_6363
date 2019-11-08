import sys
import ReadFromFile as rff

class Neighbor():
    examples = {}
    data_type = {}

    attribute_names = []
    class_names = []

    def __init__(self, path):
        self.path = path

        # Utility that allows reading of the file contents
        self.util = rff.ReadFile()

        # Run the utility on the path given
        self.util.Run(self.path)

        # Separates each attribute type and it's examples into it's own list
        self.ExamplesToDict()
        self.ExampleToDataType()

    # Prints straight from the file
    def PrintTrainingFile(self):
        self.util.PrintStrList()

    def PrintData(self):
        for key in self.examples:
            print(key, ": ", self.examples[key])

    def PrintDataType(self):
        for key in self.data_type:
            print(key, ": ", self.data_type[key])

    def ExamplesToDict(self):
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

    def ExampleToDataType(self):
        for key in self.examples:
            unique_values = len(set(self.examples[key]))

            if unique_values == 0:
                self.data_type[key] = "Issues"
            elif unique_values == 1:
                self.data_type[key] = "Unary"
            elif unique_values == 2:
                self.data_type[key] = "Categorical"
            else:
                self.data_type[key] = "Continuous"



#######################################################
#                        MAIN                         #
#######################################################
def main(argv):
    if argv:
        knn = Neighbor(argv[0])
        # knn.PrintTrainingFile()
        # knn.PrintData()
        knn.PrintDataType()
    else:
        raise Exception("Path not given")


# The 0th argument is the file name
if __name__ == "__main__":
    main(sys.argv[1:])