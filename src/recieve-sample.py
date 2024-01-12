import send_anywhere

myDevice = send_anywhere.Device("596fb5c413a6e37b31f3b2be15d0c949c2996092")

myData = myDevice.receive_files("191196")

with open('file.bat', 'wb') as fh:
    fh.write(myData)
