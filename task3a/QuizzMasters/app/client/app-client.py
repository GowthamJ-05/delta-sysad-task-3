import sys

from Constants import *
from requestsender import Request


def login_choice():
    global username, password
    username, password = None, None
    choice = input(f"{TAB}{BLUE}Enter your Choice (1/2): {RESET}")

    if choice == '1':
        login_func()
        print()
    elif choice == '2':
        create_account_func()
    else:
        print(f"{TAB}{RED}invalid input... Enter again{RESET}\n")
        login_choice()


def login_func():
    global username, password
    username = input(f"\n{TAB}{BLUE}Enter Username: {RESET}")
    password = input(f"{TAB}{BLUE}Enter password: {RESET}")
    value = {"username": username, "password": password}
    res = Request("login", value).sender(serverhost, serverport)
    print(res["result"])
    if res["result"] == f"{TAB}{RED}Username not found.{RESET}" or res["result"] == f"{TAB}{RED}Password incorrect{RESET}":
        choice = input(f"{TAB}{BLUE}Do you want to retry? (y/n): ")
        if choice == 'y' or choice == 'Y':
            login_func()
        else:
            print(welcome_statement)
            login_choice()
    elif res["result"] == f"{TAB}{GREEN}User successfully authenticated{RESET}":
        print(services)
        service_choice()
    else:
        print(welcome_statement)
        login_choice()
    return

def create_account_func():
    global username, password
    username = input(f"\n{TAB}{BLUE}Enter new username: {RESET}")
    password = input(f"{TAB}{BLUE}Enter password: {RESET}")
    value = {"new-username": username, "new-password": password}
    res = Request("new", value).sender(serverhost, serverport)
    print(res["result"])
    if res["result"] == f"{TAB}{RED}Username already in use{RESET}":
        choice = input(f"{TAB}{BLUE}Do you want to retry? (y/n): ")
        if choice == 'y' or choice == 'Y':
            create_account_func()
        else:
            print(welcome_statement)
            login_choice()
    elif res["result"] == f"{TAB}{GREEN}Successfully added username and password{RESET}":
        print(services)
        service_choice()
    else:
        print(welcome_statement)
        login_choice()
    return

def service_choice():
    choice = input(f"{TAB}{BLUE}Enter your Choice (1/2/3/4): {RESET}")
    if choice == '1':
        add_qn_func()
    elif choice == '2':
        ans_qn_func()
    elif choice == '3':
        see_leaderboard_func()
    elif choice == '4':
        exit_func()
    else:
        print(f"{TAB}{RED}invalid input... Enter again{RESET}\n")
        service_choice()

def add_qn_func():
    question = input(f"\n{TAB}{BLUE}Enter the question: {RESET}")
    option1 = input(f"{TAB}{BLUE}Enter option 1: {RESET}")
    option2 = input(f"{TAB}{BLUE}Enter option 2: {RESET}")
    option3 = input(f"{TAB}{BLUE}Enter option 3: {RESET}")
    option4 = input(f"{TAB}{BLUE}Enter option 4: {RESET}")
    correct_option = input(f"{TAB}{BLUE}Enter the correct option: {RESET}")
    value = {
        "username": username,
        "password": password,
        "add-question": question,
        "option1": option1,
        "option2": option2,
        "option3": option3,
        "option4": option4,
        "correct-option": correct_option,
    }
    res = Request("add", value).sender(serverhost, serverport)
    print(res["result"])
    print(services)
    service_choice()


def ans_qn_func():
    value = {
        "username": username,
        "password": password,
    }
    res = Request("reqqn", value).sender(serverhost, serverport)
    result = res["result"]

    if isinstance(result, dict):
        try:
            qid = result['qid']
            question = result['question']
            option1 = result['option1']
            option2 = result['option2']
            option3 = result['option3']
            option4 = result['option4']
            print(f"{TAB}>> {BOLD}{BLUE}{question}{RESET}")
            print(f"{TAB}{BLUE}Option1: {RESET}", option1)
            print(f"{TAB}{BLUE}Option2: {RESET}", option2)
            print(f"{TAB}{BLUE}Option3: {RESET}", option3)
            print(f"{TAB}{BLUE}Option4: {RESET}", option4)
            answer_choice = ans_choice()
            value["qid"] = qid
            value["answered-option"] = answer_choice
            res = Request("check", value).sender(serverhost, serverport)
            print(res["result"])
            print(services)
            service_choice()
        except KeyError:
            print(f"{TAB}{RED}Received an incomplete response{RESET}")
            print(services)
            service_choice()
    else:
        print(res["result"])
        print(services)
        service_choice()


def ans_choice():
    answer = input(f"{TAB}{BLUE}Enter your answer (1/2/3/4): {RESET}")
    if answer not in ['1', '2', '3', '4']:
        print(f"{TAB}{RED}invalid answer... Enter again{RESET}\n")
        ans_choice()
    else:
        return int(answer)

def see_leaderboard_func():
    value = {
        "username": username,
        "password": password,
    }
    res = Request("see", value).sender(serverhost, serverport)
    result = res["result"]
    if isinstance(result, dict):
        try:
            print(f"{TAB}{GREEN}Your Position: {result['you'][2]}")
            print(f"{TAB}Points scored: {result['you'][0]}")
            print(f"{TAB}Number of Questions Attempted: {result['you'][1]}{RESET}")

            for toppers in result:
                if toppers != 'you':
                    print(result[toppers][3])
                    print(f"{TAB}{YELLOW}Username: {RESET}", result[toppers][0])
                    print(f"{TAB}{YELLOW}Points: {RESET}", result[toppers][1])
                    print(f"{TAB}{YELLOW}Number 0f Questions Answered: {RESET}", result[toppers][2])

            print(services)
            service_choice()
        except KeyError:
            print(f"{TAB}{RED}Received an incomplete response{RESET}")


def exit_func():
    print(f"{TAB}{BOLD}{BLUE}Sorry to see you leave....{RESET}")
    sys.exit()


try:
    print(welcome_statement)
    login_choice()
except KeyboardInterrupt:
    exit_func()
except Exception:
    sys.exit()

