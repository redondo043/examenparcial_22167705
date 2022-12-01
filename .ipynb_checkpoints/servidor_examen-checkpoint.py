import socket          #hablar con otra consola
import threading       #hilos
import sys             #habalr con el sistema
import pickle          #serializar y deserializar
import os              #hablar con el sistema operativo

class Servidor():

	def __init__(self, host=socket.gethostname(), port=int(input("Que puerto quiere usar ? "))): #host e IP
		self.clientes = []        #array de los clientes
		print('\nSu IP actual es : ',socket.gethostbyname(host))
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(), '\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		self.s = socket.socket() #crea
		self.s.bind((str(host), int(port))) #enlaza el host y el puerto
		self.s.listen(30) #numero de veces que puedo estar esperando a que entre la conexion
		self.s.setblocking(False) #para que no se bloquee

		threading.Thread(target=self.aceptarC, daemon=True).start()
		threading.Thread(target=self.procesarC, daemon=True).start()

		while True:
			msg = input('\n << SALIR = 1 >> \n') #si le doy a 1 cierra el servidor
			if msg == '1':
				print(" **** Me piro vampiro; cierro socket y mato SERVER con PID = ", os.getpid())
				self.s.close()
				sys.exit()
			else: pass

	def aceptarC(self):
		print('\nHilo ACEPTAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())

		while True:
			try:
				conn, addr = self.s.accept() #pilla las especificaciones
				print(f"\nConexion aceptada via {addr}\n")
				conn.setblocking(False)  #para que no se bloquee
				self.clientes.append(conn) #lo meto en el array de clientes
				self.readNickname()
			except: pass
	def readNickname(self):
				with open("nicknameList.txt", "r") as f:  #archivo donde pasar las cosas
						print("Clientes conectados actualmente: \n [" + f.read() + "]")

	def procesarC(self):
		print('\nHilo PROCESAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			if len(self.clientes) > 0: #si hay clientes...
				for c in self.clientes: #para los clientes en el array
					try:
						data = c.recv(128) #recibo 128 bytes de cada cliente y los guardo
						if data: self.broadcast(data,c) #si es verdadero(hay datos) llamo al boradcast
					except: pass

	def broadcast(self, msg, cliente):
		i=0
		for c in self.clientes:
			try:
				if c != cliente:
						if i==0:
								print("\n Clientes conectados Right now = ", len(self.clientes))
								self.readNickname
								print(pickle.loads(msg)) #carga el mensaje en binario
						i=1
				c.send(msg) #lo envia
			except: self.clientes.remove(c) 
    
	def historial(self, n): #Historial del chat
		with open ("ue22167705.txt", 'a') as f: 
			f.write(n"Historial: "+ str(n) + "\n") #se escribe el valor de las variables
arrancar = Servidor() 