import io
import struct
import json
import sys

def send_request(sock, request):
    try: 
        content_byte = request["content"]
        content_type = request["type"]
        content_encoding = request["encoding"]
        content = {
            "content_byte": content_byte,
            "content_encoding": content_encoding,
            "content_type": content_type
        }
        message = create_message(**content)
        write(sock, message)
        return True
    except Exception as e:
        print(f"Exception {e} occured")
        return False
        
    
def create_message(content_byte, content_type, content_encoding):
    
    content = json_encode(content_byte, content_encoding)
    content_length = len(content)
    header_json = create_header_json(content_type, content_encoding, content_length)
    header_json_length = len(header_json)
    header_fixed = create_header_fixed(header_json_length)

    message = header_fixed + header_json + content 
    return message

def json_encode(json_content, encoding):
    return json.dumps(json_content, ensure_ascii=False).encode(encoding)

def create_header_json(content_type, content_encoding, content_length):
    jsonheader = {
        "content-type": content_type,
        "byteorder": sys.byteorder,
        "content-length": content_length,
        "content-encoding": content_encoding,
    }
    return json_encode(jsonheader, "utf-8")

def create_header_fixed(jsonlength):
    return struct.pack(">H", jsonlength)

def write(sock, message):
    sock.sendall(message)


class Get_response:
    def __init__(self, sock):
        self.sock = sock
        self.message = b""
        self.recv_buffer = b""
        self.json_header_len = None
        self.json_header = None
        self.sock_closed = False
        self.response = None


    def process_response(self):
        while True:
            try:
                self.read()

                if self.recv_buffer:
                    if self.json_header_len is None:
                        self.process_fixedheader()

                    if self.json_header_len is not None:
                        if self.json_header is None:
                            self.process_jsonheader()

                    if self.json_header is not None:
                        self.process_content()

                    if self.response:
                        self.close()

                if self.sock_closed:
                    break
            except Exception as e:
                break
        return self.response

    def read(self):
        data = self.sock.recv(4096)
        if data:
            self.recv_buffer += data
        else:
            print("Server connection terminated.....")
            self.close() 

    def process_fixedheader(self):
        hdrlen = 2
        if len(self.recv_buffer) >= hdrlen:
            self.json_header_len = struct.unpack(">H", self.recv_buffer[:hdrlen])[0]
            self.recv_buffer = self.recv_buffer[hdrlen:]


    def process_jsonheader(self):
        hdrlen = self.json_header_len
        if len(self.recv_buffer) >= hdrlen:
            self.json_header = self.json_decode(self.recv_buffer[:hdrlen], "utf-8")
            self.recv_buffer = self.recv_buffer[hdrlen:]

            for reqhdr in ("byteorder", "content-type", "content-encoding", "content-length"):
                if reqhdr not in self.json_header:
                    print(f"Required header {reqhdr} missing"
                          f"Exiting .....")
                    self.close()

    def process_content(self):
        content_length = self.json_header["content-length"]
        encoding = self.json_header["content-encoding"]
        if len(self.recv_buffer) >= content_length:
            self.response = self.json_decode(self.recv_buffer[:content_length], encoding)

    def json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(io.BytesIO(json_bytes), encoding=encoding, newline="")
        obj = json.load(tiow)
        tiow.close()
        return obj
    
    def close(self):
        try:
            self.sock.close()
        except OSError as e:
            print(f"Error: socket.close() exception : {e!r}")
        finally:
            self.sock = None
            self.sock_closed = True
