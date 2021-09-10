from SwarmUtils import SwarmServer

swarm = SwarmServer()
#swarm.send_command(cmd=swarm.CMD_SET_LED_STATE, data=[255, 100, 10])
swarm.receive_command()
