import inquirer
from database.current import get_current_data
from app.objects import RobotXP
from functools import wraps


coming_soon = lambda: print("Choice coming soon!\n")

def requires_level(min_level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            bot = get_current_data("bot")
            xp = bot['xp']
            level = RobotXP(xp).level
            if level < min_level:
                print(f"This unlocks at level {min_level}! \n")
                return False
            return func(*args, **kwargs)
        return wrapper
    return decorator

def choice_interface(ask, choice_structure: dict, self_returns=[]):
    choices = list(choice_structure.keys()) + ["Exit"]
    choose = [
        inquirer.List(
            'choice',
            message=ask,
            choices=choices,
        ),
    ]
    while True:
        make_choice = inquirer.prompt(choose)
        chosen = make_choice['choice']
        if chosen == "Exit":
            break
        choice_structure[chosen]()
        if chosen in self_returns:
            return chosen
    return "exited"


def search_interface(ask, search_query: list, retrieve_func, choice_filter= lambda x:x, query_num=5):
    length = len(search_query)
    page_number = 0
    total_pages = length//query_num
    print_page_number = lambda: print(f"Page {page_number}")
    
    next_page = "Next Page -->"
    prev_page = "<-- Previous Page"
    set_pages = {
        next_page: print_page_number,
        prev_page: print_page_number
    }

    def set_choice_interface(page_num):
        page = search_query[page_num*query_num: min(length, (page_num+1)*query_num)]
        choices = dict(zip([choice_filter(p) for p in page], [lambda: retrieve_func(obj["id"]) for obj in page]))

        if total_pages > page_num:
            set_pages[next_page] = print_page_number
        else: del set_pages[next_page]
        if page_num > 0:
            set_pages[prev_page] = print_page_number
        else: del set_pages[prev_page]
        
        return choice_interface(f"{ask} (Page:{page_num+1}/{total_pages+1})", {**choices, **set_pages}, self_returns=list(set_pages.keys()))

    choice = set_choice_interface(page_number)
    while choice != "exited":
        if choice == next_page:
            page_number += 1
        elif choice == prev_page:
            page_number -= 1
        choice = set_choice_interface(page_number)
