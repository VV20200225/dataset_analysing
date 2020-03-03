# Import libraries
import unittest
import pandas as pd
import os
from scipy import stats
from pandas.api.types import is_numeric_dtype

# Class and functions
# -choosing_dataset
def choosing_dataset():
    global dataset_file
    dataset_file = dataset(str(input('\nPlease input a filename in .csv format: ')))

# -dataset class
class dataset:

    def __init__(self,filename):
        # Raise an error if filename is not a string
        if not isinstance(filename,str):
            raise TypeError('The filename is not a string.')
        # Raise an error if filename does exist
        if not os.path.isfile(filename):
            raise FileNotFoundError('No such file or directory.')
        # Raise an error if
        if filename[-4:] != '.csv':
            raise FileNotFoundError('Please choose a dataset file in .csv format.')

        self.filename = filename
        # Read the file
        self.df = pd.read_csv(self.filename)

        # Make a dictionary to save the normality result
        self.normality = {}

    def input_independent(self,testname):
        # Print the name of each variable in the dataset.
        for i in list(self.df.columns):
            print(i)
        # Input the independent variable
        independent = str(input('\nPlease select an independent to run {}: '.format(testname)))
        # Return the function if the independent can't be found in the dataset
        if not independent in self.df.columns:
            print('Please enter a correct variable name.')
            return
        # Return the function if the independent is not numeric.
        if not is_numeric_dtype(self.df[independent]):
            print('The datatype is not number.')
            return
        print('The independent {} is selected.'.format(independent))
        return independent

    def input_dependent(self,testname):
        # Assign
        self.df = pd.read_csv(self.filename)
        # Print the name of each variable in the dataset.
        for i in list(self.df.columns):
            print(i)
        # Input the dependent variable
        dependent = str(input('\nPlease select an dependent to run {}: '.format(testname)))
        # Return the function if the dependent can't be found in the dataset
        if not dependent in self.df.columns:
            print('Please enter a correct variable name.')
            return
        # Return the function if the dependent is not numeric.
        if not is_numeric_dtype(self.df[dependent]):
            print('The datatype is not number.')
            return
        print('The dependent {} is selected.'.format(dependent))
        return dependent

    def normality_test(self):
        independent = self.input_independent('Shapiro-Wilk test for normality')
        # If the tests were not passed, independent should be a None and then we should return the function
        if independent == None:
            return
        # Calculate and print the normality result
        shapiro = stats.shapiro(self.df[independent].dropna())
        print('Test statistic: {}\np-value: {}'.format(shapiro[0],shapiro[1]))
        # Save the shapiro result to the normality dictionary if it's not in the dictionary
        if independent in self.normality.keys():
            return
        else:
            self.normality[independent] = shapiro

    def anova(self):
        # Set a significance_level
        try:
            siglevel = float(input('\nPlease enter a significance level: '))
        except ValueError:
            print('The significance level should be numeric')
            return

        # Choose an independent
        independent = self.input_independent('one-way ANOVA')
        # If the tests were not passed, independent should be a None and then we should return the function
        if independent == None:
            return
        if self.normality[independent][1] < siglevel:
            print('The p-value for {} is larger than {}, which rejects the normality test.\nPlease use the Mann-Whitney U test.'.format(independent,siglevel))
            return

        # Choose an dependent
        dependent = self.input_dependent('Shapiro-Wilk test for normality')
        # If the tests were not passed, dependent should be a None and then we should return the function
        if dependent == None:
            return

    def utest(self):
        print()
    def linear_regression(self):
        print()


# -Unit testing
  #class TestFunctions(unittest.TestCase):

menu = {1:("Choose a dataset",choosing_dataset),
        2:("Normality test",),
        3:("One-way ANOVA test or Mann-Whitney U test",),
        4:("Linear regression",),
        5:("Help",),
        6:("Exit",exit)}

while True:
    # Display the menu
    print( '''
    #################### MENU ####################
    Input a command to use the function.
    E.g. Input 5 to use the [Help] command.
    
    The current dataset is: {} 
    '''.format('Not existed' if not 'dataset_file' in globals() else dataset_file.filename))

    for key in sorted(menu.keys()):
        print ('    [{}] {}'.format(key,menu[key][0]))

    # Input the command and catch errors
    try:
        current_command = int(input('\nPlease select: '))
    except ValueError:
        print('Please enter an integer.') # Don't raise error as the loop should restart later.

    # Run the selected command and catch errors
    try:
        menu.get(current_command)[1]()
    except KeyError:
        print('Please enter an integer between 1 and 6.') # Don't raise error as the loop should restart later.


#if __name__ == '__main__':
#    unittest.main()
