# This is a python include file
from unittest import TestCase
# This is the application mangager.py in project4
from application_manager import menu_controller,get_headlines,get_all,execute_query, query_all_from_date_range,quit_program

# main testing class to be used by python
class TestAppMan(unittest.TestCase):

    # a test to ensure the menu controller works proper
    def test_menu_controller(self):
        # TODO:test to check to see if dictionary selection are coming back correctly

        # TODO: input something to check the if not in dictionary

        # TODO comment out when test is writen
        pass

    def test_get_headlines(self):
        # TODO: don't think we really need to test this one?
        # TODO comment out when test is writen
        pass

    def test_get_all(self):
        # TODO: same thing as get headlines, don't think we have anything to test?
        # TODO comment out when test is writen1
        pass

    def test_execute_query(self):
        # TODO: inset query argument and query type

        # TODO: test to see that article.__str__() returns stuff that contains query argument

        # TODO: test to ensure keyError

    def test_quit_program(self):
        #TODO: test to ensure statement Farewell digital world...is showen

        
