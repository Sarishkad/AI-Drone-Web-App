from dronekit import connect

vehicle = connect("COM5", baud=57600)
print("Connected:", vehicle.version)
