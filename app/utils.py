import inquirer


coming_soon = lambda: print("Choice coming soon!")

def choice_interface(ask, choice_structure: dict):
    choices = list(choice_structure.keys()) + ["exit"]
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
        if chosen == "exit":
            break
        func = choice_structure[chosen]()
        if func:
            break
