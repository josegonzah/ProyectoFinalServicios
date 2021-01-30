import socket as sk

def udpconect(account, passw, money, ip):
    ##string = str(account) + ", "
    #string = string + str(passw) + ", "
    #string = string + str(money)
    #print(string)
    string = "123456, 1234, 72000"
    print(string)
    c = sk.socket(sk.AF_INET,sk.SOCK_DGRAM)
    c.sendto(string.encode(),(ip, 7777)) ##Puerto del servicio banco UDP
    data, remote = c.recvfrom(1024)
    print(data.decode())
    data, remote = c.recvfrom(1024)
    print(data.decode())
    c.close()
    return data.decode()