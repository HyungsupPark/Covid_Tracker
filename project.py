#####################################
#             Parts 1-4             #
#####################################

#Enter code for Part1 below:
import csv

def parse_covid19(filename):
    '''
    (str) -> dictionary of form: {str: [(str, int), (str, int), ...], ...}
    Given a csv filename, the function creates and returns a dictionary 
    that stores the date and number of confirmed cases of the date for each country
    '''
    # initialize dictionary
    country_confirmed_cases = dict()
    
    # read csvfile
    with open(filename, 'r') as csvfile:
        covid19_cases = csv.reader(csvfile)
        for row in covid19_cases:
            province = row[0]
            
            # skip header
            if province != "Province_State":
                country = row[1]
                date =  row[2]
                cases = int(row[3])                
                
                # country already in dictionary
                if country in country_confirmed_cases:
                
                    # iterate through data with counter and flag to find same date entry 
                    data = country_confirmed_cases[country]
                    index_counter = 0
                    same_date_found = False
                    for old_date, old_num_cases in data:
                        
                        # replace the same date entry by adding number of cases
                        if old_date == date:
                            cases += old_num_cases
                            data[index_counter] = (date, cases)
                            same_date_found = True
                        index_counter += 1
                    
                    # when no same date entry, append to data
                    if not same_date_found:
                        data.append((date, cases))
                
                # country first time entry
                else:
                    country_confirmed_cases[country] = [(date, cases)]
    
    # return dictionary
    return country_confirmed_cases

         
#Enter code for Part2 below:
def select_countries(country_names, covid19_data):
    '''
    (list of str, dict) -> dict
    The function returns a dictionary like the one inputted 
    but with keys that are only in the inputted list
    '''
    # initialize dictionary
    new_data = dict()
    for name in country_names:
        
        # add data from covid19 dictionary for specified countries
        if name in covid19_data:
            new_data[name] = covid19_data[name]
    
    # return new dictionary
    return new_data


#Enter code for Part3 below:
class Covid_Country:
    '''
    A class that stores all the COVID-19 data for a specified country
    '''
    # initialize class by storing country name and corresponding data
    def __init__(self, country_name=str(), covid19_data=dict()):
        '''
        (self, str, dict) -> NoneType
        Create a Covid_Country object given a country name and a dictionary as an input
        '''
        self.country_name = country_name
        daily_count = covid19_data[country_name]
        self.daily_count = daily_count
    
    # day_count method
    def day_count(self, date):
        '''
        (self, str) -> int
        Return the number of COVID-19 cases for the date of the country inputted
        '''
        # initialize list of dates
        date_list = list()
        
        # iterate through stored data
        for data in self.daily_count:
            
            # day_count is the number of cases of that country of the input date
            if date == data[0]:
                date_list.append(data[1])
                day_count = data[1]
        
        # if date entry does not exist for the country, return None
        if not date_list:
            day_count = None
        
        return day_count
        
#Enter code for Part4 below:
class Split_Node:
    '''
    A class that implements Covid_Country objects and organizes into a binary tree
    '''
    def __init__(self):
        '''
        (self) -> NoneType
        Create a Split_Node object
        '''
        
        # initialize Split_Node object
        self.split_number = float()
        self.countries = list()
        self.left = None
        self.right = None
    
    def build_tree(self, country_list, date):
        '''
        (list of Covid_Country objects, str) -> NoneType
        Creates a binary tree that organizes countries based on the split number of confirmed cases of a date
        '''
        # initialize sum and lists 1, 2, 3
        total = 0
        list1 = list()
        list2 = list()
        list3 = list()
        
        # assign split number
        for country in country_list:
            if country.day_count != None:
                total += country.day_count(date)
        self.split_number = total/len(country_list)
        
        # create list 1, 2, 3
        for country in country_list:
            if country.day_count(date) < 0.7*self.split_number:
                list1.append(country)
            elif country.day_count(date) > 1.3*self.split_number:
                list2.append(country)
            else:
                list3.append(country)
        
        # assign list3 to self.countries
        self.countries = list3
        
        # assign list1 to self.left
        if list1:
            self.left = Split_Node()
            self.left.countries = list1
            
            # recursive case
            self.left.build_tree(list1, date)
        
        # assign list2 to self.right
        if list2:
            self.right = Split_Node()
            self.right.countries = list2
            
            # recursive case
            self.right.build_tree(list2, date)
            
#####################################
#             Tests                 #
#####################################
def run_my_tests():
    '''
    (NoneType) -> NoneType
    Run the tests defined by the student
    '''
    
    # Change this variable to test different parts of the project.
    # Possible values: "Part 1", "Part 2", "Part 3", "Part 4", "all"
    test_what = "all" 

    # Tests for Part 1
    if test_what == "all" or test_what == "Part 1":
        
        # Use the csv file 'part1_test1.csv'
        part1_input = 'part1_test1.csv'
        part1_output = parse_covid19(part1_input)
        part1_expected_output = {'Afghanistan': [('2020-03-26', 2)], 'Armenia': [('2020-03-26', 2), ('2020-03-27', 3)], 'China': [('2020-03-26', 1100), ('2020-03-27', 1900)]}
        '''
        This test proves that the function returns a dictionary where the keys are the names of the countries, which in this test, are 'Afghanistan', 'Armenia', and 'China', and the values are a list of tuples of date and number of confirmed cases.
        Also, it shows the value of the dictionary is the sum of all confirmed cases of the day when a country has multiple entries on the same day, 
        as on 2020-03-26 and 2020-03-27, China and Armenia both have multiple entries, so the number of confirmed cases must be the sum of the confirmed cases of all entries on the 26th and 27th, respectively.
        Additionally, in the csv file used in this test, Afghanistan and Armenia do not have provinces in their entries, whereas China does have specified provinces.
        However, since the function will create a dictionary based on the country names under the second column no matter what comes under the Province column, this will not affect the output.
        '''

    # Tests for Part 2
    if test_what == "all" or test_what == "Part 2":
        
        # Use the same dictionary created from Part 1 Test
        part2_test_dict = {'Afghanistan': [('2020-03-26', 2)], 'Armenia': [('2020-03-26', 2), ('2020-03-27', 3)], 'China': [('2020-03-26', 1100), ('2020-03-27', 1900)]}
        
        # Test1: When the list of country names include a key in the input dictionary
        country_names1 = ["China", "Australia", "South Korea", "Taiwan"]
        part2_input1 = (country_names1, part2_test_dict)
        part2_output1 = select_countries(country_names1, part2_test_dict)
        part2_expected_output1 = {'China' : [('2020-03-26', 1100), ('2020-03-27', 1900)]}
        '''
        In the list of country names given, only China has an entry in the input dictionary. Therefore the function will return the same dictionary but only containing China's entry.
        '''
        
        # Test2: When the list of country names does not include a key in the input dictionary
        country_names2 = ["South Korea", "Taiwan"]
        part2_input2 = (country_names2, part2_test_dict)
        part2_output2 = select_countries(country_names2, part2_test_dict)
        part2_expected_output2 = dict()
        '''
        In the input list of country names, none of them have an entry in the input dictionary. Therefore the function will return an empty dictionary.
        '''

    # Tests for Part 3
    if test_what == "all" or test_what == "Part 3":
        
        # Use the same dictionary as Part 1 and 2
        part3_test_dict = {'Afghanistan': [('2020-03-26', 2)], 'Armenia': [('2020-03-26', 2), ('2020-03-27', 3)], 'China': [('2020-03-26', 1100), ('2020-03-27', 1900)]}
        
        # Test 1: Create Covid_Country object
        part3_input1and2 = ('China', part3_test_dict)
        China = Covid_Country('China', part3_test_dict)
        part3_output1 = China.country_name
        part3_expected_output1 = 'China'
        part3_output2a = China.daily_count
        part3_expected_output2a = [('2020-03-26', 1100), ('2020-03-27', 1900)]
        
        part3_test_dict['China'].append('a')
        part3_output2b = China.daily_count
        part3_expected_output2b = [('2020-03-26', 1100), ('2020-03-27', 1900), 'a']
        '''
        This test checks if the Covid_Country object is correctly constructed. Since we are allowed to assume that the country exists in the passed in dictionary,
        it is safe to just test for China, which is included in the dictionary. 
        The name of the country is China, in this case, and the daily_count object should be  [('2020-03-26', 1100), ('2020-03-27', 1900)], according to the given dictionary.
        Additionally, since China.daily_count is a alias to the value of the passed in dictionary, when the dictionary's value is muted, China.daily_count should be muted as well.
        '''
        
        # Test 2: Check day_count method when there is a date entry
        China = Covid_Country('China', part3_test_dict)
        part3_input3 = '2020-03-27'
        part3_output3 = China.day_count(part3_input3)
        part3_expected_output3 = 1900
        '''
        This test checks the day_count method when the date passed in is an entry in the Covid_Country object's daily_count attribute.
        Since '2020-03-27' is passed in, the outcome will be 1900.
        '''
        
        # Test 3: Check day_count method when there is no such date entry
        China = Covid_Country('China', part3_test_dict)
        part3_input4 = '2020-04-04'
        part3_output4 = China.day_count(part3_input4)
        part3_expected_output4 = None     
        '''
        This test checks the day_count method when the date passed in is not an entry in the Covid_Country object's daily_count attribute.
        Since '2020-04-04', which is not a date in the given Covid_Country object, is passed in, the outcome will be None.
        '''
        
    # Tests for Part 4
    if test_what == "all" or test_what == "Part 4":
        
        # Use the following dictionary and generated country list to set up the input
        part4_test_dict = {'Canada': [('2020-03-26', 9), ('2020-03-27', 12), ('2020-03-28', 45), ('2020-03-29', 45)], 'England': [('2020-03-26', 21), ('2020-03-27', 65), ('2020-03-28', 65), ('2020-03-29', 86)], 'China': [('2020-03-26', 60), ('2020-03-27', 73), ('2020-03-28', 331), ('2020-03-29', 331)]}
        
        Canada = Covid_Country('Canada', part4_test_dict)
        England = Covid_Country('England', part4_test_dict)
        China = Covid_Country('China', part4_test_dict)
        country_list = [Canada, England, China]
        
        # Test 1
        '''inputs:'''
        date1 = '2020-03-26'
        sp_node1 = Split_Node()
        sp_node1.build_tree(country_list, date1)
        '''outputs'''
        part4_test1_output1 = sp_node1.split_number
        part4_test1_output2 = sp_node1.countries[0].country_name
        part4_test1_output3 = sp_node1.left.split_number
        part4_test1_output4 = sp_node1.left.countries[0].country_name
        part4_test1_output5 = sp_node1.right.split_number
        part4_test1_output6 = sp_node1.right.countries[0].country_name
        '''expected outputs'''
        part4_test1_expected_output1 = 30.0
        part4_test1_expected_output2 = 'England'
        part4_test1_expected_output3 = 9.0
        part4_test1_expected_output4 = 'Canada'
        part4_test1_expected_output5 = 73.0
        part4_test1_expected_output6 = 'China'  
        '''
        Test 1 shows that a Covid_Country object will be assigned to the left child when it is only strictly less than 0.7 times the split number,
        as England's day_count is exactly 0.7 times the split number.
        '''
        
        # Test 2
        '''inputs:'''
        date2 = '2020-03-27'
        sp_node2 = Split_Node()
        sp_node2.build_tree(country_list, date2)
        '''outputs'''
        part4_test2_output1 = sp_node2.split_number
        part4_test2_output2 = sp_node2.countries[0].country_name
        part4_test2_output3 = sp_node2.left.split_number
        part4_test2_output4 = sp_node2.left.countries[0].country_name
        part4_test2_output5 = sp_node2.right.split_number
        part4_test2_output6 = sp_node2.right.countries[0].country_name
        '''expected outputs'''
        part4_test2_expected_output1 = 50.0
        part4_test2_expected_output2 = 'England'
        part4_test2_expected_output3 = 12.0
        part4_test2_expected_output4 = 'Canada'
        part4_test2_expected_output5 = 73.0
        part4_test2_expected_output6 = 'China'        
        '''
        Test 2, similar to Test 1, shows that any Covid_Country will be assigned to the right child if it is only strictly larger than 1.3 times the split number,
        as England's day_count is exactly 1.3 times the split number.
        '''
        
        # Test 3
        '''inputs:'''
        date3 = '2020-03-28'
        sp_node3 = Split_Node()
        sp_node3.build_tree(country_list, date3)
        '''outputs'''
        part4_test3_output1 = sp_node3.split_number
        part4_test3_output2 = sp_node3.left.split_number
        part4_test3_output3 = sp_node3.left.countries[0].country_name
        part4_test3_output4 = sp_node3.left.countries[1].country_name
        part4_test3_output5 = sp_node3.right.split_number
        part4_test3_output6 = sp_node3.right.countries[0].country_name
        '''expected outputs'''
        part4_test3_expected_output1 = 147.0
        part4_test3_expected_output2 = 55.0
        part4_test3_expected_output3 = 'Canada'
        part4_test3_expected_output4 = 'England'
        part4_test3_expected_output5 = 331.0
        part4_test3_expected_output6 = 'China'
        '''
        This test demonstrates that a Split_Node object can store more than one element in its countries attribute if they share the same split number,
        as Canada and England both fall into the range of split number 55.0.
        '''
        
        # Test 4
        '''inputs:'''
        date4 = '2020-03-29'
        sp_node4 = Split_Node()
        sp_node4.build_tree(country_list, date4)
        '''outputs'''
        part4_test4_output1 = sp_node4.split_number
        part4_test4_output2 = sp_node4.left.split_number
        part4_test4_output3 = sp_node4.left.left.split_number
        part4_test4_output4 = sp_node4.left.left.countries[0].country_name
        part4_test4_output5 = sp_node4.left.right.split_number
        part4_test4_output6 = sp_node4.left.right.countries[0].country_name
        part4_test4_output7 = sp_node4.right.split_number
        part4_test4_output8 = sp_node4.right.countries[0].country_name
        '''expected outputs'''
        part4_test4_expected_output1 = 154.0
        part4_test4_expected_output2 = 65.5
        part4_test4_expected_output3 = 45.0
        part4_test4_expected_output4 = 'Canada'
        part4_test4_expected_output5 = 86.0
        part4_test4_expected_output6 = 'England'
        part4_test4_expected_output7 = 331.0
        part4_test4_expected_output8 = 'China'
        '''
        Test 4 demonstrates that the left or right atttribute of Split_Node object can assign a left or right attribute again,
        as Canada and England are two levels below the first split number.
        '''

# You can change the booleans below to decide if you want to run
# your tests or the visualization or both 

run_tests = False
run_visualization = True


#####################################
# Do not change anything below here #
#####################################
import matplotlib.pyplot as plt
from datetime import datetime
from project_helper import display_growth, display_tree


if __name__ == "__main__":

    if run_tests: 
        run_my_tests() 

    if run_visualization: 

        # load data via parse_covid19
        covid_dict = parse_covid19("Covid-19_data.csv")
        
        # select countries via select_countries 
        country_names = ["US","Italy","Spain","Germany"]
        sd = select_countries(country_names, covid_dict)
        
        # visualize graph via display_growth()
        display_growth(sd)
        
        # create Covid_country list 
        covid_countries = []
        date = '2020-03-21'
        for country in covid_dict:
            country = Covid_Country(country, covid_dict)
            if country.day_count(date):
                covid_countries.append(country)
        #for country in covid_dict:
        #    covid_countries.append(Covid_Country(country, covid_dict))
        
        #Create split_node and build tree
        date = '2020-03-21'
        sp_node = Split_Node()
        sp_node.build_tree(covid_countries,date)
        
        #Visualize the tree
        display_tree(sp_node, date)

