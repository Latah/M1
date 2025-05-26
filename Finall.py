import tkinter as tk
from tkinter import font
import RPi.GPIO as GPIO # Importiere RPi.GPIO für die tatsächliche Motorsteuerung
import time # Importiere time für sleep

# --- GPIO Setup ---
# Nur ausführen, wenn auf einem Raspberry Pi.
# Wenn du das auf einem normalen PC testest, kommentiere diesen Block aus.
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    STEP = 17  # Step pin
    DIR = 27   # Direction pin
    EN = 23    # Enable pin

    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(EN, GPIO.OUT)

    # Motor parameters (aus deinem vorherigen Code)
    STEPS_PER_REV = 200 # Schritte pro Umdrehung deines Motors (z.B. 200 für 1.8 Grad/Schritt)
    MOVEMENT_DEGREE = 90 # Grad der Bewegung pro Klick
    usDelay = 950 # Mikrosekunden-Verzögerung zwischen Pulsen (Geschwindigkeit)
    uS = 0.000001 # Eine Mikrosekunde

    # Motor initial deaktivieren
    GPIO.output(EN, GPIO.HIGH)
    
    # Flag, um zu prüfen, ob GPIO initialisiert wurde
    gpio_initialized = True
except RuntimeError:
    print("RPi.GPIO nicht verfügbar. Führe den Code auf einem Raspberry Pi aus, um die Motorsteuerung zu aktivieren.")
    gpio_initialized = False

# Funktion zur Motorsteuerung
def move_motor_degrees(degrees, direction_clockwise):
    if not gpio_initialized:
        print(f"Simulation: Motor bewegt sich {degrees} Grad {'im Uhrzeigersinn' if direction_clockwise else 'gegen den Uhrzeigersinn'}")
        return # Beende die Funktion, wenn GPIO nicht initialisiert ist

    # Motor-Treiber aktivieren
    GPIO.output(EN, GPIO.LOW)
    time.sleep(0.01) # Kleine Verzögerung, damit sich der Treiber stabilisiert

    num_steps = int((degrees / 360.0) * STEPS_PER_REV)
    GPIO.output(DIR, GPIO.HIGH if direction_clockwise else GPIO.LOW) # DIR HIGH = CW, DIR LOW = CCW

    for _ in range(num_steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(uS * usDelay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(uS * usDelay)

    # Motor-Treiber nach der Bewegung deaktivieren
    GPIO.output(EN, GPIO.HIGH)
    print(f"Motor bewegt sich {degrees} Grad {'im Uhrzeigersinn' if direction_clockwise else 'gegen den Uhrzeigersinn'}.")

# --- Tkinter GUI Setup ---

# Fenster einrichten
root = tk.Tk()
root.title("Motorsteuerung")
root.geometry("800x400") # Anpassung der Fenstergröße
root.configure(bg="#f0f0f0")

# Große Schriftarten definieren
title_font = font.Font(family="Helvetica", size=36, weight="bold")
button_font = font.Font(family="Helvetica", size=32, weight="bold")

# Titel
title_label = tk.Label(root, text="🛠️ Motorsteuerung", font=title_font, bg="#f0f0f0")
title_label.pack(pady=30)

# Rahmen für die einzelnen Motor-Buttons
# Da wir nur einen Motor haben, vereinfachen wir dies
motor_frame = tk.Frame(root, bg="#f0f0f0")
motor_frame.pack(pady=15)

# Button für Linksbewegung (entspricht z.B. gegen den Uhrzeigersinn)
btn_left = tk.Button(motor_frame, text="◀ Links", font=button_font, fg="red", width=8, height=2,
                     command=lambda: move_motor_degrees(MOVEMENT_DEGREE, False)) # False für CCW
btn_left.pack(side=tk.LEFT, padx=30) # Mehr padding für Abstand

# Button für Rechtsbewegung (entspricht z.B. im Uhrzeigersinn)
btn_right = tk.Button(motor_frame, text="Rechts ▶", font=button_font, fg="green", width=8, height=2,
                      command=lambda: move_motor_degrees(MOVEMENT_DEGREE, True)) # True für CW
btn_right.pack(side=tk.LEFT, padx=30) # Mehr padding für Abstand


# Cleanup GPIO when the Tkinter window is closed
def on_closing():
    if gpio_initialized:
        GPIO.output(EN, GPIO.HIGH) # Ensure motor is disabled
        GPIO.cleanup()
        print("GPIO cleaned up.")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing) # Call on_closing when window is closed

# Fenster starten
root.mainloop()