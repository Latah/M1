#!/usr/bin/env python3
import PCF8591 as ADC
import time
import LCD1602

# LCD Configuration
LCD_I2C_ADDR = 0x27
LCD_ROWS = 2
LCD_COLS = 16

# Drink Options
DRINKS = ["Mojito", "Cosmopolitan", "Margarita", "Long Island"]
current_drink_index = 0

# Messages
WELCOME_MSG = "Cocktail Mixer"
INSTRUCTION_MSG = "Select your drink"

def setup():
    ADC.setup(0x48)
    LCD1602.init(LCD_I2C_ADDR, 1)
    LCD1602.clear()
    global state

def get_joystick_direction():
    state = ['home', 'up', 'down', 'left', 'right', 'pressed']
    x_val = ADC.read(0)
    y_val = ADC.read(1)
    btn_val = ADC.read(2)

    if y_val <= 30: return state[4]  # right
    elif y_val >= 225: return state[3] # left
    elif btn_val <= 30: return state[5] # pressed
    elif 110 < x_val < 140 and 110 < y_val < 140 and btn_val == 255: return state[0] # home
    return None

def display_message(row, text):
    LCD1602.write(row, 0, text.center(LCD_COLS))

def display_welcome():
    display_message(0, WELCOME_MSG)
    display_message(1, INSTRUCTION_MSG.center(LCD_COLS))
    time.sleep(2)

def display_drink_menu():
    LCD1602.clear()
    line = ""
    for i, drink in enumerate(DRINKS):
        if i == current_drink_index:
            line += f"[{drink[:LCD_COLS // len(DRINKS) - 1]}]"
        else:
            line += f" {drink[:LCD_COLS // len(DRINKS) - 1]} "

    # Split the drinks across the two rows if there are more than 2
    if len(DRINKS) > 2:
        row1_drinks = line[:LCD_COLS]
        row2_drinks = line[LCD_COLS:]
        LCD1602.write(0, 0, row1_drinks)
        LCD1602.write(1, 0, row2_drinks)
    else:
        LCD1602.write(0, 0, line.center(LCD_COLS))
        LCD1602.write(1, 0, "".center(LCD_COLS)) # Clear second row

def update_drink_selection():
    global current_drink_index
    direction_val = get_joystick_direction()

    if direction_val == 'right':
        current_drink_index = (current_drink_index + 1) % len(DRINKS)
        display_drink_menu()
        time.sleep(0.2)
    elif direction_val == 'left':
        current_drink_index = (current_drink_index - 1) % len(DRINKS)
        display_drink_menu()
        time.sleep(0.2)

def check_selection():
    if get_joystick_direction() == 'pressed':
        selected_drink = DRINKS[current_drink_index]
        LCD1602.clear()
        display_message(0, "Dispensing:")
        display_message(1, selected_drink)
        time.sleep(2)
        print(f"Dispensing drink: {selected_drink}")
        return True
    return False

def destroy():
    LCD1602.clear()

if __name__ == '__main__':
    setup()
    try:
        display_welcome()
        display_drink_menu()
        while True:
            update_drink_selection()
            if check_selection():
                display_drink_menu()
            time.sleep(0.1)
    except KeyboardInterrupt:
        destroy()