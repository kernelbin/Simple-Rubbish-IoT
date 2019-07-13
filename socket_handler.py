from threading import Thread
import socket
from packet_handler import pack, unpack, packets
import traceback
import time


class SocketHandler(Thread):

    def __init__(self, host, port, *args, **kwargs):
        Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET)
        self.running = True
        self.breaking = False
        self.host = host
        self.port = port
        self.connected = False
        self.on_connected = lambda: 1
        self.last_heartbeat = 0

    def run(self):
        while self.running:
            try:
                self.socket.connect((self.host, self.port))
                self.last_heartbeat = time.time()
                print("Connected")
                self.connected = True
                self.on_connected()
                while self.running and not self.breaking:
                    try:
                        packid = int(self.socket.recv(1))
                        packet_length = int.from_bytes(
                            self.socket.recv(4), "little")
                        packet_body = self.socket.recv(packet_length)
                        format_string, func = packets[packid]
                        func(*unpack(format_string, packet_body))
                    except Exception as ex:
                        # print(ex)
                        print("Packet recv failed..")
                        print(traceback.format_exc())
                self.breaking = False
            except Exception as ex:
                print("Connect failed...retrying...")
                print(traceback.format_exc())
            self.connected = False

    def update_server_heartbeat(self):
        self.last_heartbeat = time.time()

    def send_packet(self, pack_id, format_string="", *args):
        print(f"Sending {pack_id} {format_string} {args}")
        body = pack(format_string, *args)
        head = pack("BI", pack_id, len(body))
        self.socket.send(head+body)

    def send_login(self, uuid):
        self.send_packet(0x01, "s", uuid)

    def send_heartbeat(self):
        self.send_heartbeat(0x02, "")

    def send_process_success(self, userid, processid, rubbish_type):
        self.send_packet(0x03, "Iss", userid, processid, rubbish_type)

    def close(self):
        self.socket.close()
        self.running = False
        self.breaking = True
