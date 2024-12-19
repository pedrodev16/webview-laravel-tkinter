import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import webview

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Laravel App Wrapper")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=10, font=("Arial", 10))
        self.text_area.pack(padx=10, pady=10)

        self.start_button = tk.Button(root, text="Start Laravel Server", command=self.start_server)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Laravel Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.process = None
        self.webview = None

    def start_server(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Iniciar el servidor Laravel
        self.process = subprocess.Popen(
            ["php", "artisan", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        # Leer la salida del servidor en un hilo separado
        threading.Thread(target=self.read_output, daemon=True).start()

        # Abrir la ventana de la web de Laravel
        self.root.after(5000, self.open_webview)  # Esperar 5 segundos antes de abrir la webview

    def read_output(self):
        for line in self.process.stdout:
            self.text_area.insert(tk.END, line)
            self.text_area.yview(tk.END)

    def open_webview(self):
        # Crear la ventana de la web de Laravel
        self.webview = webview.create_window("Laravel App", "http://127.0.0.1:8000")
        webview.start()

    def stop_server(self):
        if self.process:
            self.process.terminate()
            self.process = None
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            if self.webview:
                webview.destroy_window(self.webview)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()