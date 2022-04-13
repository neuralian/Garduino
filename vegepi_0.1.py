# GardenPi v0.1
# receives weather data from garden_piplot_1.ino running on Sparkfun 1-CH Gateway
# echoes data back to the sender
#
# To keep running after logout, start from terminal:
#  nohup python3 vegepi_0.1.py

#
# based on lora_txrx_adafruitdemo by Brent Rubell for Adafruit Industries 2018


"""
Example using RFM9x Radio with Raspberry Pi.
Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
"""
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None

while True:
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi LoRa', 35, 0, 1)

    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        display.show()
        display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text and rssi
        display.fill(0)
        prev_packet = packet
        try:
            packet_text = str(prev_packet, "utf-8")
            display.text('RX: ', 0, 0, 1)
            display.text(packet_text, 25, 0, 1)
            print(packet_text)
            time.sleep(.05)
            print(" ")
            display.fill(0)
            reply_str = bytes("Hello back to you!","utf-8")
            rfm9x.send(prev_packet)
            display.text('Sent A!', 25, 15, 1)
        except:
            print("decode error")
        time.sleep(.05)
        

    if not btnA.value:
        # Send Button A
        display.fill(0)
        button_a_data = bytes("A","utf-8")
        rfm9x.send(button_a_data)
        display.text('Sent A!', 25, 15, 1)
    elif not btnB.value:
        # Send Button B
        display.fill(0)
        button_b_data = bytes("B","utf-8")
        rfm9x.send(button_b_data)
        display.text('Sent B', 25, 15, 1)
    elif not btnC.value:
        # Send Button C
        display.fill(0)
        button_c_data = bytes("C","utf-8")
        rfm9x.send(button_c_data)
        display.text('Sent C', 25, 15, 1)


    display.show()
    time.sleep(0.1)
