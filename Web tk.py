import tkinter as tk
from tkinter import font

# Funktion zur Motorsteuerung (Platzhalter - wird nicht mit GPIO verbunden)
# Diese Funktion gibt nur aus, was passieren würde, wenn sie verbunden wäre.
def motor_control(direction):
    if direction == 'left':
        print("Motor dreht nach links")
    else: # direction == 'right'
        print("Motor dreht nach rechts")

# Fenster einrichten
root = tk.Tk()
root.title("Ein-Motor-Steuerung") # Angepasster Titel
root.geometry("600x400") # Kleinere Fenstergröße, da weniger Elemente
root.configure(bg="#f0f0f0")

# Große Schriftarten definieren
title_font = font.Font(family="Helvetica", size=36, weight="bold")
button_font = font.Font(family="Helvetica", size=32, weight="bold") # Etwas größere Buttons

# Titel
title_label = tk.Label(root, text="Motorsteuerung", font=title_font, bg="#f0f0f0")
title_label.pack(pady=30) # Mehr vertikaler Abstand

# Rahmen für die Buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=50) # Vertikal zentrieren

# Button Links (←)
btn_left = tk.Button(button_frame, text="← Links", font=button_font, fg="blue", width=8, height=2,
                     command=lambda: motor_control("left")) # motor_id entfernt
btn_left.pack(side=tk.LEFT, padx=30) # Mehr horizontaler Abstand zwischen Buttons

# Button Rechts (→)
btn_right = tk.Button(button_frame, text="Rechts →", font=button_font, fg="red", width=8, height=2,
                      command=lambda: motor_control("right")) # motor_id entfernt
btn_right.pack(side=tk.RIGHT, padx=30) # Mehr horizontaler Abstand zwischen Buttons

# Fenster starten
root.mainloop()