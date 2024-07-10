import socket
import sys

import libclient
from Constants import *

class Request:
    def __init__(self, action, value):
        self.action = action
        self.value = value
        self.host = None
        self.port = None
        self.request = None
        self.response = None

    def create_request(self):
        allowed_actions = ("login", "new", "add", "reqqn", "check", "see")
        if self.action in allowed_actions:
            content = {"action": self.action, "value": self.value}
            self.request = {
                    "content": content,
                    "type": "text/json",
                    "encoding": "utf-8"
                }
        else:
            print(f"{TAB}{RED}{BOLD}Request not sent due to unknown: {self.action}{RESET}")
            sys.exit(1)

    def start_connection(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.settimeout(5)
                sock.connect((self.host, self.port))

                # print("Starting connection to server....")
                success = libclient.send_request(sock, self.request)
                if success:
                    # print("Request made successfully, fetching response")
                    self.response = libclient.Get_response(sock).process_response()
                    if self.response is None:
                        print(f"{TAB}{RED}{BOLD}Failed to get any response.....{RESET}")
                else:
                    print(f"{TAB}{RED}{BOLD}Failed to send the request :({RESET}")
            except socket.timeout:
                self.response = {"result": f"{TAB}{RED}{BOLD}Connection timed out..{RESET}"}


    def sender(self, host, port):
        self.host = host
        self.port = port
        self.create_request()
        try:
            self.start_connection()
            return self.response
        except KeyboardInterrupt:
            print("Caught Keyboard Interruption... exiting ")


