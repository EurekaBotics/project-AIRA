import socket
print("Hello")
s = socket.socket()

host = '192.168.0.161'

port = 12345
s.bind((host, port))
s.listen(5)

while True:
    c, addr = s.accept()
    print("Got connection", addr)
    c.send('Thanks')
    c.close()