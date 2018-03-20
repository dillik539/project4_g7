

def top_menu():

    message('''
        1) Search Headline Articles
        2) Search All Articles
        3) Search All Articles in Date-Range
        q) Exit
    ''')

    menu_selection = input('Select an option to continue.\n')

    if menu_selection not in ['1', '2', '3', 'q']:
        message('Invalid selection. Try again.')
        top_menu()

    else:
        return menu_selection



def get_user_query():

    query_parameter = input('Enter query term(s)\n')

    if query_parameter is None:
        message('Query cannot be empty. Enter your query.')

    else:
        return query_parameter



def message(msg):
    print(msg + '\n')
