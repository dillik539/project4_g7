import sys, user_interface, log_controller
from api_controller import ApiController

ui = user_interface
api = ApiController()
log_object = log_controller


def main():
    menu_controller(ui.top_menu())



def menu_controller(menu_selection):

    selection_dict = {
        '1': execute_query('headlines'),
        '2': execute_query('all'),
        '3': query_all_from_date_range,
        'q': quit_program,
    }

    call_function = selection_dict.get(menu_selection)

    if menu_selection is None:
        ui.message('Invalid Selection, Try Again')
        log_object.log_info_message('Tried to enter invalid selection.')

    else:
        return call_function()



def execute_query(query_type):

    ui.message('in execute_query()')
    query_argument = ui.get_user_query()
    data = api.query_api(query_argument, query_type)

    try:
        for article in data:
            ui.message(article.__str__())

    except KeyError:
        ui.message('Query found no results.')
        log_object.log_error_message('Queried newsapi. No results were fetched.')



def query_all_from_date_range():
    ui.message('in query_all_from_date_range')



def quit_program():
    sys.exit('Farewell digital world...\n')
    log_object.log_info_message('Closed the application.')



if __name__ == '__main__':
    main()
