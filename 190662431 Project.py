# Import libraries
import pandas as pd
import os
from scipy import stats
from pandas.api.types import is_numeric_dtype

# Class and functions
# -choosing_dataset
def choosing_dataset():
    # Let dataset_file be global
    global dataset_file
    # Create a dataset object with an argument that receives input.
    dataset_file = dataset(str(input('\nPlease input a filename in .csv format: ')))

# -dataset class
class dataset:
    def __init__(self, filename):
        # Raise an error if filename is not a string
        if not isinstance(filename, str):
            raise TypeError('The filename is not a string.')
        # Raise an error if filename does exist
        if not os.path.isfile(filename):
            raise FileNotFoundError('No such file or directory. Please try again.')
        # Raise an error if filename is not in .csv format
        if filename[-4:] != '.csv':
            raise FileNotFoundError('Please choose a dataset file in .csv format.')
        # Assign filename to self.filename
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
        print('The {} variable {} is selected.'.format(var_type, var))
        return var

    def distribution_test(self):
        # Choose a dependent
        dependent = self.input_variable('distribution test', 'dependent')
        # Failed to select a variable will cause a value of None. In this case, we should end the execution of the function call.
        if dependent == None:
            return

        # Determine binomial data
        lst = self.df[dependent].dropna().values.tolist()
        # For a sorted list, if lst[0] != lst[-1], lst[0] + lst[-1] = len(lst) and lst[0] + lst[-1] = 1,
        # then the item values for the list might be binomial
        if lst.count(lst[0]) + lst.count(lst[-1]) == len(lst) and lst[0] != lst[-1] and lst[0] + lst[-1] == 1:
            # Save the type
            self.distribution[dependent] = [0, 0, 'binomial']
            print('The dependent is binomial. Skip the distribution test.')
            # Return from the fuction
            return
        else:
            print('The dependent is not binomial.')

        # Set a significance_level
        try:
            critical_val = float(input('\nPlease enter a critical value before running Shapiro-Wilk test: '))
        except ValueError:
            print('The critical value should be numeric')

        # Shapiro test
        # Return from the function if the dependent is not numeric because Shapiro test only takes numbers.
        if not is_numeric_dtype(self.df[dependent]):
            print('The dependent should be numeric for Shapiro-Wilk test .')
            return
        # Calculate and print the distribution result
        shapiro = stats.shapiro(self.df[dependent].dropna())
        print('Test statistic: {}\np-value: {}'.format(shapiro[0], shapiro[1]))

        # Print the comparison between p-value and critical value
        if shapiro[1] < critical_val:
            print(
                'The p-value for dependent is larger than critical value of {}, which rejects the normality test.'.format(
                    critical_val))
            self.distribution[dependent] =  [shapiro[0], shapiro[1], 'Gaussian']
        else:
            print(
                'The p-value for dependent is smaller than or equal to critical value of {}, which accepts the normality test.'.format(
                    critical_val))
            self.distribution[dependent] = [shapiro[0], shapiro[1], 'non-Gaussian']


    def stat_tests(self):
        # Reminder
        print('''Statistical tests will run with regards to the datatype of dependent.
        Please perform distribution test before starting this test.''')

        # Choose an independent
        independent = self.input_variable('statistical tests', 'independent')
        # Failed to select a variable will cause a value of None. In this case, we should end the execution of the function call.
        if independent == None:
            return
        # Choose a dependent
        dependent = self.input_variable('statistical tests', 'dependent')
        # Failed to select a variable will cause a value of None. In this case, we should end the execution of the function call.
        if dependent == None:
            return

        # If the dependent has no result for the distribution test, then the function should return.
        if not dependent in self.distribution.keys():
            print('Please run the distribution test before running statistical tests.')
            return

        # Binomial case
        if self.distribution[dependent][2] == 'binomial':
            print('\nChi-square test of independence:')
            # Create a contingency table that contains the observed frequencies
            observed = pd.crosstab(self.df[dependent].dropna(), self.df[independent].dropna())
            chi2 = stats.chi2_contingency(observed)
            # Print the chi-square test result
            print('Test statistic: {}  p-value: {}  Degree of freedom: {}\nExpected frequencies: {}'.format(*chi2))
            return

        # Before the cases for Gaussian and non-Gaussian,
        # extract independent groups and save their names
        group_name = list(self.df.dropna().groupby([independent]).groups.keys())
        # Make an empty group
        groups = {}
        # Group the dependent according to the independent subgroups
        for subgroup in group_name:
            groups[subgroup] = self.df.dropna().groupby([independent]).get_group(subgroup)[dependent].values.tolist()

        # Gaussian case
        if self.distribution[dependent][2] == 'Gaussian':
            print('\nANOVA analysis:')
            # Run ANOVA and print the result
            print(stats.f_oneway(*groups.values()))
            return
        # Non-Gaussian case
        if self.distribution[dependent][2] == 'non-Gaussian':
            print('\nMann-Whitney U test::')
            # Compare each two groups (Not repeatedly).
            lst_key = list(groups.keys())
            for i in range(len(lst_key)):
                for k in range(i + 1, len(lst_key)):
                    # Run U test and print the result
                    utest = stats.mannwhitneyu(groups[lst_key[i]], groups[lst_key[k]])
                    # Print the combination.
                    print(independent,lst_key[i],'and', lst_key[k])
                    # Print the U test result.
                    print(utest)
            return
# -Help
def helps():
    print(''' 
            Instructions:
            1. Input 1 in the menu to select a datafile in .csv format.
            2. Then input 2 in the menu to run the distribution test for dependent variable. 
            3. Select a dependent and a critical value. 
               If dependent is binomial, the test will skip and return a binomial datatype for dependent.
               In other cases, Shapiro-Wilk test will run and the function will return a Gaussian or non-Gaussian 
               datatype.
            4. Input 3 to run the statistical test. 
               Select an independent and a dependent.
               ANOVA, Mann-Whitney U test or Chi-square test will be automatically run depending on the datatype of
               dependent.    
    ''')
# -Menu
def menu():
    # Menu options
    menu = {1: "Choose a dataset ({})".format('None' if not 'dataset_file' in globals() else dataset_file.filename),
            2: "Test for distribution type",
            3: "Statistical analysis",4: "Help", 5: "Exit"}
    # Display the menu description
    print('''
    ################################### MENU ###################################
    Input a command to use the function. E.g. Input 4 to use the [Help] command.
    ''')
    # Print the menu options
    for key in sorted(menu.keys()):
        print('    [{}] {}'.format(key, menu[key]))

    # Input the command and catch errors
    try:
        current_command = int(input('\nPlease select: '))
        # Raise error when 1<= current_command <=5.
        if not 1 <= current_command <= 5:
            raise ValueError
    except ValueError:
        raise ValueError('Please enter an integer between 1 and 5.')

    # Run the selected command and catch errors
    try:
        if current_command == 1:
            choosing_dataset()
        if current_command == 2:
            dataset_file.distribution_test()
        if current_command == 3:
            dataset_file.stat_tests()
        if current_command == 4:
            helps()
        if current_command == 5:
            exit()
    except KeyError:
        raise KeyError('Please enter an integer between 1 and 5.')
    except NameError:
        raise NameError('Please choose a dataset before using this function.')

while True:
    try:
        # Run the menu
        menu()
    # The loop should restart after catching an error
    except ValueError as e:
        print(e)
    except KeyError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    except TypeError as e:
        print(e)
    except NameError as e:
        print(e)

# if __name__ == '__main__':
#    unittest.main()
