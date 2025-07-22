from dronekit import connect

vehicle = connect("YOUR TELEMETRY PORT HERE", baud=57600) # # e.g., "/dev/ttyUSB0" or "udp:
print("Connected:", vehicle.version)
