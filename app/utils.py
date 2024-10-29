import inquirer


coming_soon = lambda: print("Choice coming soon!")

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
