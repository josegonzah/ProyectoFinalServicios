import socket
from datetime import datetime

class UDPServer:
    ''' A simple UDP Server '''

    def __init__(self, host, port):
        self.host = host    # Host address
        self.port = port    # Host port
        self.sock = None    # Socket
        ##Información dict es : [Codigo, DNS, u disponibles, precio x unidad]
        self.invent = {'vodka': [1, 'ru', 100, 72000]} ##Se utiliza como clave el nombre en minuscula del licor por facilidad
                                                        

    def printwt(self, msg):
        ''' Print message with current date and time '''

        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{current_date_time}] {msg}')

    def configure_server(self):
        ''' Configure the server '''

        # create UDP socket with IPv4 addressing
        self.printwt('Creating socket...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.printwt('Socket created')

        # bind server to the address
        self.printwt(f'Binding server to {self.host}:{self.port}...')
        self.sock.bind((self.host, self.port))
        self.printwt(f'Server binded to {self.host}:{self.port}')

    def get_phone_no(self, name):
        ''' Get phone no for a given name '''

        phonebook = {'Alex': '1234567890', 'Bob': '1234512345', 'Dylan': '1234'}
        for i in phonebook.keys():
            if i == name[0:-1]:
                return f"{name[0:-1]}'s phone number is {phonebook[name[0:-1]]}"
        return f"No records found for {name[0:-1]}"
    def get_inventory(self):
        return f"Inventory: {self.inventory}"
    def handle_request(self, data, client_address):
        ''' Handle the client '''

        # handle request
        name = data.decode('utf-8')
        resp = self.get_phone_no(name)
        self.printwt(f'[ REQUEST from {client_address} ]')
        print('\n', name, '\n')

        # send response to the client
        self.printwt(f'[ RESPONSE to {client_address} ]')
        self.sock.sendto(resp.encode('utf-8'), client_address)
        print('\n', resp, '\n')
    def buy_drink(self, drink, quant, creds):
        # Se esta haciendo la conexion con el servidor banco
        drink = drink.lower()
        msgFromClient="WIT, "+str(creds[0])+", "+str(creds[1])[0:-1]+", "+str(self.invent[drink][3])+"\n"
        print(msgFromClient)
        bytesToSend = str.encode(msgFromClient)
        bufferSize          = 1024
        serverAddressPort   = ("127.0.0.2", 5555)
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = "Message from Bank {}".format(msgFromServer[0])
        print(msg)
        if drink in self.invent.keys() and int(quant)<= self.invent[drink][2]:
            self.invent[drink][2] = self.invent[drink][2] - int(quant)
            return f"Succesful purchase you got {quant}: {drink}s \n"
        else:
            return f"Unsuccesful purchase \n"


    def wait_for_client(self):
        ''' Wait for a client '''

        try:
            # receive message from a client
            data, client_address = self.sock.recvfrom(1024)

            # handle client's request
            self.handle_request(data, client_address)

        except OSError as err:
            self.printwt(err)

    def shutdown_server(self):
        ''' Shutdown the UDP server '''

        self.printwt('Shutting down server...')
        self.sock.close()

def main():
    ''' Create a UDP Server and respond to a client's resquest '''

    udp_server = UDPServer('127.0.0.1', 4444)
    udp_server.configure_server()
    udp_server.wait_for_client()
    udp_server.shutdown_server()

if __name__ == '__main__':
    main()
