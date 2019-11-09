import sys
import ReadFromFile as rff
import copy


class Neighbor():
    examples = {}
    new_example = {}
    attributes = {}
    attribute_types = {}
    attribute_values = {}
    attribute_values_num = {}
    transformed_attributes = {}
    transformed_examples = {}
    transformed_new_example = {}
    key_index = {}

    attribute_names = []
    class_names = []
    data = []
    new_data = []

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

        self.transformed_examples = copy.deepcopy(self.examples.copy())
        self.transformed_attributes = self.attributes.copy()

        self.TransformAttributes()
        self.TransformExamples(self.transformed_examples)

    # Prints straight from the file
    def PrintTrainingFile(self):
        self.util.PrintStrList()

    def PrintExamples(self):
        for key in self.examples:
            print(key, ": ", self.examples[key])

    def PrintNewExample(self):
        for key in self.new_example:
            print(key, ": ", self.new_example[key])

    def PrintTransformedExamples(self):
        for key in self.transformed_examples:
            print(key, ": ", self.transformed_examples[key])

    def PrintTransformedNewExample(self):
        for key in self.transformed_new_example:
            print(key, ": ", self.transformed_new_example[key])

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
        self.data = self.util.GetStrList()

        self.AttrToDict(self.data)
        self.ExamplesToList(self.data[1:])

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

    def ExamplesToList(self, data):
        for example in data:
            self.examples[example[0]] = example[1:]

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


    def GetUniqueValues(self, attribute_list):
        unique_values = []
        for attribute in attribute_list:
            if attribute not in unique_values:
                unique_values.append(attribute)

        return unique_values

    def TransformExamples(self, examples):
        for column, key in enumerate(examples):
            attributes_list = examples[key]

            for index, attribute in enumerate(attributes_list):
                attribute_name = self.key_index[index]

                if self.attribute_types[attribute_name] == self.binary:
                    if attribute == self.attribute_values[attribute_name][0]:
                        examples[key][index] = 0
                    elif attribute == self.attribute_values[attribute_name][1]:
                        examples[key][index] = 1
                elif self.attribute_types[attribute_name] == self.categorical:
                    for place, attribute_value in enumerate(self.attribute_values[attribute_name]):
                        if attribute == attribute_value:
                            examples[key][index] = place


    def TransformAttributes(self):
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

    def GetNewExample(self):
        for attribute in list(self.attributes.keys()):
            self.new_data.append(input(attribute + ": "))

        self.ParseNewExample()

    def ParseNewExample(self):
        key = self.new_data[0]
        value = self.new_data[1:]

        self.new_example[key] = value
        self.transformed_new_example = self.new_example.copy()

        self.TransformExamples(self.transformed_new_example)

    def ClassifyNewExample(self, neighbor=1):
        knn_dict = {}

        for key in self.transformed_examples:
            example = self.transformed_examples[key]
            bi_data = []
            # FIXME: Nope nope nope on the hard code
            distance = self.CalculateHammingDistance(example[:-1], list(self.transformed_new_example.values())[0][:-1])

            knn_dict[distance] = self.examples[key][-1]

        key_list = list(knn_dict.keys())
        key_list.sort()

        for k in range(neighbor):
            print("Nearest neighbor", k, ": ", knn_dict[key_list[k]])

    def CalculateHammingDistance(self, example, new_example):
        distance = 0

        for index in range(len(example)):
            if example[index] != new_example[index]:
                distance += 1

        return distance


#######################################################
#                        MAIN                         #
#######################################################
def main(argv):
    if argv:
        knn = Neighbor(argv[0])
        # knn.PrintTrainingFile()
        # knn.PrintAttributes()
        # knn.PrintDataType()
        # knn.PrintExamples()
        # knn.PrintTransformedExamples()

        knn.GetNewExample()
        # knn.PrintTransformedNewExample()
        knn.ClassifyNewExample(neighbor=3)
    else:
        raise Exception("Path not given")


# The 0th argument is the file name
if __name__ == "__main__":
    main(sys.argv[1:])