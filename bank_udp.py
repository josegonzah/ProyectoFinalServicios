from socketserver import BaseRequestHandler, ThreadingUDPServer
from sys import argv, exit

users = {'123456': ["pepito perez", 1234, 60000000]}
if len(argv) != 2:
    print("deme la ip")
    exit(1)

class bankhandleUdp(BaseRequestHandler):
    def handle(self):
        print("Hello bank")
        data, conn = self.request
        conn.sendto("501\n".encode(),self.client_address)
        data = data.decode().split(", ")
        cuenta = str(data[0])
        passw = int(data[1])
        money = int(data[2])
        if cuenta in users.keys():
            if users[cuenta][1] == passw:
                if users[cuenta][2] >= money:
                    users[cuenta][2] -= money
                    conn.sendto("True\n".encode(), self.client_address)
                else:
                    conn.sendto("False\n".encode(), self.client_address)
            else:
                conn.sendto("False\n".encode(), self.client_address)
        else:
            conn.sendto("False\n".encode(), self.client_address)
ip = str(argv[1])
udp = ThreadingUDPServer((ip, 7777), bankhandleUdp)
print("Hello")
udp.serve_forever()