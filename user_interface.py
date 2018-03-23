import log_controller

log_object = log_controller

def top_menu():

    message('''
        1) Search Headline Articles
        2) Search All Articles
        3) Search All Articles in Date-Range
        3) Exit
    ''')

    menu_selection = input('Select an option to continue.\n')

    return menu_selection



def get_user_query():

    query_parameter = input('Enter query term(s)\n')

    if query_parameter is None:
        message('Query cannot be empty. Enter your query.')
        log_object.log_info_message('Searched database with empty query string.')

    else:
        return query_parameter



def message(msg):

    print(msg + '\n')
