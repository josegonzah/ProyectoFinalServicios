from socketserver import ThreadingTCPServer, BaseRequestHandler
from sys import argv, exit

if len(argv) != 2:
    print("Hey, deme la IP solamente")
    exit(1)

ip = str(argv[1])
users = {'123456': ["pepito perez", 1234, 60000000]}

class bank_handler(BaseRequestHandler):
    def handle(self):
        global users
        print(f'Conneting with client {self.client_address}')
        while True:
            data = self.request.recv(1024).decode()
            if(data[0:3] == "DEP"):
                proto, cc, passw, money = data.split(", ")
                self.deposit(cc, int(passw), int(money))
            elif(data[0:3] == "WIT"):
                proto, cc, passw, money = data.split(", ")
                self.withdraw(cc, int(passw), int(money))
            elif(data[0:6] == "CONSUL"):
                proto, cc, passw = data.split(", ")
                self.consul(cc, int(passw))
            elif(data[0:3] == "BYE"):
                self.request.close()
                return None
            else:
                data = "Orden invalida\n".encode()
                self.request.send(data)
    def deposit(self, cc, passw, money):
        try:
            if(cc in users.keys()):
                if(passw == users[cc][1]):
                    users[cc][2] += money
                    data = "Consignacion exitosa \n".encode("utf-8")
                    self.request.send(data)
                else:
                    data = "Contrasena incorrecta \n".encode("utf-8")
                    self.request.send(data)
            else:
                data = "Usuario no encontrado \n".encode("utf-8")
                self.request.send(data)
        except:
            data = "Consignacion fallida \n".encode("utf-8")
            self.request.send(data)

    def withdraw(self, cc, passw, money):
        try:
            if(cc in users.keys()):
                if(passw == users[cc][1]):
                    if(money <= users[cc][2]):
                        users[cc][2] -= money
                        data = "Retiro exitoso \n".encode("utf-8")
                        self.request.send(data)
                    else:
                        data = "No posee fondos suficientes \n".encode("utf-8")
                        self.request.send(data)
                else:
                    data = "Contrasena incorrecta \n".encode("utf-8")
                    self.request.send(data)
            else:
                data = "Usuario no encontrado \n".encode("utf-8")
                self.request.send(data)
        except:
            data = "Consignacion fallida \n".encode("utf-8")
            self.request.send(data)


    def consul(self, cc, passw):
        if(str(cc) in users.keys()):
            if(passw == users[cc][1]):
                string = users[cc][0] + " su saldo es de: " + str(users[cc][2]) + "\n"
                data = string.encode("utf-8")
                self.request.send(data)
            else:
                data = "Contrasena invalida \n".encode("utf-8")
                self.request.send(data)
        else:
            data = "Usuario no registrado \n".encode("utf-8")
            self.request.send(data)

myserver = ThreadingTCPServer((ip, 5668), bank_handler)
myserver.serve_forever()