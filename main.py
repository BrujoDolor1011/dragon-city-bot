import os
import sys
import customtkinter as ctk
from threading import Thread
import pyautogui
import time
from datetime import datetime

# Configuración de la ventana principal
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Manejo de rutas para PyInstaller
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICONO_JUEGO = os.path.join(ASSETS_DIR, "dragoncity-icon.png")

BOTS = {
    "Collect Gold & Food Bot": "collect_gold_food",
    "Food Farm Bot": "food_farm",
    "Terra Breed Bot": "terra_breed",
    "Terra Hatch Bot": "terra_hatch"
}


class BotRunnerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dragon City Bot Menu")
        self.geometry("600x650")
        self.running = False

        self.label = ctk.CTkLabel(self, text="Selecciona un bot para ejecutar:", font=("Arial", 16))
        self.label.pack(pady=10)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        for bot_name in BOTS:
            button = ctk.CTkButton(self.button_frame, text=bot_name, command=lambda b=bot_name: self.run_bot(b))
            button.pack(pady=5, padx=10, fill='x')

        self.console_output = ctk.CTkTextbox(self, height=200, wrap='word')
        self.console_output.pack(pady=10, padx=10, fill='both', expand=True)

        self.stop_button = ctk.CTkButton(self, text="Detener Bot", fg_color="red", command=self.stop_bot,
                                         state="disabled")
        self.stop_button.pack(pady=5)

        self.exit_button = ctk.CTkButton(self, text="Salir", command=self.quit)
        self.exit_button.pack(pady=5)

    def run_bot(self, bot_name):
        if self.running:
            self.console_output.insert('end', "⚠️ Un bot ya está en ejecución. Deténlo antes de iniciar otro.\n")
            self.console_output.see('end')
            return

        self.console_output.delete("1.0", "end")
        self.console_output.insert('end', f"🚀 Ejecutando {bot_name}...\n")
        self.console_output.see('end')
        self.stop_button.configure(state="normal")
        self.running = True
        Thread(target=self.execute_bot, args=(bot_name,), daemon=True).start()

    def execute_bot(self, bot_name):
        if bot_name == "Collect Gold & Food Bot":
            run_collect_gold_food()
        elif bot_name == "Food Farm Bot":
            run_food_farm()
        elif bot_name == "Terra Breed Bot":
            run_terra_breed()
        elif bot_name == "Terra Hatch Bot":
            run_terra_hatch()

        self.running = False
        self.stop_button.configure(state="disabled")
        self.console_output.insert('end', "✅ Bot finalizado.\n")
        self.console_output.see('end')

    def stop_bot(self):
        self.running = False
        self.console_output.insert('end', "🛑 Bot detenido por el usuario.\n")
        self.console_output.see('end')
        self.stop_button.configure(state="disabled")


# Funciones generales de bots
def log(mensaje):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {mensaje}")


def is_dragon_city_open(intentos=5, confianza=0.4):
    for i in range(intentos):
        posicion = pyautogui.locateCenterOnScreen(ICONO_JUEGO, confidence=confianza)
        if posicion:
            log(f"🎮 Dragon City detectado en {posicion}")
            return True
        log(f"🔎 Intento {i + 1}/{intentos}: Icono del juego no encontrado...")
        time.sleep(1)
    return False


def locate_and_click(image, descripcion, intentos=3, click=True, duracion_mov=0.3, confianza=0.8):
    for _ in range(intentos):
        try:
            posicion = pyautogui.locateCenterOnScreen(image, confidence=confianza)
            if posicion:
                log(f"✅ {descripcion} encontrado en {posicion}")
                if click:
                    pyautogui.moveTo(posicion, duration=duracion_mov)
                    pyautogui.click()
                return True
        except:
            continue
        time.sleep(0.3)
    log(f"❌ No se encontró {descripcion}")
    return False


def run_collect_gold_food():
    IMAGES = [os.path.join(ASSETS_DIR, img) for img in ["food.png", "gold.png", "gold-food.png"]]
    while app.running and is_dragon_city_open():
        log("🔄 Iniciando recolección de recursos...")
        for img in IMAGES:
            locate_and_click(img, f"{os.path.basename(img).split('.')[0].capitalize()}")
        time.sleep(5)


def run_food_farm():
    COMIDA = os.path.join(ASSETS_DIR, "food.png")
    GRANJA_COMIDA = os.path.join(ASSETS_DIR, "huge-food-farm.png")
    REPLANTAR = os.path.join(ASSETS_DIR, "regrow-all.png")
    CERRAR = os.path.join(ASSETS_DIR, "close-button.png")
    while app.running and is_dragon_city_open():
        for i in range(10):
            locate_and_click(COMIDA, f"Comida ({i + 1}/10)")
        if locate_and_click(GRANJA_COMIDA, "Huge Food Farm"):
            time.sleep(1)
            locate_and_click(REPLANTAR, "Regrow All")
            time.sleep(1)
            locate_and_click(CERRAR, "Close Button")
            time.sleep(30)
        time.sleep(10)


def run_terra_breed():
    IMAGENES = [
        (os.path.join(ASSETS_DIR, 'ultra-breeding-tree.png'), 0.4),
        (os.path.join(ASSETS_DIR, 'rebreed.png'), 1),
        (os.path.join(ASSETS_DIR, 'breed.png'), 16),
        (os.path.join(ASSETS_DIR, 'take-egg.png'), 16),
        (os.path.join(ASSETS_DIR, 'terra-hatch.png'), 0.4),
        (os.path.join(ASSETS_DIR, 'sell.png'), 0.4),
        (os.path.join(ASSETS_DIR, 'sell-green.png'), 0.4)
    ]
    while app.running and is_dragon_city_open():
        for imagen, delay in IMAGENES:
            locate_and_click(imagen, f"{os.path.basename(imagen)}")
            time.sleep(delay)

def run_terra_hatch():
    IMAGENES = [
        (os.path.join(ASSETS_DIR, 'divine-orbs-habitat-2.png'), 1),
        (os.path.join(ASSETS_DIR, 'get-egg.png'), 0.4),
        (os.path.join(ASSETS_DIR, 'gold_bar.png'), 0.4),
        (os.path.join(ASSETS_DIR, 'terra-buy.png'), 16),
        (os.path.join(ASSETS_DIR, 'terra-hatch.png'), 0.4),
        (os.path.join(ASSETS_DIR, 'place.png'), 1),
        (os.path.join(ASSETS_DIR, 'divine-orbs-habitat-2.png'), 1),
        (os.path.join(ASSETS_DIR, 'terra-dragon.png'), 0.4),
        (os.path.join(ASSETS_DIR, 'sell_celestial.png'), 0.4),
        (os.path.join(ASSETS_DIR, 'sell-green.png'), 0.4)
    ]
    while app.running and is_dragon_city_open():
        for imagen, delay in IMAGENES:
            locate_and_click(imagen, f"{os.path.basename(imagen)}")
            time.sleep(delay)

if __name__ == "__main__":
    app = BotRunnerApp()
    app.mainloop()