from socketserver import ThreadingTCPServer, BaseRequestHandler
from udp_liquor import udpconect
from sys import argv, exit


if len(argv) != 2:
    print("Hey, deme la ip pues")
    exit(1)

ip = str(argv[1])
users = 0
inventory = {'vodka': [1, 'ru', 100, 72000], 'ron': [2, 'co', 70, 46400], 'aguadiente': [3, 'co', 80, 36800], 'Whisky': [4, 'uk', 200, 125000], 'tequila': [5, 'mx', 37, 95000]}

class handler_liquor(BaseRequestHandler):
    def handle(self):
        global users
        global inventory

        print(f'Conneting with client {self.client_address}')

        users += 1
        while True:
            data = self.request.recv(1024).decode('utf-8')
            ##Se utiliza el split para saber que se hará en la cadena de caracteres
            print(data)
            if data[0:6] == "INVENT":
                self.print_invent()
            elif data[0:3] == "BUY":
                proto, liquor, quant = data.split(", ")
                self.buy(liquor, quant[0:-1])
            elif data[0:3] == "BYE":
                self.request.close()
                return None
            else:
                
                data = 'Solo tenemos estas dos acciones \n'.encode("utf-8")
                self.request.send(data)
                
        self.request.close()
        users -= 1

    def print_invent(self):
        data = ("Usuarios en linea: " + str(users) + "\n").encode("utf-8")
        self.request.send(data)
        for i in inventory.keys():
            data = (i) + ". Cantidad: " + str(inventory[i][2]) + ". Precio por unidad: " + str(inventory[i][3])+ "\n"
            data = data.encode("utf-8")
            self.request.send(data)


    
    def buy(self, liquor, quant):
        if(liquor in inventory.keys() and int(quant) <= inventory[liquor][2]):
            data = "Ingrese su numero de cedula y su contraseña para pagar, separados por , \n".encode("utf-8")
            self.request.send(data)
            data = self.request.recv(1024).decode("utf-8")
            data = data[0:-1]
            cc, passw = data.split(", ")
            ##Conexion UDP
            money = int(inventory[liquor][3])*(int(quant))
            flag = udpconect(str(cc), str(passw), str(money), ip)
            if flag:
                inventory[liquor][2] -= int(quant)
                data = "Compra exitosa \n".encode("utf-8")
                self.request.send(data)
            else:
                data = "Compra denegada \n".encode("utf-8")
                self.request.send(data)
        else:
            data = "Error en inventario, no hay esta cantidad de licor en stock \n"
            self.request.send(data)
    

myserver = ThreadingTCPServer((ip, 5555), handler_liquor)
myserver.serve_forever()
