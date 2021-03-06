# sys is to exit the quit_program
# user_interface is the a file for graphics
 # log controller is a a file for logging
import sys, user_interface, log_controller, bookmark_articles_db
# uses the api controoler to be used with the requests
from api_controller import ApiController

# creating variables that are easier to type
ui = user_interface
api = ApiController()
log_object = log_controller

# main program
def main():
    # calling the menu for user and calling the method
    menu_controller(ui.top_menu())



def menu_controller(menu_selection):

    # using a dictionary to control the selection from the user
    selection_dict = {
        '1': get_headlines,
        '2': get_all,
        '3': query_all_from_date_range,
        '4': display_bookmarked_data,
        'q': quit_program,
        'Q': quit_program,
    }

    # getting the user selection from user interface and calling related function
    call_function = selection_dict.get(menu_selection)

    # This checks to see if the selection is in the dictionary
    if menu_selection not in selection_dict:
        ui.message('Invalid Selection, Try Again')
        log_object.log_info_message('Tried to enter invalid selection.')
        main()

    # calling the method selected from menu if it valid
    else:
        call_function()


def get_headlines():
    # printing a message for the user to know what was selected
    ui.message("Search headlines for ?")
    # calling the query from api_controller.py
    execute_query('headlines')
    # after query returning to the menu
    main()

def get_all():
    ui.message("Search all articles for ?")
    # calling the query from api_controller.py
    execute_query('all')
    # returning to the main program after the query
    main()

def execute_query(query_type):

    # ui.message('in execute_query()')
    query_argument = ui.get_user_query()
    data = api.query_api(query_argument, query_type)


    try:
        # to print the information that is coming from the api
        for article in data:
            ui.message(article.__str__())

    except KeyError:
        # prints if nothing is returned in results
        # doesn't work?
        ui.message('Query found no results.')
        log_object.log_error_message('Queried newsapi. No results were fetched.')



def query_all_from_date_range():
    # TODO: while loop to ensure correct date input
    ui.message('Choose a date (bewteen now and 2016), format YYYY-MM-DD')
    # TODO: make a check for inside date range
    # TODO: Setup date query
    main()



def quit_program():
    sys.exit('Farewell digital world...\n')
    log_object.log_info_message('Closed the application.')

def display_bookmarked_data():
    print(bookmark_articles_db.get_bookmarked_data())


if __name__ == '__main__':
    main()
