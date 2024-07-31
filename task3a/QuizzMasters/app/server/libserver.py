import io
import selectors
import json
import struct
import sys

from database import pool
from handle_request import HandleRequest

class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.send_buffer = b""
        self.recv_buffer = b""
        self._json_header_length_ = None
        self._json_header_ = None
        self.request = None
        self.response_created = False

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

        if self._json_header_length_ is None:
            self.process_proto_header()

        if self._json_header_length_ is not None:
            if self._json_header_ is None:
                self.process_json_header()


        if self._json_header_:
            if self.request is None:
                self.process_request()

    def _read(self):
        try:
            data = self.sock.recv(4096)
        except BlockingIOError:
            pass
        else:
            if data:
                self.recv_buffer += data
            else:
                raise RuntimeError("Peer Closed....")

    def process_proto_header(self):
        hdrlen = 2
        if len(self.recv_buffer) >= hdrlen:
            self._json_header_length_ = struct.unpack(">H", self.recv_buffer[:hdrlen])
            self.recv_buffer = self.recv_buffer[hdrlen:]


    def process_json_header(self):
        hdrlen = self._json_header_length_[0]
        if len(self.recv_buffer) >= hdrlen:
            self._json_header_ = self._json_decode(self.recv_buffer[:hdrlen], "utf-8")
            self.recv_buffer = self.recv_buffer[hdrlen:]

            for reqhdr in ["byteorder", "content-type", "content-length", "content-encoding"]:
                if reqhdr not in self._json_header_:
                    raise ValueError(f"Missing required header {reqhdr}")

    def process_request(self):
        content_length = self._json_header_["content-length"]
        if len(self.recv_buffer) >= content_length:
            data = self.recv_buffer[:content_length]
            self.recv_buffer = self.recv_buffer[content_length:]
            if self._json_header_["content-type"] == "text/json":
                encoding = self._json_header_["content-encoding"]
                self.request = self._json_decode(data, encoding)
                print(f"Received request from {self.addr} ")
            else:
                self.request = data
                print(f"Received {self._json_header_['content-type']!r} request from {self.addr}")

            self._set_selector_event_mask_("w")

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(io.BytesIO(json_bytes), encoding=encoding, newline="")
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _set_selector_event_mask_(self, mode):

        if mode == 'w':
            events = selectors.EVENT_WRITE
        elif mode == 'r':
            events = selectors.EVENT_READ
        elif mode == 'rw':
            events = selectors.EVENT_WRITE | selectors.EVENT_READ
        else:
            raise ValueError(f"Invalid event mask mode {mode!r}")
        self.selector.modify(self.sock, events, data=self)

    def write(self):
        if self.request is not None:
            if not self.response_created:
                self._create_response()

        self._write()

    def _create_response(self):
        response = self._create_response_json_content()
        message = self._create_message(**response)
        self.response_created = True
        self.send_buffer += message

    def _create_response_json_content(self):
        action = self.request.get("action")
        value = self.request.get("value")

        result = HandleRequest(action, value, pool).decision()
        content = {"result": result}
        content_encoding = "utf-8"
        response = {
            "content_type": "text/json",
            "content_bytes": self._json_encode(content, content_encoding),
            "content_encoding": content_encoding
        }
        return response

    def _json_encode(self, json_bytes, encoding):
        return json.dumps(json_bytes, ensure_ascii=False).encode(encoding)


    def _create_message(self, content_bytes, content_type, content_encoding):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-length": len(content_bytes),
            "content-encoding": content_encoding
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def _write(self):
        if self.send_buffer:
            print(f"Sending data {self.send_buffer} to connection {self.addr}")
            try:
                sent = self.sock.send(self.send_buffer)
            except BlockingIOError:
                pass
            else:
                self.send_buffer = self.send_buffer[sent:]
                if sent and not self.send_buffer:
                    print("sent")
                    self.close()

    def close(self):
        print(f"Closing connection to {self.addr}")
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(f"Error: selector.unregister() exception for {self.addr}: {e}")
        try:
            self.sock.close()
        except OSError as e:
            print(f"Error: socket.close() exception for {self.addr}: {e}")
        finally:
            self.sock = None


