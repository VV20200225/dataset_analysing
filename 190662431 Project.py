# Import libraries
import unittest
import pandas as pd
import os
from scipy import stats
from pandas.api.types import is_numeric_dtype
from sklearn.linear_model import LinearRegression

# Class and functions
# -choosing_dataset
def choosing_dataset():
    global dataset_file
    dataset_file = dataset(str(input('\nPlease input a filename in .csv format: ')))

# -dataset class
class dataset:
    def __init__(self, filename):
        # Raise an error if filename is not a string
        if not isinstance(filename, str):
            raise TypeError('The filename is not a string.')
        # Raise an error if filename does exist
        if not os.path.isfile(filename):
            raise FileNotFoundError('No such file or directory.')
        # Raise an error if filename is not in .csv format
        if filename[-4:] != '.csv':
            raise FileNotFoundError('Please choose a dataset file in .csv format.')

        self.filename = filename
        # Read the file
        self.df = pd.read_csv(self.filename)
        # Make a dictionary to save the distribution result
        self.distribution = {}

    def input_variable(self, testname, var_type):
        # Print the name of each variable in the chosen dataset.
        for i in list(self.df.columns):
            print(i)
        # Input the variable
        var = str(input('\nPlease select an {} to run {}: '.format(var_type, testname)))
        # Return if the variable can't be found in the dataset.
        if not var in self.df.columns:
            print('Please enter a correct variable name.')
            return
        print('The {} {} is selected.'.format(var_type, var))
        return var

    def distribution_test(self):
        # Choose dependent
        dependent = self.input_variable('distribution test', 'dependent')
        # When it's failed to select a variable. The variable should then be a None.
        # In this case, we should end the execution of the function call.
        if dependent == None:
            return

        # Determine binomial data
        lst = self.df[dependent].dropna().values.tolist()
        # For a sorted list, if lst[0] != lst[-1] and lst[0] + lst[-1] = len(lst), then the item values for the list might be binomial
        if lst.count(lst[0]) + lst.count(lst[-1]) == len(lst) and lst[0] != lst[-1]:
            # The values might just look binomial and we need to confirm with the user.
            bino_confirm = input('This dependent consists only {} and {}. Do you confirm that it is binomial?\nEnter Y to confirm: '.format(lst[0],lst[-1]))
            if bino_confirm== 'Y' or 'y' or 'yes' or 'Yes':
                self.distribution[dependent] = [0, 0, 'binomial']
                print('You have confirmed that the dependent is binomial.')
                return
            else:
                print('You have disagreed that the dependent is binomial.')
        else:
            print('The dependent is not binomial.')

        # Set a significance_level
        try:
            critical_val = float(input('\nPlease enter a critical value before running Shapiro-Wilk test: '))
        except ValueError:
            print('The critical value should be numeric')
            return

        # Shapiro test
        # Return the function if the dependent is not numeric because Shapiro test only takes numbers.
        if not is_numeric_dtype(self.df[dependent]):
            print('The dependent should be numeric for Shapiro-Wilk test .')
            return
        # Calculate and print the distribution result
        shapiro = stats.shapiro(self.df[dependent].dropna())
        print('Test statistic: {}\np-value: {}'.format(shapiro[0], shapiro[1]))

        # Print the comparison between p-value and critical-value
        if shapiro[1] > critical_val:
            print(
                'The p-value for dependent is larger than critical-value of {}, which rejects the normality test.'.format(
                    critical_val))
            self.distribution[dependent] =  [shapiro[0], shapiro[1], 'Gaussian']
        else:
            print(
                'The p-value for dependent is smaller than or equal to critical-value of {}, which accepts the normality test.'.format(
                    critical_val))
            self.distribution[dependent] = [shapiro[0], shapiro[1], 'non-Gaussian']


    def stat_tests(self):
        # Reminder
        print('''Statistical tests will run with regards to the datatype of dependent.
        Please perform distribution test before starting this test.''')

        # Choose an independent
        independent = self.input_variable('statistical tests', 'independent')
        # When it's failed to select a variable. The variable should then be a None.
        # In this case, we should end the execution of the function call.
        if independent == None:
            return
        # Choose a dependent
        dependent = self.input_variable('statistical tests', 'dependent')
        # When it's failed to select a variable. The variable should then be a None.
        # In this case, we should end the execution of the function call.
        if dependent == None:
            return

        # If the dependent has no result for the distribution test, then the function should return.
        if not dependent in self.distribution.keys():
            print('Please run the distribution test before running statistical tests.')
            return

        # Binomial case
        if self.distribution[dependent][3] == 'binomial':


            return

        # Before the cases for Gaussian and non-Gaussian
        # Extract independent groups and save their names
        group_name = list(self.df.groupby([independent]).groups.keys())
        # Make an empty group
        groups = {}
        # Group the dependent according to the independent subgroups
        for subgroup in group_name:
            groups[subgroup] = self.df.groupby([independent]).get_group(subgroup)[dependent].values.tolist()

        # Gaussian case
        if self.distribution[dependent][3] == 'Gaussian':
            print(stats.f_oneway(*groups.values()))
            return
        # Non-Gaussian case
        if self.distribution[dependent][3] == 'non-Gaussian':
            # Compare each two groups
            lst_key = list(groups.keys())
            for i in range(len(lst_key)):
                for k in range(i + 1, len(lst_key)):
                    utest = stats.mannwhitneyu(groups[lst_key[i]], groups[lst_key[k]])
                    print(independent,lst_key[i],'and', lst_key[k])
                    print(utest)
            return




        # Calculate and print the ANOVA result
        anova = stats.shapiro(self.df[dependent].dropna())
        print('Test statistic: {}\np-value: {}'.format(anova[0], anova[1]))

    def linear_regression(self):
        print()



# -Unit testing
# class TestFunctions(unittest.TestCase):



def menu():
    # Menu options
    menu = {1: "Choose a dataset", 2: "Test for distribution type",
            3: "Statistical analysis",4: "Linear regression",5: "Help", 6: "Exit"}
    # Display the menu description
    print('''
    #################### MENU ####################
    Input a command to use the function.
    E.g. Input 5 to use the [Help] command.

    The current dataset is: {} 
    '''.format('None' if not 'dataset_file' in globals() else dataset_file.filename))
    # Print the menu options
    for key in sorted(menu.keys()):
        print('    [{}] {}'.format(key, menu[key]))

    # Input the command and catch errors
    try:
        current_command = int(input('\nPlease select: '))
        if not 1 <= current_command <= 6:
            raise ValueError
    except ValueError:
        raise ValueError('Please enter an integer between 1 and 6.')

    # Run the selected command and catch errors
    try:
        if current_command == 1:
            choosing_dataset()
        if current_command == 2:
            dataset_file.distribution_test()
        if current_command == 3:
            dataset_file.stat_tests()
    except KeyError:
        raise KeyError('Please enter an integer between 1 and 6.')
    except ValueError:
        raise ValueError('Please choose a dataset before using this function.')

while True:
    try:
        menu()
    except ValueError as e:
        print(e)  # Don't raise error as the loop should restart later.



# if __name__ == '__main__':
#    unittest.main()
