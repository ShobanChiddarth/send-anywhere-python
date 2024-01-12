import send_anywhere

myDevice = send_anywhere.Device("596fb5c413a6e37b31f3b2be15d0c949c2996092")

code = myDevice.send_files([r"C:\Users\Admin\Downloads\Images\profile photo.png",
                            r"C:\Users\Admin\Downloads\Images\privateinvestocat.jpg"])


