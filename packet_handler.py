from collections import namedtuple
# 包ID -> (格式化字符串,处理函数)
packets = {}

Handler = namedtuple("Handler", "format_string handler")


def unpack(format, bytes: bytes) -> tuple:
    ret = []
    ptr = 0

    for char in format:
        if char == "i":
            ret.append(int.from_bytes(bytes[ptr:ptr+4], "little", signed=True))
            ptr += 4
        elif char == "I":
            ret.append(int.from_bytes(
                bytes[ptr:ptr+4], "little", signed=False))
            ptr += 4
        elif char == "h":
            ret.append(int.from_bytes(bytes[ptr:ptr+2], "little", signed=True))
            ptr += 2
        elif char == "H":
            ret.append(int.from_bytes(
                bytes[ptr:ptr+2], "little", signed=False))
            ptr += 2
        elif char == "b":
            ret.append(int.from_bytes(bytes[ptr:ptr+1], "little", signed=True))
            ptr += 1
        elif char == "B":
            ret.append(int.from_bytes(
                bytes[ptr:ptr+1], "little", signed=False))
            ptr += 1
        elif char == "s":
            length = int.from_bytes(bytes[ptr:ptr+2], "little", signed=False)
            ptr += 2
            string = bytes[ptr:ptr+length].decode("utf-8")
            ptr += length
            ret.append(string)
    return tuple(ret)


def pack(format, *args) -> bytes:
    from io import BytesIO
    buf = BytesIO()
    ptr = 0
    for char in format:
        if char == "i":
            buf.write(int(args[ptr]).to_bytes(4, "little", signed=True))
        elif char == "I":
            buf.write(int(args[ptr]).to_bytes(4, "little", signed=False))
        elif char == "h":
            buf.write(int(args[ptr]).to_bytes(2, "little", signed=True))
        elif char == "H":
            buf.write(int(args[ptr]).to_bytes(2, "little", signed=False))
        elif char == "b":
            buf.write(int(args[ptr]).to_bytes(1, "little", signed=True))
        elif char == "B":
            buf.write(int(args[ptr]).to_bytes(1, "little", signed=False))
        elif char == "s":
            str_bytes = str(args[ptr]).encode("utf-8")
            buf.write(len(str_bytes).to_bytes(2, "little", signed=False))
            buf.write(str_bytes)

        ptr += 1
    return buf.getvalue()


def handle_broadcast(message):
    print("Broadcast: {}".format(message))


def handle_server_heartbeat():
    from main import socket_handler
    socket_handler.update_server_heartbeat()


packets[0x04] = Handler("s", handle_broadcast)
packets[0x05] = Handler("", handle_server_heartbeat)
