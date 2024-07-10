import hashlib
import json
import os

# from connection import Connection
# from database import pool

# def _generate_salt():
#     return os.urandom(16)
#
#
# def _hasher(password, salt=None):
#     if salt is None:
#         salt = _generate_salt()
#     salted_password = salt + password.encode()
#     print(salt)
#     return salt.hex() + hashlib.sha256(salted_password).hexdigest()


# query = "select password from Userbase where username = %s"
# result = Connection(pool).accept_query(query, ('root', ))
# provided_password = "myrootpassword"
# print(result)
#
# stored_password = result[0]
# salt = bytes.fromhex(stored_password[:32])
# hashy = _hasher(provided_password, salt)
#
# if hashy == stored_password:
#     print('Well done')

# try:
#     query = "select * from Userbase where username = %s"
#     result = Connection(pool).accept_query(query, ("delta",))
#
#     if result is not None:
#         # return_response = self.error_msg[3]
#         print("result is not None")
#     else:
#         hashy = _hasher('mydeltaforcepassword')
#         query = "insert into Userbase values (%s,%s)"
#         Connection(pool).accept_query(query, ("force", hashy))
#         query = "insert into Leaderboard (username) values (%s)"
#         Connection(pool).accept_query(query, ("force",))
#         print("success")
#         # self.return_response = f"{TAB}{GREEN}Successfully added username and password{RESET}"
# except Exception as e:
#     print(f"Error: {e}")
    # self.return_response = self.error_msg[0]
    # return

# username = "delta"
# question = "Are you gojo because you are the strongest or are you strong because you are gojo "
# option1 = "go/jo"
# option2 = "jo/go"
# option3 = "go/go"
# option4 = "jo/jo"
# correct_option = 2
# allotted_for = json.dumps([])
# try:
#     query = '''insert into QuestionBank (question, option1, option2, option3, option4, correct_option,
#     username, allotted_for) values (%s, %s, %s, %s, %s, %s, %s, %s)'''  # QuestionId for qns
#     Connection(pool).accept_query(query, (question, option1, option2, option3, option4, correct_option, username, allotted_for))
#     print('success')
#     # self.return_response = f"{TAB}{GREEN}Question added to question bank successfully{RESET}"
# except Exception as e:
#     print(f"Error: {e}")
#     # self.return_response = self.error_msg[0]


# try:
#     query = ("select qid, question, option1, option2, option3, option4, allotted_for from QuestionBank where username != %s order by RAND() limit 1;")
#     result = Connection(pool).accept_query(query, ('force',))
#     print(result)
#     if result is None:
#         # self.return_response = f"{TAB}{YELLOW}The question bank is empty ... but you can add questions{RESET}"
#         print("Question Bank is empty")
#     qid, question, option1, option2, option3, option4, allotted_for_json = result
#     allotted_for = json.loads(allotted_for_json)
#     if 'force' not in allotted_for:
#         allotted_for.append('force')
#     allotted_for_json = json.dumps(allotted_for)
#     query = "update QuestionBank set allotted_for = %s where qid = %s"
#     Connection(pool).accept_query(query, (allotted_for_json, qid))
#
#     query = "update Leaderboard set number_qns = number_qns+1 where username = %s"
#     Connection(pool).accept_query(query, ('force',))
#     # self.return_response = {'qid': qid, 'question': question, 'option1': option1, 'option2': option2,
#     #                         'option3': option3, 'option4': option4}
# except Exception as e:
#     print(f"Error: {e}")
#     # self.return_response = self.error_msg[0]


# username = 'force'
# qid = 3
# answered_option = 2
# try:
#     query = "select correct_option, allotted_for from QuestionBank where qid = %s  "
#     result = Connection(pool).accept_query(query, (qid,))
#     if result is None:
#         # self.return_response = f"{TAB}{RED}The given qid: {qid} does not exist{RESET}"
#         print("The qid DNE")
#         exit()
#     correct_option, allotted_for_json = result
#     allotted_for = json.loads(allotted_for_json)
#     if username not in allotted_for:
#         # self.return_response = f"{TAB}{RED}The given qid: {qid} was not allotted for {username}{RESET}"
#         print("The qid is not allotted for you")
#         exit()
#     if correct_option != answered_option:
#         # self.return_response = f"{TAB}{RED}The answered option is incorrect. The correct option was {correct_option}{RESET}"
#         print("Incorrect")
#         allotted_for.remove(username)  # HERE
#         allotted_for_json = json.dumps(allotted_for)
#         query = "update QuestionBank set allotted_for = %s where qid = %s"
#         Connection(pool).accept_query(query, (allotted_for_json, qid))
#         exit()
#     else:
#         query = "update Leaderboard set points = points+3 where username = %s"
#         Connection(pool).accept_query(query, (username,))
#         print("Success")
#         allotted_for.remove(username)  # HERE
#         allotted_for_json = json.dumps(allotted_for)
#         query = "update QuestionBank set allotted_for = %s where qid = %s"
#         Connection(pool).accept_query(query, (allotted_for_json, qid))
#         # self.return_response = (f"{TAB}{GREEN}Congratulations! The answered-option is correct."
#         #                         f" You have acquired 3 points{RESET}")
# except Exception as e:
#     print(f"Error: {e}")
#     # self.return_response = self.error_msg[0]

# username = 'force'
# try:
#     # HERE
#     query = "select points, number_qns, (select COUNT(*)+1 where points > l.points) from Leaderboard l where username = %s"
#     result = Connection(pool).accept_query(query, (username,))
#     return_response_dict = {"you": result}
#
#     query = "select username, points, number_qns from Leaderboard order by points desc limit 3"
#     result = Connection(pool).accept_query(query)
#     i = 1
#     print(result)
#     if isinstance(result, tuple):
#         return_response_dict["Rank 1"] = result
#     else:
#         for tup in result:
#             string = f"Rank {i}"
#             return_response_dict[string] = tup
#             i += 1
#     print(return_response_dict)
#     # self.return_response = return_response_dict
# except Exception as e:
#     print(f"Error: {e}")
#     # self.return_response = self.error_msg[0]

# from requestsender import Request
#
# value = {'username': 'force', 'password': 'mydeltaforcepassword'}
# serverhost = '127.0.0.1'
# serverport = 5000
# res = Request("reqqn", value).sender(serverhost, serverport)
# print(res)
