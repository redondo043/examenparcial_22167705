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
		with open("ue22167705.txt", "a") as f:         #archivo donde guardar
				f.write(self.nickname + ": " + msg + "\n")

	def historial(self, nick, msg): #Historial del chat
		with open ("ue22167705.txt", 'a') as f: 
			f.write(nick+ ": "+ msg + "\n") #se escribe el valor de las variables

#Funcion matrices
	def sec_mult(A, B): # f() que calcula la mult. en secuencial, como toda la vida se ha hecho 
		C = [[0] * n_col_B for i in range(n_fil_A)] # Crear y poblar la matrix  C = A*B
			for i in range(n_fil_A): # Hago la multiplicacion de AxB = C, i para iterar sobre las filas de A
				for j in range(n_col_B): # j para iterar sobre las columnas de B
					for k in range(n_col_A): # k para iterar en C
						C[i][j] += A[i][k] * B[k][j] # Aqui se hace la multiplicación y guardo en C.
		return C

	def par_mult(A, B): # f() que prepara el reparto de trabajo para la mult. en paralelo
		n_cores = mp.cpu_count() # Obtengo los cores de mi pc
		size_col = math.ceil(n_col_B/n_cores) # Columnas  a procesar x c/cpre, ver Excel adjunto
		size_fil = math.ceil(n_fil_A/n_cores) # Filas a procesar x c/cpre, ver Excel adjunto
		MC = mp.RawArray('i', n_fil_A * n_col_B) # Array MC de memoria compartida donde se almacenaran los resultados, ver excel adjunto
		cores = [] # Array para guardar los cores y su trabajo
		for core in range(n_cores):# Asigno a cada core el trabajo que le toca, ver excel adjunto
			i_MC = min(core * size_fil, n_fil_A) # Calculo i para marcar inicio del trabajo del core en relacion a las filas
			f_MC = min((core + 1) * size_fil, n_fil_A) # Calculo f para marcar fin del trabajo del core, ver excel
			cores.append(mp.Process(target=par_core, args=(A, B, MC, i_MC, f_MC)))# Añado al Array los cores y su trabajo
		for core in cores:
			core.start()# Arranco y ejecuto el trabajo para c/ uno de los cores que tenga mi equipo, ver excel
		for core in cores:
			core.join()# Bloqueo cualquier llamada hasta que terminen su trabajo todos los cores
		C_2D = [[0] * n_col_B for i in range(n_fil_A)] # Convierto el array unidimensional MC en una matrix 2D (C_2D) 
		for i in range(n_fil_A):# i para iterar sobre las filas de A
			for j in range(n_col_B):# j para iterar sobre las columnas de B
				C_2D[i][j] = MC[i*n_col_B + j] # Guardo el C_2D los datos del array MC
		return C_2D

	def par_core(A, B, MC, i_MC, f_MC): # La tarea que hacen todos los cores
		for i in range(i_MC, f_MC): # Size representado en colores en el excel que itera sobre las filas en A
			for j in range(len(B[0])): # Size representado en colores en el excel que itera sobre las columnas en B
				for k in range(len(A[0])): # n_fil_B o lo que es l mismo el n_col_A
					MC[i*len(B[0]) + j] += A[i][k] * B[k][j]# Guarda resultado en MC[] de cada core
                
	def multiplicacionMatrices(self, n_fil_A, n_col_A, n_fil_B, n_col_B):
		A = [[random.randint(0,215) for i in range(6)] for j in range(2153522)] # Genero A[21535220][6]con num. aleatorios del 0 al 215, ver excel 
		B = [[random.randint(0,215) for i in range(200)] for j in range(6)] # Genero B[6][21535220]con num. aleatorios del 0 al 215, ver excel
		n_fil_A = 7705 # Doy el numero de filas a A
		n_col_A = 22 # Doy el numero de columnas a A
		n_fil_B = 22 # Doy el numero de filas a B
		n_col_B = 7705 # Doy el numero de columnas a B
		if n_col_A != n_fil_B: raise Exception('Dimensiones no validas') # Compruebo que se puedan multiplicar A y B
		inicioS = time.time()
		sec_mult(A, B) # Ejecuto multiplicacion secuencial
		finS = time.time()
		inicioP = time.time()
		self.par_mult(A, B) # Ejecuto multiplicacion paralela
		finP = time.time()
		with open("examenparcial_22167705.txt", 'w') as f:
			f.write('\n\nMatriz  A y B se han multiplicado con exito en SECUENCIAL ha tardado ', finS-inicioS, ' y en PARALELO ', finP-inicioP)   
			f.write('\n\ Tamaño de A es: '+n_fil_A+ ' x ' +n_col_A+ '\n')
			f.write('\n\ Tamaño de B es: '+n_fil_B+ ' x ' +n_col_B+ '\n') 

arrancar = Cliente()