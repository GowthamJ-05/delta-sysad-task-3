import os
import socket
import selectors
import traceback

import libserver


sel = selectors.DefaultSelector()
hostname = os.environ["HOSTNAME"] or 'localhost'
host = socket.gethostbyname(hostname)
port = os.environ["PORT"] or 5000


lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, int(port)))
lsock.listen()
lsock.setblocking(False)
print(f"Starting server....Listening at {host, port} ")
sel.register(lsock, selectors.EVENT_READ, data=None)

def accept_wrapper(sock, selector):
    conn, addr = sock.accept()
    conn.setblocking(False)
    print(f"Accepted connection from {addr}")
    message = libserver.Message(sel, conn, addr)
    selector.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=message)


try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj, sel)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    message.close()
except KeyboardInterrupt:
    print("Keyboard Interrupt detected.... Exiting")
finally:
    sel.close()
