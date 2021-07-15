import sys, socket

print("Hello?")

try:
    rfc_number = int(sys.argv[1])
except (IndexError, ValueError):
    print('Must supply an RFC number as first argument')
    sys.exit(2)

print(rfc_number)

host = 'www.ietf.org'
port = 80
sock = socket.create_connection((host, port))

req = (
    f"""GET /rfc/rfc{rfc_number}.txt HTTP/1.1\r\nHost: {host}:{port}\r\n'User-Agent: Python {sys.version_info[0]}\r\nConnection: close\r\n\r\n"""
)
print(req)
sock.sendall(req.encode('ascii'))
rfc_raw = bytearray()

while True:
    buf = sock.recv(4096)
    print(buf)
    if not len(buf):
        break
    rfc_raw += buf
rfc = rfc_raw.decode('utf-8')
print(rfc)