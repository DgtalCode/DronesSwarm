from SwarmUtils import SwarmClient
import time

copter = SwarmClient()
#data = copter.receive_data()
while True:
    copter.send_command(cmd=copter.CMD_SET_LED_STATE, data=[255, 100, 10], ip='localhost', port=9090)
    print("Sent")
    time.sleep(1.5)