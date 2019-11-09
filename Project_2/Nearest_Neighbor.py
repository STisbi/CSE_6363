import sys
import ReadFromFile as rff


class Neighbor():
    examples = {}
    attributes = {}
    attribute_types = {}
    attribute_values = {}
    attribute_values_num = {}
    transformed_attributes = {}
    transformed_examples = {}
    key_index = {}

    attribute_names = []
    class_names = []

    unknown = "unknown"
    unary = "unary"
    binary = "binary"
    categorical = "categorical"
    continuous = "continuous"

    def __init__(self, path):
        self.path = path

        # Utility that allows reading of the file contents
        self.util = rff.ReadFile()

        # Run the utility on the path given
        self.util.Run(self.path)

        # Separates each attribute type and it's examples into it's own list
        self.ParseData()
        self.ExampleToDataType()
        self.TransformAttributes()
        self.TransformExamples()

    # Prints straight from the file
    def PrintTrainingFile(self):
        self.util.PrintStrList()

    def PrintExamples(self):
        for key in self.examples:
            print(key, ": ", self.examples[key])

    def PrintTransformedExamples(self):
        for key in self.transformed_examples:
            print(key, ": ", self.transformed_examples[key])

    def PrintAttributes(self):
        for key in self.attributes:
            print(key, ": ", self.attributes[key])

    def PrintTransformedAttributes(self):
        for key in self.transformed_attributes:
            print(key, ": ", self.transformed_attributes[key])

    def PrintDataType(self):
        for key in self.attribute_types:
            print(key, ": ", self.attribute_types[key])

    def ParseData(self):
        # Data is an row by column array
        data = self.util.GetStrList()

        self.ExamplesToList(data[1:])
        self.AttrToDict(data)

    def ExamplesToList(self, data):
        for example in data:
            self.examples[example[0]] = example[1:]


    def AttrToDict(self, data):
        # Iterate over column
        for column in range(len(data[0])):
            key = ""
            value = []
            # Iterate over row
            for row in range(len(data)):
                # The first row has the names for the type of attribute in that column
                if row == 0:
                    key = data[row][column]

                    self.attribute_names.extend(key)
                    self.key_index[column - 1] = key
                else:
                    value.append(data[row][column])

            self.attributes[key] = value

    def ExampleToDataType(self):
        for key in self.attributes:
            values = self.GetUniqueValues(self.attributes[key])
            num_values = len(values)

            if num_values == 0:
                self.attribute_types[key] = self.unknown
            elif num_values == 1:
                self.attribute_types[key] = self.unary
            elif num_values == 2:
                self.attribute_types[key] = self.binary
            else:
                self.attribute_types[key] = self.categorical

            self.attribute_values[key] = values
            # self.attribute_values_num[key] = self.ValueToNumber(values)


    def GetUniqueValues(self, attribute_list):
        unique_values = []
        for attribute in attribute_list:
            if attribute not in unique_values:
                unique_values.append(attribute)

        return unique_values


    def TransformExamples(self):
        self.transformed_examples = self.examples.copy()

        for column, key in enumerate(self.transformed_examples):
            attributes_list = self.transformed_examples[key]

            for index, attribute in enumerate(attributes_list):
                attribute_name = self.key_index[index]

                if self.attribute_types[attribute_name] == self.binary:
                    if attribute == self.attribute_values[attribute_name][0]:
                        self.transformed_examples[key][index] = 0
                    elif attribute == self.attribute_values[attribute_name][1]:
                        self.transformed_examples[key][index] = 1


    def TransformAttributes(self):
        self.transformed_attributes = self.attributes.copy()

        for key in self.transformed_attributes:
            if self.attribute_types[key] == self.binary:
                unique_list = self.GetUniqueValues(self.transformed_attributes[key])
                new_list = []
                for value in self.transformed_attributes[key]:
                    if value == unique_list[0]:
                        new_list.append(0)
                    else:
                        new_list.append(1)

                self.transformed_attributes[key] = new_list

#######################################################
#                        MAIN                         #
#######################################################
def main(argv):
    if argv:
        knn = Neighbor(argv[0])
        # knn.PrintTrainingFile()
        # knn.PrintAttributes()
        # knn.PrintDataType()
        # knn.PrintTransformedData()
        # knn.PrintExamples()
        knn.PrintTransformedExamples()
    else:
        raise Exception("Path not given")


# The 0th argument is the file name
if __name__ == "__main__":
    main(sys.argv[1:])