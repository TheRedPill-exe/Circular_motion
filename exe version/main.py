import sys
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from calculate import calculate_moves
from files import save_video_info
class VideoGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Video Circular")
        self.root.geometry("400x800")
        self.root.configure(bg="#f7f7f7")

        # Etiqueta de título
        title_label = tk.Label(root, text="Generador de Video Circular", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333")
        title_label.pack(pady=10)

        # Nombre del video
        self.label_video_name = tk.Label(root, text="Nombre del video:", font=("Helvetica", 12), bg="#f7f7f7")
        self.label_video_name.pack(pady=5)
        self.video_name_entry = tk.Entry(root, font=("Helvetica", 12), width=30)
        self.video_name_entry.pack(pady=5)

        # Duración del video
        self.label_duration = tk.Label(root, text="Duración del video (segundos):", font=("Helvetica", 12), bg="#f7f7f7")
        self.label_duration.pack(pady=5)
        self.duration_spinbox = tk.Spinbox(root, from_=1, to=300, font=("Helvetica", 12), width=5)
        self.duration_spinbox.pack(pady=5)

        # Radio del primer círculo
        self.label_radius1 = tk.Label(root, text="Radio del primer círculo (píxeles):\n(En este sistema, 100px = 1 cm)", font=("Helvetica", 12), bg="#f7f7f7")
        self.label_radius1.pack(pady=5)
        self.radius1_spinbox = tk.Spinbox(root, from_=1, to=500, font=("Helvetica", 12), width=5)
        self.radius1_spinbox.pack(pady=5)

        # Número de vueltas del círculo
        self.label_turns = tk.Label(root, text="Número de vueltas:", font=("Helvetica", 12), bg="#f7f7f7")
        self.label_turns.pack(pady=5)
        self.turns_spinbox = tk.Spinbox(root, from_=1, to=100, font=("Helvetica", 12), width=5)
        self.turns_spinbox.pack(pady=5)

        # Número de vueltas del círculo
        self.acele = tk.Label(root, text="¿Cual será la aceleración tangencial (m/s^2)?", font=("Helvetica", 12), bg="#f7f7f7")
        self.acele.pack(pady=5)
        self.acele_spinbox = tk.Spinbox(root, from_=1, to=100, font=("Helvetica", 12), width=5)
        self.acele_spinbox.pack(pady=5)

        # Botón para seleccionar la ruta de guardado
        self.select_path_button = tk.Button(root, text="Seleccionar ruta de guardado", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=self.select_save_path)
        self.select_path_button.pack(pady=10)

        # Mostrar ruta seleccionada
        self.save_path_label = tk.Label(root, text="", font=("Helvetica", 10), bg="#f7f7f7", fg="#333")
        self.save_path_label.pack(pady=5)

        # Botón para generar el video
        self.generate_button = tk.Button(root, text="Generar video", font=("Helvetica", 14), bg="#FF5722", fg="white", command=self.generate_video)
        self.generate_button.pack(pady=20)
        
        self.load_data_button = tk.Button(root, text="Cargar datos desde archivo", font=("Helvetica", 12), bg="#2196F3", fg="white", command=self.load_video_data)
        self.load_data_button.pack(pady=10)
        # Botón para seleccionar el video
        self.select_video = tk.Button(root, text="Seleccionar video a calcular", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=self.select_video_path)
        self.select_video.pack(pady=10)
        
        self.calculate_button = tk.Button(root, text="Calcular", font=("Helvetica", 14), bg="#FF5722", fg="white", command=self.calculate_params)
        self.calculate_button.pack(pady=20)

        # Mostrar ruta seleccionada
        self.save_video_label = tk.Label(root, text="", font=("Helvetica", 10), bg="#f7f7f7", fg="#333")
        self.save_video_label.pack(pady=5)


        self.save_path = ""
        self.video_path = ""

    def calculate_params(self):
        # Validar si se ha seleccionado un video
        if not self.video_path:
            messagebox.showerror("Error", "Debe sezleccionar un video antes de calcular.")
            return
        
        # Llamar a la función calculate_moves con la ruta del video seleccionado
        print(f"Calculando movimientos en el video: {self.video_path}")  # Solo para depuración
        calculate_moves(self.video_path)

    def select_video_path(self):
        # Abrir un cuadro de diálogo para seleccionar un archivo de video
        self.video_path = filedialog.askopenfilename(
            filetypes=[("Archivos de video", "*.mp4;*.avi;*.mov;*.mkv")],
            title="Seleccione un archivo de video"
        )
        
        # Actualizar la etiqueta con la ruta seleccionada
        if self.video_path:
            self.save_video_label.config(text=f"Video seleccionado: {self.video_path}")
        else:
            self.save_video_label.config(text="No se seleccionó ningún video")
    
    def load_video_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")], title="Seleccione un archivo de texto")
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = f.readlines()
                # Aquí puedes procesar los datos según el formato del archivo
                print("Datos cargados desde el archivo:")
                for line in data:
                    print(line.strip())
                messagebox.showinfo("Éxito", "Datos cargados correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")

    def select_save_path(self):
        # Selección de la ruta de guardado
        self.save_path = filedialog.askdirectory()
        if self.save_path:
            self.save_path_label.config(text=f"Ruta seleccionada: {self.save_path}")

    def generate_video(self):
        # Validar entradas
        video_name = self.video_name_entry.get()
        if not video_name or not self.save_path:
            messagebox.showerror("Error", "Debe ingresar un nombre de video y seleccionar una ruta.")
            return

        duration = int(self.duration_spinbox.get())
        radius1 = int(self.radius1_spinbox.get())
        turns = int(self.turns_spinbox.get())
        aceleration = int(self.acele_spinbox.get())        
        
        # Generar el video con los parámetros proporcionados
        self.create_video(video_name, duration, radius1, turns, [2,100
                                                                 
                                                                 ], aceleration)
        messagebox.showinfo("Éxito", f"Video generado correctamente en {self.save_path}")

    def create_video(self, video_name, duration, radius1, turns, forces, aceleration):
        fps = 60
        width, height = 640, 480
        center = (width // 2, height // 2)
        total_frames = int(duration * fps)
        time_force_applied = forces[0] * fps - 1  # Momento en el que se aplica la fuerza, en fotogramas
        force_value = forces[1]  # Magnitud de la fuerza aplicada
        video_path = f"{self.save_path}/{video_name}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        angular_velocities = []
        xpositions = []
        ypositions = []
        angles = []
        
        # Aceleración angular calculada como α = a_t / r (en m)
        angular_acceleration = aceleration / radius1

        # Velocidad angular inicial (calculada sin afectar la física)
        angular_velocity = 2 * np.pi * turns / (fps * duration)

        for t in range(total_frames):
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Calcular la nueva velocidad angular en cada frame
            angular_velocity += angular_acceleration / fps
            angle = (angular_velocity * t) % 360  # El ángulo se calcula usando la velocidad angular

            # Posición del círculo
            x1 = int(center[0] + radius1 * np.cos(np.radians(angle)))  # Usar el radio en píxeles
            y1 = int(center[1] + radius1 * np.sin(np.radians(angle)))  # Usar el radio en píxeles
            cv2.circle(frame, (x1, y1), 20, (0, 255, 0), -1)  # Dibujar el círculo en el frame

            # Almacenar posiciones y ángulos para análisis
            xpositions.append(x1 - center[0])
            ypositions.append(y1 - center[1])
            angles.append(angle)
            angular_velocities.append(angular_velocity)
            
            out.write(frame)  # Escribir el frame en el video

        # Guardar información sobre el video generado
        save_video_info(video_name, duration, radius1, turns, angles, xpositions, ypositions, angular_velocities, aceleration, self.save_path)
        out.release()




if __name__ == "__main__":
    root = tk.Tk()
    app = VideoGeneratorApp(root)
    root.mainloop()
