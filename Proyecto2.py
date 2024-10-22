import cv2
import os
import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Crear carpeta para guardar las fotos si no existe
if not os.path.exists("fotos"):
    os.makedirs("fotos")

class CameraApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cámara App")
        self.master.geometry("900x600")
        self.master.config(bg="#2c3e50")

        self.cap = None
        self.cam_on = False

        main_frame = tk.Frame(master, bg="#2c3e50")
        main_frame.pack(pady=20)

        video_frame = tk.Frame(main_frame, bg="#2c3e50")
        video_frame.grid(row=0, column=0)

        filtros_frame = tk.Frame(main_frame, bg="#2c3e50")
        filtros_frame.grid(row=0, column=1, padx=20)

        self.btn_prender_camara = tk.Button(master, text="Prender Cámara", command=self.prender_apagar_camara, bg="#27ae60", fg="#ffffff", font=("Helvetica", 16))
        self.btn_prender_camara.pack(pady=10, padx=20, fill=tk.X)

        self.btn_foto = tk.Button(master, text="Tomar Foto", command=self.tomar_foto, bg="#3498db", fg="#ffffff", font=("Helvetica", 16), state=tk.DISABLED)
        self.btn_foto.pack(pady=10, padx=20, fill=tk.X)

        self.btn_salir = tk.Button(master, text="Salir", command=self.salir, bg="#e74c3c", fg="#ffffff", font=("Helvetica", 16))
        self.btn_salir.pack(pady=10, padx=20, fill=tk.X)

        self.label = tk.Label(video_frame)
        self.label.pack()

        self.filtros_activos = {
            'normal': True,
            'blanco_negro': False,
            'invertido': False,
            'verde': False,
            'purpura': False,
            'dibujo': False,
        }

        self.btn_normal = tk.Button(filtros_frame, text="Normal", command=self.reset_filtros, bg="#2ecc71", fg="#ffffff", font=("Helvetica", 10), width=15)
        self.btn_normal.pack(pady=5)

        self.btn_blanco_negro = tk.Button(filtros_frame, text="Blanco y Negro", command=lambda: self.toggle_filtro('blanco_negro'), bg="#34495e", fg="#ffffff", font=("Helvetica", 10), width=15)
        self.btn_blanco_negro.pack(pady=5)

        self.btn_invertido = tk.Button(filtros_frame, text="Invertido", command=lambda: self.toggle_filtro('invertido'), bg="#8e44ad", fg="#ffffff", font=("Helvetica", 10), width=15)
        self.btn_invertido.pack(pady=5)

        self.btn_verde = tk.Button(filtros_frame, text="Verde", command=lambda: self.toggle_filtro('verde'), bg="#d35400", fg="#ffffff", font=("Helvetica", 10), width=15)
        self.btn_verde.pack(pady=5)

        self.btn_dibujo = tk.Button(filtros_frame, text="Dibujo", command=lambda: self.toggle_filtro('dibujo'), bg="#16a085", fg="#ffffff", font=("Helvetica", 10), width=15)
        self.btn_dibujo.pack(pady=5)

        self.btn_purpura = tk.Button(filtros_frame, text="Purpura", command=lambda: self.toggle_filtro('purpura'), bg="#f39c12", fg="#ffffff", font=("Helvetica", 10), width=15)
        self.btn_purpura.pack(pady=5)

    def prender_apagar_camara(self):
        if not self.cam_on:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "No se pudo abrir la cámara.")
                return
            self.cam_on = True
            self.btn_prender_camara.config(text="Apagar Cámara", bg="#e67e22")
            self.btn_foto.config(state=tk.NORMAL)
            self.mostrar_video()
        else:
            self.cam_on = False
            self.btn_prender_camara.config(text="Prender Cámara", bg="#27ae60")
            self.btn_foto.config(state=tk.DISABLED)
            self.label.config(image="")
            if self.cap:
                self.cap.release()
                self.cap = None

    def mostrar_video(self):
        if self.cam_on and self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = self.aplicar_filtros(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                self.photo = ImageTk.PhotoImage(image=img)
                self.label.configure(image=self.photo)
                self.label.image = self.photo

            self.master.after(10, self.mostrar_video)

    def aplicar_filtros(self, frame):
        # Aplicar solo el filtro activo
        for filtro, activo in self.filtros_activos.items():
            if activo:
                if filtro == 'normal':
                    return frame  # Retornar el frame sin cambios

                elif filtro == 'blanco_negro':
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

                elif filtro == 'invertido':
                    frame = cv2.bitwise_not(frame)

                elif filtro == 'verde':
                    frame[:, :, 2] = 0  # Eliminar el canal rojo y azul

                elif filtro == 'purpura':
                    frame[:, :, 1] = 0  # Eliminar el canal verde

                elif filtro == 'dibujo':
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    inv_gray = cv2.bitwise_not(gray)
                    frame = cv2.divide(gray, inv_gray, scale=256.0)
                    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

                return frame  # Retornar el frame con el filtro aplicado

    def toggle_filtro(self, filtro):
        # Reiniciar todos los filtros y activar el seleccionado
        for key in self.filtros_activos:
            self.filtros_activos[key] = False
        self.filtros_activos[filtro] = True

    def reset_filtros(self):
        # Reiniciar todos los filtros
        for key in self.filtros_activos:
            self.filtros_activos[key] = False
        self.filtros_activos['normal'] = True

    def tomar_foto(self):
        if self.cam_on and self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = self.aplicar_filtros(frame)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"fotos/foto_{timestamp}.png"
                cv2.imwrite(filename, frame)
                messagebox.showinfo("Foto guardada", f"Foto guardada como {filename}")

    def salir(self):
        if self.cap:
            self.cap.release()
        self.master.quit()

root = tk.Tk()
app = CameraApp(root)
root.mainloop()
