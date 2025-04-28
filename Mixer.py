# Libraries
import RPi.GPIO as GPIO
import time
import smbus
from RPLCD.i2c import CharLCD

# Define GPIO pins for joystick (adjust based on your wiring)
JOY_HORIZ_PIN = 0  # Replace with your analog input pin for horizontal movement
JOY_VERT_PIN = 1  # Replace with your analog input pin for vertical movement
JOY_BUTTON_PIN = 2  # Replace with your digital input pin for the joystick button

# Define LCD I2C address (adjust if needed)
LCD_I2C_ADDR = 0x27
LCD_NUM_ROWS = 2
LCD_NUM_COLS = 16

# Define drink options
drinks = ["Mojito", "Cosmopolitan", "Margarita", "Long Island Iced Tea", "Select"]
current_drink_index = 0

# Welcome screen message
welcome_message = "Cocktail Mixer"
instruction_message = "Use Joystick"

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

# Setup joystick pins
# For analog input, you'll typically use an ADC (Analog-to-Digital Converter) chip
# connected to the Raspberry Pi's I2C or SPI interface.
# This example assumes you have a function to read analog values.
# Replace these dummy setups with your actual ADC reading implementation.
def read_joystick_horizontal():
    # Replace with your ADC reading for the horizontal axis
    # This should return a value that changes based on joystick position
    # For example, a value between 0 and 1023
    time.sleep(0.1)  # Simulate reading
    return 512

def read_joystick_vertical():
    # Replace with your ADC reading for the vertical axis
    # This should return a value that changes based on joystick position
    # For example, a value between 0 and 1023
    time.sleep(0.1)  # Simulate reading
    return 512

GPIO.setup(JOY_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button with pull-up resistor

# Initialize LCD
try:
    lcd = CharLCD(i2c_expander='PCF8574', address=LCD_I2C_ADDR,
                    cols=LCD_NUM_COLS, rows=LCD_NUM_ROWS)
except Exception as e:
    print(f"Error initializing LCD: {e}")
    exit()

def display_welcome():
    lcd.clear()
    lcd.cursor_pos = (0, (LCD_NUM_COLS - len(welcome_message)) // 2)
    lcd.write_string(welcome_message)
    lcd.cursor_pos = (1, (LCD_NUM_COLS - len(instruction_message)) // 2)
    lcd.write_string(instruction_message)
    time.sleep(2) # Display for a few seconds

def display_drink_menu():
    lcd.clear()
    for i, drink in enumerate(drinks):
        if i == current_drink_index:
            lcd.cursor_pos = (i % LCD_NUM_ROWS, 0)
            lcd.write_string(">")
            lcd.cursor_pos = (i % LCD_NUM_ROWS, 2)
            lcd.write_string(drink[:LCD_NUM_COLS - 2]) # Truncate if too long
        elif i < LCD_NUM_ROWS:
            lcd.cursor_pos = (i % LCD_NUM_ROWS, 2)
            lcd.write_string(drink[:LCD_NUM_COLS - 2])

def update_drink_selection():
    global current_drink_index
    horiz_val = read_joystick_horizontal()
    vert_val = read_joystick_vertical()

    # Adjust sensitivity based on your joystick's output range
    sensitivity = 200

    if vert_val < (512 - sensitivity):
        current_drink_index = (current_drink_index - 1) % len(drinks)
        display_drink_menu()
        time.sleep(0.2) # Debounce
    elif vert_val > (512 + sensitivity):
        current_drink_index = (current_drink_index + 1) % len(drinks)
        display_drink_menu()
        time.sleep(0.2) # Debounce

    # You can also implement horizontal movement for more options or sub-menus

def check_selection():
    if GPIO.input(JOY_BUTTON_PIN) == GPIO.LOW: # Button pressed (assuming pull-up)
        selected_drink = drinks[current_drink_index]
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("Selected:")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(selected_drink[:LCD_NUM_COLS])
        time.sleep(2) # Display selection
        # Here you would add the code to trigger the dispensing of the selected drink
        print(f"Selected drink: {selected_drink}")
        return True
    return False

if __name__ == "__main__":
    try:
        display_welcome()
        display_drink_menu()

        while True:
            update_drink_selection()
            if check_selection():
                # After selection, you might want to go back to the menu
                display_drink_menu()
            time.sleep(0.05) # Small delay for responsiveness

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        lcd.clear()
        GPIO.cleanup()