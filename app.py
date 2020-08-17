
import time
import tkinter as tk
import subprocess #para ejecutar en terminal de computador
import paramiko #para ejecutar remoto
import select
#from getpass import getpass

class Application(tk.Frame):
	def __init__(self, master=None):#crea la raiz o ventana principal de la app
		super().__init__(master)
		self.master = master
		self.master.geometry("1280x720")
		self.master.resizable(0,0)
		self.master.title("aplicacion de seguridad")
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		#crea las partes de la app

		self.etiq_user = tk.Label(self, text="Usuario:", font=("Lucida Grande",20))
		self.usuario = str
		self.ctext_user = tk.Entry(self, textvariable=self.usuario,width=30)

		self.etiq_clave = tk.Label(self, text="Contraseña:", font=("Lucida Grande",20))
		self.clave = str 
		self.ctext_clave = tk.Entry(self, textvariable=self.clave, show="*", width=30)

		self.etiq_ip = tk.Label(self, text="Direccion IP:", font=("Lucida Grande",20))
		self.ip = str   
		self.ctext_ip = tk.Entry(self, textvariable=self.ip,width=30)	

		self.connect_ssh = tk.Button(self, font=("Lucida Grande",20), fg="green",height=2,width=30)
		self.connect_ssh["text"] = "Comprobar datos de conexion."
		self.connect_ssh["command"] = self.connect

		self.quit = tk.Button(self, text="SALIR", font=("Lucida Grande",20), fg="red",height=2,width=30)
		self.quit["command"] = self.exit

		#Acomoda partes de la app en la ventana

		self.etiq_user.grid(column=0, row=1, pady=30)
		self.ctext_user.grid(column=1, row=1, columnspan=2)

		self.etiq_clave.grid(column=0, row=2, pady=30)
		self.ctext_clave.grid(column=1, row=2, columnspan=2)

		self.etiq_ip.grid(column=0, row=3, pady=30)
		self.ctext_ip.grid(column=1, row=3, columnspan=2)

		self.connect_ssh.grid(column=0, row=4, columnspan=3, pady=30)

		self.quit.grid(column=0, row=5, columnspan=3, pady=30)

	def connect(self):#Establece conexion via ssh
		try:
			self.client=paramiko.SSHClient()
			self.client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
			self.client.connect('192.168.0.114', username='darwin', password='holahola')
			#self.client.connect(self.ctext_ip.get(), username=self.ctext_user.get(), password=self.ctext_clave.get())
			self.sftp = self.client.open_sftp()
			print("\nConectado!")
			self.create_widgets_connect()

		except paramiko.ssh_exception.AuthenticationException:
			print("\nError de conexion. Verifique sus datos.")

		except paramiko.ssh_exception.NoValidConnectionsError:
			print("\nError de conexion. Verifique la IP.")

		

	def create_widgets_connect(self):
		self.connect_interface = tk.Toplevel(self)
		self.connect_interface.geometry("1280x720")
		self.connect_interface.resizable(0,0)

		self.start_app = tk.Button(self.connect_interface, font=("Lucida Grande",20),height=2,width=30)
		self.start_app["text"] = "Iniciar aplicacion."
		self.start_app["command"] = self.startapp

		self.end_app = tk.Button(self.connect_interface, font=("Lucida Grande",20),height=2,width=30)
		self.end_app["text"] = "Terminar ejecucion de aplicacion."
		self.end_app["command"] = self.endapp
		
		self.read_inf = tk.Button(self.connect_interface, font=("Lucida Grande",20),height=2,width=30)
		self.read_inf["text"] = "Leer informe."
		self.read_inf["command"] = self.read

		self.watch_video = tk.Button(self.connect_interface, font=("Lucida Grande",20),height=2,width=30)
		self.watch_video["text"] = "Ver video."
		self.watch_video["command"] = self.watchvideo

		self.quit2 = tk.Button(self.connect_interface, text="SALIR", fg="red", font=("Lucida Grande",20),height=2,width=30)
		self.quit2["command"] = self.disconnect
		
		self.start_app.grid(row=0, pady=30)
		self.end_app.grid(row=1, columnspan=2, pady=30)
		self.read_inf.grid( row=2, columnspan=2, pady=30)
		self.watch_video.grid( row=3, columnspan=2, pady=30)
		self.quit2.grid( row=4, columnspan=2, pady=30)

		#self.master.wait_window(self.connect_interface)

	def startapp(self):#para iniciar sniffer
		print("\nIniciando aplicacion!")
		self.transport = self.client.get_transport()
		self.channel = self.transport.open_session()
		sin=self.channel.exec_command('python3 /home/darwin/proyecto3/sniffer_trial.py')
		time.sleep(10)
		
	def endapp(self):#para terminar sniffer
		print("\nTerminando ejecucion!")
		pass

	def read(self):#Para leer informe generado por el sniffer
		print("\nAbriendo informe!")
		self.sftp.get('/home/darwin/proyecto3/Informe.txt', '/home/darwin/proyecto3/informeprueba.txt')
		#subprocess.call(['nano','-v','informeprueba.txt'])
		f = open ('informeprueba.txt','r')
		mensaje = f.read()
		print("\n"+mensaje)
		f.close()
		print("\nAqui termina el informe!")

	def watchvideo(self):#Para ver el video generado por el sniffer
		print("\nReproduciendo video!")
		self.sftp.get('/home/darwin/proyecto3/footage.avi', '/home/darwin/proyecto3/videoprueba.avi')
		subprocess.call(['mplayer','videoprueba.avi'])

	def disconnect(self):#desconectar de servidor remoto
		print("\nCerrando conexion!")
		self.connect_interface.destroy()
		self.client.close()

	def exit(self):#Salir de la app
		print("\nSaliendo!\n")
		self.master.destroy()

root = tk.Tk()
app = Application(master=root)
app.mainloop()