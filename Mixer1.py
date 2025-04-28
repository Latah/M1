#!/usr/bin/env python3
import PCF8591 as ADC
import time
import LCD1602

# Define LCD I2C address (adjust if needed)
LCD_I2C_ADDR = 0x27
LCD_NUM_ROWS = 2
LCD_NUM_COLS = 16

# Define drink options
drinks = ["Mojito", "Cosmopolitan", "Margarita", "Long Island", "Select"]
current_drink_index = 0

# Welcome screen message
welcome_message = "Cocktail Mixer"
instruction_message = "Use Joystick"

def setup():
    ADC.setup(0x48)
    LCD1602.init(LCD_I2C_ADDR, 1)  # init(slave address, background light)
    LCD1602.clear()
    global state

def direction():   #get joystick result
    state = ['home', 'up', 'down', 'left', 'right', 'pressed']
    i = 0
    if ADC.read(0) <= 30:
        i = 1         #up
    elif ADC.read(0) >= 225:
        i = 2         #down

    if ADC.read(1) >= 225:
        i = 3         #left
    elif ADC.read(1) <= 30:
        i = 4         #right

    if ADC.read(2) <= 30:
        i = 5         # Button pressed

    if ADC.read(0) - 125 < 15 and ADC.read(0) - 125 > -15   and ADC.read(1) - 125 < 15 and ADC.read(1) - 125 > -15 and ADC.read(2) == 255:
        i = 0

    return state[i]

def display_welcome():
    LCD1602.clear()
    LCD1602.write(0, 0, welcome_message.center(LCD_NUM_COLS))
    LCD1602.write(1, 0, instruction_message.center(LCD_NUM_COLS))
    time.sleep(2)

def display_drink_menu():
    LCD1602.clear()
    for i, drink in enumerate(drinks):
        line = ""
        if i == current_drink_index:
            line += "> "
        else:
            line += "  "
        line += drink[:LCD_NUM_COLS - 2]
        LCD1602.write(i % LCD_NUM_ROWS, 0, line.ljust(LCD_NUM_COLS))

def update_drink_selection():
    global current_drink_index
    direction_val = direction()

    if direction_val == 'up':
        current_drink_index = (current_drink_index - 1) % len(drinks)
        display_drink_menu()
        time.sleep(0.2) # Debounce
    elif direction_val == 'down':
        current_drink_index = (current_drink_index + 1) % len(drinks)
        display_drink_menu()
        time.sleep(0.2) # Debounce
    elif direction_val == 'left':
        # You can implement horizontal movement for more options if needed
        pass
    elif direction_val == 'right':
        # You can implement horizontal movement for more options if needed
        pass

def check_selection():
    if direction() == 'pressed':
        selected_drink = drinks[current_drink_index]
        LCD1602.clear()
        LCD1602.write(0, 0, "Selected:".ljust(LCD_NUM_COLS))
        LCD1602.write(1, 0, selected_drink.ljust(LCD_NUM_COLS))
        time.sleep(2) # Display selection
        # Here you would add the code to trigger the dispensing of the selected drink
        print(f"Selected drink: {selected_drink}")
        return True
    return False

def destroy():
    LCD1602.clear()

if __name__ == '__main__':    # Program start from here
    setup()
    try:
        display_welcome()
        display_drink_menu()
        while True:
            update_drink_selection()
            if check_selection():
                # After selection, go back to the menu
                display_drink_menu()
            time.sleep(0.1) # Small delay for responsiveness
    except KeyboardInterrupt:     # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()