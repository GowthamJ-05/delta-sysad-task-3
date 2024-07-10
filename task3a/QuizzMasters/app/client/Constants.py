import sys

RED = "\033[31m"  # error color
GREEN = "\033[32m"  # answer is correct
YELLOW = "\033[33m"  # wrong answer
BLUE = "\033[34m"  # default theme color
WHITE = "\033[47m"  # default text color
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"
TAB = "\t"*4
welcome_statement = (f'{TAB}\t\t{UNDERLINE}{BOLD}{BLUE}Welcome to QuizzMasters{RESET}\n'
                     f'{TAB}To start playing you must have an account\n'
                     f'{TAB}>> {BOLD}{BLUE}LOGIN{RESET} - enter 1\n'
                     f'{TAB}>> {BOLD}{BLUE}CREATE ACCOUNT{RESET} - enter 2\n')

services = (
    f'{TAB} Do you want to:\n'
    f'{TAB}>> {BOLD}{BLUE}ADD A QUESTION{RESET} - enter 1\n'
    f'{TAB}>> {BOLD}{BLUE}ANSWER A QUESTION{RESET} - enter 2\n'
    f'{TAB}>> {BOLD}{BLUE}SEE LEADERBOARD{RESET} - enter 3\n'
    f'{TAB}>> {BOLD}{BLUE}EXIT{RESET} - enter 4\n'
)

# serverhost = os.environ.get("HOST") or '127.0.0.1'
# serverport = os.environ.get("PORT") or 5000
if len(sys.argv) != 3:
    print(f"USAGE: python3 {sys.argv[0]} <serverhost> <serverport>")
    sys.exit(1)

serverhost = sys.argv[1]
serverport = int(sys.argv[2])

