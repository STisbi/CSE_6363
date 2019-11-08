import sys
import os
import re


# This class was created to facilitate reading a file given through
# a command line argument. It provides several utility methods that
# parse the file by line into individual characters or words.
class ReadFile:
    areCharsDigits = True
    areStrDigits   = True
    
    numRows     = 0
    numCharColm = 0
    numStrColm  = 0
    
    path = None
    
    charList     = []
    strList      = []
    typeCharList = []
    typeStrList  = []
    
    regex = re.compile('[\W_]+')
    
    # This method, although counter-intuitive is called internally
    # and not by the user. This is so that, all the proper checks
    # required on user input can be handled first
    def ReadFile(self):
        with open(self.path, "r") as file:
            for index, line in enumerate(file):
                self.AddLineByChar(line)
                self.AddLineByWord(line)
                
            self.numRows = index + 1
    
    
    # Takes a line from the file, then each character from 
    # the line is inserted into a list. A subroutine checks
    # if each character is a numerical value and inserts
    # those values as a number into a separate list.
    def AddLineByChar(self, line):
        string = self.regex.sub(' ', line)
        #self.charList.append(list(string))
        
        tempCharList = []
        tempDigList  = []
        
        for char in string:
            tempCharList.append(char)
            
            # Set the number of columns
            if len(string) > self.numCharColm:
                self.numCharColm = len(string)
            
            if char.isdigit():
                tempDigList.append(int(char))
            else:
                tempDigList.append(char)
                self.areCharsDigits = False
                
        self.charList.append(tempCharList)
        self.typeCharList.append(tempDigList)
                
    
    # Similar to AddLineByChar, each line is read
    # and stripped of white space. Each non-whitespace
    # word in the line is added to a list. A subroutine
    # checks if the word is numerical and that word is
    # added to a separate list as a number.
    def AddLineByWord(self, line):
        strList = line.split()
        #self.strList.append(strList)
        
        tempStrList = []
        tempDigList = []
        
        for word in strList:
            tempStrList.append(word)
            
            # Set the number of columns
            if len(strList) > self.numStrColm:
                self.numStrColm = len(strList)
            
            if word.isdigit():
                tempDigList.append(int(word))
            else:
                tempDigList.append(word)
                self.areStrDigits = False
        
        self.strList.append(tempStrList)
        self.typeStrList.append(tempDigList)
        
    
    # Returns two dimensional list of the file input
    # where each row is the list of characters for a line
    def GetCharList(self):
        return self.charList


    # Returns a two dimensional list of the file input
    # where each row is the list of characters for a line
    # that have been converted to numerals.
    def GetTypeCharList(self):
        return self.typeCharList
        
    
    # Returns a two dimensional list of the file input
    # where each row is the list of words in a line
    def GetStrList(self):
        return self.strList
    
    
    # Returns a two dimensional list of the file input
    # where each row is the list of words in a line
    # that has been converted into their numerical value
    def GetTypeStrList(self):
        return self.typeStrList
    
    
    # Returns the number of rows (lines in the file)
    def GetNumRows(self):
        return self.numRows
    
    
    # Returns the maximum number of columns in the file
    # as created by the characters in a line
    def GetNumCharColm(self):
        return self.numCharColm
    
    
    # Returns the maximum number of columns in the file
    # as created by words in a line 
    def GetNumStrColm(self):
        return self.numStrColm
    
    
    # Returns true if the list comprised of all characters
    # contains values that are all numerical
    def IsCharListNumerical(self):
        return self.areCharsDigits

    
    # Returns true if the list comprised of all words
    # contains values that are all numerical
    def IsStrListNumerical(self):
        return self.areStrDigits

    
    # Prints the character list by row
    def PrintCharList(self):
        for row in self.charList:
            print(row)
            
    
    # Prints the numerical type list by row
    def PrintCharTypeList(self):
        for row in self.typeCharList:
            print(row)
            
    
    # Prints the string list by row
    def PrintStrList(self):
        for row in self.strList:
            print(row)
            
    
    # Prints the numerical string list by row
    def PrintStrTypeList(self):
        for row in self.GetTypeStrList():
            print(row)

    
    # Resets all data, so another file can be read
    def ClearData(self):
        self.charList     = []
        self.strList      = []
        self.typeCharList = []
        self.typeStrList  = []
        
        self.areCharsDigits = True
        self.areStrDigits   = True
        
        self.path = ""
        
    
    # Call this method to begin the process of reading 
    # from a file. Checks the type of the input as well
    # as if it is a valid path to a file.
    def Run(self, path):
        if isinstance(path, str):
            if os.path.isfile(path):
                self.path = path
                self.ReadFile()
            else:
                print(path + " is not a file.")
        else:
            print("The argument given is not a string.")   
            
            
#######################################################
#                        MAIN                         #
#######################################################
def main(argv):
    if not argv:
        print("No argument given.")

    else:
        util = ReadFile()
        
        util.Run(argv[0])
        
        util.PrintStrList()
        
        print(util.GetNumRows(), util.GetNumCharColm(), util.GetNumStrColm())
        

# The 0th argument is the file name
if __name__ == "__main__":
    main(sys.argv[1:])