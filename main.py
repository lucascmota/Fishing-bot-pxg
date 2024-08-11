import pyautogui as auto
import time
import keyboard
import pygetwindow as gw
import threading
import tkinter as tk

attack_active = False
threads_active = False
verificar_cor_loop_active = False

def mudarJanela():
    windows = gw.getWindowsWithTitle('PokeXGames')
    if windows:
        poke_window = windows[0]
        poke_window.activate()
    else:
        exit()

def motor():
    auto.moveTo(651, 228)
    time.sleep(0.1)

def ataque():
    while threads_active:
        if attack_active:
            for key in ['1', ';', '2', ';', '3', ';', '4', ';', '5', ';', '6', ';', '7', ';', '8', '9']:
                keyboard.send(key)
                time.sleep(0.4)
            time.sleep(0.1)
        else:
            time.sleep(0.5)

def pesca():
    while threads_active:
        motor()
        time.sleep(1)
        keyboard.send('shift+z')
        time.sleep(1)
        auto.moveTo(658, 220)
        bolha_detectada = False
        imagens = ['assets/img/bolha.png', 'assets/img/bubble.png', 'assets/img/bolha1.png']
        tempo_inicial = time.time()

        while not bolha_detectada:
            for imagem in imagens:
                try:
                    bolha = auto.locateOnScreen(imagem, confidence=0.8)
                    if bolha is not None:
                        bolha_detectada = True
                        break
                except:
                    pass
                time.sleep(0.1)

            if time.time() - tempo_inicial > 20:
                break

        if bolha_detectada:
            keyboard.send('shift+z')
            time.sleep(1.54)

def heal():
    keyboard.send('shift+3')
    time.sleep(0.2)

def verificar_batalha():
    global attack_active
    while threads_active:
        try:
            batalha = auto.locateOnScreen('assets/img/batalha.png', confidence=0.7)
            cor_esperada_1 = (216, 37, 55)
            cor_atual_1 = auto.screenshot().getpixel((434, 641))
            cor_esperada_2 = (34, 34, 34)
            cor_atual_2 = auto.screenshot().getpixel((473, 638))
            cor_esperada_3 = (32, 32, 32)
            cor_atual_3 = auto.screenshot().getpixel((448, 637))
            cor_esperada_4 = (41, 15, 17)
            cor_atual_4 = auto.screenshot().getpixel((1176, 121))
            
            if (batalha is not None or
                cor_atual_1 == cor_esperada_1 or
                cor_atual_2 == cor_esperada_2 or
                cor_atual_3 == cor_esperada_3 or
                cor_atual_4 != cor_esperada_4):
                attack_active = True
            else:
                attack_active = False
        except Exception:
            attack_active = False
        time.sleep(0.5)

def verificar_cor():
    while verificar_cor_loop_active:
        try:
            x, y = 128, 61
            cor_atual = auto.screenshot().getpixel((x, y))
            cor_esperada = (59, 103, 55)
            if cor_atual != cor_esperada:
                heal()
        except Exception:
            heal()
        time.sleep(0.1)

def start_threads():
    global threads_active
    threads_active = True
  
    mudarJanela()
    
    threading.Thread(target=ataque, daemon=True).start()
    threading.Thread(target=verificar_batalha, daemon=True).start()
    
    threading.Thread(target=pesca, daemon=True).start()

def stop_threads():
    global threads_active
    threads_active = False

def toggle_verificar_cor_loop(button):
    global verificar_cor_loop_active
    if verificar_cor_loop_active:
        verificar_cor_loop_active = False
        button.config(bg="SystemButtonFace")
    else:
        verificar_cor_loop_active = True
        button.config(bg="lightgreen")
        threading.Thread(target=verificar_cor, daemon=True).start()

def toggle_start(button):
    if threads_active:
        stop_threads()
        button.config(bg="SystemButtonFace", text="Iniciar")
    else:
        start_threads()
        button.config(bg="lightgreen", text="Parar")

def main():
    root = tk.Tk()
    root.title("Controle de Automação")

    start_button = tk.Button(root, text="Iniciar", command=lambda: toggle_start(start_button))
    start_button.pack(pady=10)

    verificar_cor_button = tk.Button(root, text="Autocura", command=lambda: toggle_verificar_cor_loop(verificar_cor_button))
    verificar_cor_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
