# Import libraries
import unittest
import pandas as pd

dataset_file = 'null'

# Class and functions
# -Loading a dataset
def choosing_dataset():
    # Choose a dataset
    dataset_file = str(input('Please choose a dataset file in .csv format: '))
    if dataset_file[-4:] != '.csv':
        raise ValueError('Please choose a dataset file in .csv format.')
    # Extract the columns to list

# -Normality test
def normality_test():
    print('Before using [3], please run the normality test for the aimed parameter.')
# -One-way ANOVA test or Mann-Whitney U test
# -Linear regression
# -Unit testing
  #class TestFunctions(unittest.TestCase):

menu = {1:("Choose a dataset",choosing_dataset),
        2:("Normality test",choosing_dataset),
        3:("One-way ANOVA test or Mann-Whitney U test",choosing_dataset),
        4:("Linear regression",choosing_dataset),
        5:("Help",choosing_dataset),
        6:("Exit",choosing_dataset)}

while True:
    # Display the menu
    print( '''
    #################### MENU ####################
    Input a command to use the function.
    E.g. Input 5 to use the [Help] command.
    
    The current dataset is: {} 
    '''.format(dataset_file))
    for key in sorted(menu.keys()):
        print ('    [{}] {}'.format(key,menu[key][0]))

    # Input the command and catch errors
    try:
        current_command = int(input('Please select: '))
    except ValueError:
        print('Please enter an integer.') # Don't raise error as the loop should restart later.

    # Run the selected command and catch errors
    try:
        menu.get(current_command)[1]()
    except KeyError:
        print('Please enter an integer between 1 and 6.') # Don't raise error as the loop should restart later.

        
#if __name__ == '__main__':
#    unittest.main()
