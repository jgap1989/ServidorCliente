import socket
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread

class ClientApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cliente - Chat con el Servidor")

        # Área de chat donde se muestran los mensajes
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.chat_area.pack(padx=20, pady=5)
        self.chat_area.config(state=tk.DISABLED)

        # Campo para escribir el mensaje
        self.msg_entry = tk.Entry(master)
        self.msg_entry.pack(padx=20, pady=5, fill=tk.X)
        self.msg_entry.bind("<Return>", self.send_message)

        # Botón para enviar el mensaje
        self.send_button = tk.Button(master, text="Enviar", command=self.send_message)
        self.send_button.pack(padx=20, pady=5)

        # Conectar al servidor
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = '192.168.137.1'
        self.server_port = 9999
        try:
            self.client.connect((self.server_ip, self.server_port))
            self.add_to_chat(f"Conectado al servidor {self.server_ip}:{self.server_port}")
            self.listen_thread = Thread(target=self.receive_messages, daemon=True)
            self.listen_thread.start()
        except ConnectionRefusedError:
            self.add_to_chat(f"No se pudo conectar al servidor en {self.server_ip}:{self.server_port}")

    def receive_messages(self):
        """Escucha mensajes del servidor y los muestra en la ventana."""
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if not message:
                    break
                self.add_to_chat(f"Servidor: {message}")
            except:
                self.add_to_chat("Error al recibir mensaje del servidor.")
                break

    def send_message(self, event=None):
        """Envía un mensaje al servidor."""
        message = self.msg_entry.get()
        if message:
            self.client.send(message.encode('utf-8'))
            self.add_to_chat(f"Tú: {message}")
            self.msg_entry.delete(0, tk.END)

    def add_to_chat(self, message):
        """Agrega un mensaje al área de chat."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def close_connection(self):
        """Cierra la conexión con el servidor."""
        self.client.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_connection)
    root.mainloop()