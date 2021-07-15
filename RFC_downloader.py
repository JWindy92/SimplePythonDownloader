import os, sys, socket, ssl

try:
    rfc_number = int(sys.argv[1])
except (IndexError, ValueError):
    print('Must supply an RFC number as first argument')
    sys.exit(2)

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
host = 'www.ietf.org'
port = 443
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_sock = context.wrap_socket(sock, server_hostname=host)
s_sock.connect((host, port))

req = (
f'GET /rfc/rfc{rfc_number}.txt HTTP/1.1\r\n'
f'Host: {host}:{port}\r\n'
f'User-Agent: Python {sys.version_info[0]}\r\n'
'Connection: close\r\n'
'\r\n'
)

s_sock.send(req.encode('ascii'))
rfc_raw = bytearray()
while True:
    buf = s_sock.recv(4096)
    if not len(buf):
        break
    rfc_raw += buf

rfc = rfc_raw.decode('utf-8')
print(rfc)

if not os.path.exists('./output'):
    os.makedirs('./output')

with open(f'./output/RFC_{rfc_number}.txt', "w") as outfile:
    outfile.write(rfc)