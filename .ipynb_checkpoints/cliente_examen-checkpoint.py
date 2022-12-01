import threading  #para los hilos
import sys        #para hablar con el sistema operativo (lin 21)
import socket     #para habalr con otra consola
import pickle     #para convertir en binario
import os         

class Cliente():

	def __init__(self, host=input("Intoduzca la IP del servidor ?  "), port=int(input("Intoduzca el PUERTO del servidor ?  ")), nickname=" "):
		self.s = socket.socket()                #creo el objeto socket
		while(nickname==""):
				nickname=input("Nombre de usuario: ")
				self.nickname= nickname
		with open("nicknameList.txt", "a") as f:  #archivo donde guardar
			f.write((self.nickname + "\n"))
		self.s.connect((host, int(port)))       #creo la conexion
            
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		threading.Thread(target=self.recibir, daemon=True).start()  #se instancia el hilo

		while True:
			msg = input('\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 1 \n')
			if msg != '1' : self.enviar(msg)
			else:
				print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid())
				self.s.close()
				sys.exit()
                    
	def deleteNickname (self, nickname):
		espacio = []
		with open ("nicknameList.txt", 'r') as f:   #se abre el txt en modo lectura
				nicknames = f.readlines()
				for n in nicknames:
						if (nickname not in n):
								espacio.append(n)
		with open("nicknameList.txt", 'w' ) as f:   #se abre el txt en modo escritura
				for n in espacio:
						f.write(n)

	def recibir(self):
		print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			try:
				data = self.s.recv(128)               #guarda la info del otro lado del chat en binario
				if data: print(pickle.loads(data))    #mete el dato y lo desserializa(vuelve a normal)
			except: pass

	def enviar(self, msg):
		self.s.send(pickle.dumps(self.nickname+ ": " + msg))
		with open("22167705.txt", "a") as f:         #archivo donde guardar
				f.write(self.nickname + ": " + msg + "\n")

arrancar = Cliente()