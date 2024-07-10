import hashlib
import os
import json

from connection import Connection
from Constants import *

class HandleRequest:
    def __init__(self, action, value, pool):
        self.action = action
        self.value = value
        self.pool = pool
        self.allowed_action = ("login", "new", "add", "reqqn", "check", "see")
        self.error_msg = (f"{TAB}{BOLD}{RED}Internal server error. Try again later{RESET}",
                          f"{TAB}{RED}Username not found.{RESET}",
                          f"{TAB}{RED}Password incorrect{RESET}",
                          f"{TAB}{RED}Username already in use{RESET}")
        self.return_response = None
        

    def _generate_salt(self):
        return os.urandom(16)
    

    def _hasher(self, password, salt=None):
        if salt is None:
            salt = self._generate_salt()
        salted_password = salt + password.encode()
        return salt.hex()+hashlib.sha256(salted_password).hexdigest()


    def decision(self):
        if self.action == "login":
            self._login_handler()
        elif self.action == "new":
            self._newuser_handler()
        elif self.action == "add":
            self._addqn_handler()
        elif self.action == "reqqn":
            self._reqqn_handler()
        elif self.action == "check":
            self._checkans_handler()
        elif self.action == "see":
            self._seelead_handler()
        else:
            self.return_response = f"{TAB}{RED}Received an invalid action: {self.action}{RESET}"
        return self.return_response
    

    def _login_handler(self):
        login = self._login()
        if login:
            self.return_response = f"{TAB}{GREEN}User successfully authenticated{RESET}"
        return
    

    def _login(self):
        relevant_fields = ("username", "password")
        for field in relevant_fields:
            if field not in self.value:
                self.return_response = f"{TAB}{RED}Missing field: {field}{RESET}"
                return False
        username = self.value["username"]
        provided_password = self.value["password"]
        try:
            query = "select password from Userbase where username = %s"
            result = Connection(self.pool).accept_query(query, (username, ))
            if result is None:
                self.return_response = self.error_msg[1]
                return False
            else:
                stored_password = result[0]
                salt = bytes.fromhex(stored_password[:32])
                hashy = self._hasher(provided_password, salt)
                if stored_password != hashy:
                    self.return_response = self.error_msg[2]
                    return False
                else:
                    return True
        except Exception as e:
            print(f"Error: {e}")
            self.return_response = self.error_msg[0]
            return False
        

    def _newuser_handler(self):
        relevant_fields = ("new-username", "new-password")
        for field in relevant_fields:
            if field not in self.value:
                self.return_response = f"{TAB}{RED}Missing field: {field}{RESET}"
                return
        new_username = self.value["new-username"]
        new_password = self.value["new-password"]
        try:
            query = "select * from Userbase where username = %s"
            result = Connection(self.pool).accept_query(query, (new_username,))

            if result is not None:
                self.return_response = self.error_msg[3]
                return
            else:
                hashy = self._hasher(new_password)
                query = "insert into Userbase values (%s,%s)"
                Connection(self.pool).accept_query(query, (new_username, hashy))
                query = "insert into Leaderboard (username) values (%s)"
                Connection(self.pool).accept_query(query, (new_username,))
                self.return_response = f"{TAB}{GREEN}Successfully added username and password{RESET}"
        except Exception as e:
            print(f"Error: {e}")
            self.return_response = self.error_msg[0]
            return
        

    def _addqn_handler(self):
        login = self._login()
        if login:
            relevant_fields = ("add-question", "option1", "option2", "option3", "option4", "correct-option")
            for field in relevant_fields:
                if field not in self.value:
                    self.return_response = f"{TAB}{RED}Missing field: {field}{RESET}"
                    return
            username = self.value["username"]
            question = self.value["add-question"]
            option1 = self.value["option1"]
            option2 = self.value["option2"]
            option3 = self.value["option3"]
            option4 = self.value["option4"]
            correct_option = self.value["correct-option"]
            allotted_for = '[]'
            try:
                query = '''insert into QuestionBank (question, option1, option2, option3, option4, correct_option, 
                username, allotted_for) values (%s, %s, %s, %s, %s, %s, %s, %s)'''  # QuestionId for qns
                Connection(self.pool).accept_query(query, (question, option1, option2, option3, option4, correct_option, username, allotted_for))
                self.return_response = f"{TAB}{GREEN}Question added to question bank successfully{RESET}"
            except Exception as e:
                print(f"Error: {e}")
                self.return_response = self.error_msg[0]
        return

    def _reqqn_handler(self):
        login = self._login()
        if login:
            print('hello')
            username = self.value["username"]
            try:
                query = "select question, qid, option1, option2, option3, option4, allotted_for from QuestionBank where username != %s order by RAND() limit 1;"

                result = Connection(self.pool).accept_query(query, (username,))
                if result is None:
                    self.return_response = f"{TAB}{YELLOW}That's all for now...{RESET}"
                    return
                question, qid, option1, option2, option3, option4, allotted_for_json = result
                allotted_for = json.loads(allotted_for_json)
                if username not in allotted_for:
                    allotted_for.append(username)
                allotted_for_json = json.dumps(allotted_for)
                query = "update QuestionBank set allotted_for = %s where qid = %s"
                Connection(self.pool).accept_query(query, (allotted_for_json, qid))

                query = "update Leaderboard set number_qns = number_qns+1 where username = %s"
                Connection(self.pool).accept_query(query, (username, ))
                self.return_response = {'qid': qid, 'question': question, 'option1': option1, 'option2': option2,
                                        'option3': option3, 'option4': option4}
            except Exception as e:
                print(f"Error: {e}")
                self.return_response = self.error_msg[0]
        return
    

    def _checkans_handler(self):
        login = self._login()
        if login:
            relevant_fields = ("qid", "answered-option")
            for field in relevant_fields:
                if field not in self.value:
                    self.return_response = f"{TAB}{RED}Missing field: {field}{RESET}"
                    return
            username = self.value["username"]
            qid = self.value["qid"]
            answered_option = self.value["answered-option"]
            try:
                query = "select correct_option, allotted_for from QuestionBank where qid = %s  "
                result = Connection(self.pool).accept_query(query, (qid,))
                if result is None:
                    self.return_response = f"{TAB}{RED}The given qid: {qid} does not exist{RESET}"
                    return
                correct_option, allotted_for_json = result
                allotted_for = json.loads(allotted_for_json)
                if username not in allotted_for:
                    self.return_response = f"{TAB}{RED}The given qid: {qid} was not allotted for {username}{RESET}"
                    return
                if correct_option != answered_option:
                    self.return_response = f"{TAB}{RED}The answered option is incorrect. The correct option was {correct_option}{RESET}"

                    allotted_for.remove(username)  # HERE
                    allotted_for_json = json.dumps(allotted_for)
                    query = "update QuestionBank set allotted_for = %s where qid = %s"
                    Connection(self.pool).accept_query(query, (allotted_for_json, qid))
                    return
                else:
                    query = "update Leaderboard set points = points+3 where username = %s"
                    Connection(self.pool).accept_query(query, (username, ))
                    self.return_response = (f"{TAB}{GREEN}Congratulations! The answered-option is correct."
                                            f" You have acquired 3 points{RESET}")

                    allotted_for.remove(username)  # HERE
                    allotted_for_json = json.dumps(allotted_for)
                    query = "update QuestionBank set allotted_for = %s where qid = %s"
                    Connection(self.pool).accept_query(query, (allotted_for_json, qid))
            except Exception as e:
                print(f"Error: {e}")
                self.return_response = self.error_msg[0]
        return


    def _seelead_handler(self):
        login = self._login()
        if login:
            username = self.value["username"]
            try:
                query = "select points, number_qns, (select COUNT(*)+1 from Leaderboard where points > l.points) from Leaderboard l where username = %s"
                result = Connection(self.pool).accept_query(query, (username,))
                return_response_dict = {"you": result}

                query = "select username, points, number_qns from Leaderboard order by points desc limit 3"
                result = Connection(self.pool).accept_query(query)

                if isinstance(result, tuple):
                    return_response_dict[f"{TAB}{YELLOW}{BOLD}Rank 1{RESET}"] = result
                else:
                    index = 1
                    p = None
                    for tup in result:
                        print(tup)
                        print(p, tup[1])
                        if p == tup[1]:
                            j = index-1
                            rank_list = list(tup)
                            rank_list.append(f"{TAB}{YELLOW}{BOLD}rank {j}{RESET}")
                            return_response_dict[index] = rank_list
                        else:   # f"{TAB}{YELLOW}{BOLD}Rank {i}{RESET}"
                            rank_list = list(tup)
                            rank_list.append(f"{TAB}{YELLOW}{BOLD}rank {index}{RESET}")
                            return_response_dict[index] = rank_list
                        p = tup[1]
                        index += 1
                self.return_response = return_response_dict
            except Exception as e:
                print(f"Error: {e}")
                self.return_response = self.error_msg[0]
        return

