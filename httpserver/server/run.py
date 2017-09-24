# -*- coding: utf-8 -*-
import socket
import re
import os


def get_response(request):
	httpreq = '\n200 OK'
	lines = request.decode().split('\r')
	inlin = lines[0].split(' ')
	if (inlin[0] != 'GET'):
		return 'Page not found' + '\n404 Not Found'

		
	
	if (inlin[1] == '/'):
		for x in lines:
        		if(re.search(r'^\nUser-Agent:*', x)):
				s = re.sub(r'User-Agent: ', '', x)
				s = 'Hello mister! \nYou are:' + s
				return s + httpreq


	if (inlin[1] == '/test/'):
		s = ''
		for x in lines:
			s += x
		return s + httpreq

	if (re.search(r'.txt$', inlin[1]) and re.search(r'/media/', inlin[1])):
		fname = re.sub('/media/', '', inlin[1]) 
		fname = 'files/' + fname
		try:
			f = open(fname)
		except IOError:
			return 'File not found' + '\n404 Not Found'	
		return f.read() + httpreq

	if (re.search(r'^/media/$', inlin[1])):
		files = os.listdir ("files")
		shfiles = ''
		for fi in files:
			shfiles = shfiles + fi + '\n'
		return shfiles + httpreq

     
	return 'Page not found' + '\n404 Not Found'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  #Связь сокета с хостом по данному порту
server_socket.listen(0)  #Включаем прослушивание сокета

print 'Started'

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  #Выводится сообщение о подключении клиента и его Ip
        request_string = client_socket.recv(2048)  #Получаем url запрос
        client_socket.send(get_response(request_string))  #Отправляем пользователю данные
        client_socket.close()
    except KeyboardInterrupt:  #Прерывание работы
        print 'Stopped'
        server_socket.close()  #Закрываем соккет
        exit()
