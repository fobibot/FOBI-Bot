print("Streaming in class")
                frame = cam1.read()
                # Part the progress for send the data to Application
                encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),30]
                result, imgencode = cv2.imencode('.jpg', frame, encode_param)
                data_img = numpy.array(imgencode)
                stringData = data_img.tostring()
                img_length = len(stringData)
                print(img_length)
                size = struct.pack('<l',img_length)         # Pack size of image(int) to bytes
                size += bytes(SEND_RECEIVE_COUNT-len(size)) # Fill the bytes with zero until have 4 bytes
                if is_streaming:
                    conn_streaming.send( size )
                    conn_streaming.send( stringData )



host = ''
port_control = 6321
port_streaming = 8010
def setupServer(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((host, port))
    except socket.error as msg_er:
        print(msg_er)
    print("Socket port %s bind comlete."% str(port))
    return s

# Create 2 Servers Socket tcp
s_control = setupServer(port_control)
s_streaming = setupServer(port_streaming)
def main():
    global on_LED_B, is_shutdown, conn_control, conn_streaming, hold_camera, cam1
    BlinkBlue()     # Blink LED Blue then off
    while True:
        try:
            print("Waiting to Connect")
            conn_control = setupConnection_control()
            conn_streaming = setupConnection_streaming()
            # Smile when connected
            try:
                i2c_write_Head('@HEM000!')
                i2c_write_Head('@HSN080!')
            except OSError as msg_er:
                print(msg_er)
                pass
            dataTransfer(conn_control)
            if is_shutdown:
                break
        except KeyboardInterrupt:
            break
        # have some problem with the connection
        # go to wait to new connection again
        except BrokenPipeError as msg_er:
            print(msg_er)
            is_connect = False
            continue
        except ConnectionResetError as msg_er:
            print(msg_er)
            is_connect = False
            continue
ใน main คือเรียกใช้ให้มันรอต่อกับ client
# Function to communication with Application with Socket port 6321
def dataTransfer(conn):
    global volume, on_LED_B, is_streaming, hold_camera, is_connect, conn_streaming, is_capture
    global ready_send_module, is_Head, is_shutdown, cam1
    # Loop that sends/receives data
    while is_connect:
        try:
            # Receive the data
            data_recv = conn.recv(13)
            data_recv = data_recv.decode('utf-8')
            # Split the data
            msg = data_recv.split(' ')      # Split the receive data by space
            num_cmd = len(msg)
            command = msg[0]
            if num_cmd == 4 and msg[3] == '!':
                if command == '#HS':        # Drive 2 Servo on Head Module
                    print("Head servo 1 : "+msg[1]+" / servo 2 : "+msg[2])
                    i2c_write_Head('@HST'+msg[1]+'!')
                    i2c_write_Head('@HSN'+msg[2]+'!')
                else:
                    print('Unknown Command[4] : ' + data_recv)
            elif num_cmd == 3 and msg[2] == '!':
                if command == '#SS':        # Play Sound
                    print("Sample Sound"+msg[1])
                    playSound(msg[1])
                elif command == '#SV':      # Set Volume
                    print("Set Volume : "+msg[1])
                    volume = float(msg[1])
                elif command == '#EM':      # Change the Emotion
                    print("Change emotion to : emotion"+msg[1])
                    i2c_write_Head('@HEM'+msg[1]+'!')
                elif command == '#FW':      # Drive the Robot forward with value of speed
                    print("Forward : "+msg[1])
                    i2c_write_Wheel('@WFW'+msg[1]+'!')
                elif command == '#AT':      # Drive Arms to the same direction
                    print("(Together)Arm : "+msg[1])
                    i2c_write_Arm_together(msg[1])
                elif command == '#AO':      # Drive Arms to the opposite direction
                    print("(Opposite)Arm : "+msg[1])
                    i2c_write_Arm_opposite(msg[1])
                else:
                    print('Unknown Command[3] : ' + data_recv)
            elif num_cmd == 2 and msg[1] == '!':
                if command == '#MC':        # Check the module
                    reply = module_check()
                    conn.send(reply.encode())
                elif command == '#XT':      # Client disconnect
                    i2c_write_Wheel('@WMS000!')
                    print("Our client has left us")
                    BlinkBlue()
                    break
                elif command == '#DC':      # Dancing
                    print('Dancing')
                    Dance_Func()            # Call Dancing Function
                    print('Stop Dancing')
                elif command =='#SW':       # Soft Shutdown the Robot
                    print("Shutdown")
                    is_shutdown = True
                elif command =='#ST':       # Start streaming webcam camera to app
                    print("Start Streaming")
                    if is_Head and hold_camera:
                        is_streaming = True
                elif command == '#CS':      # Cancel/Stop streaming
                    print("Cancel Streaming")
                    is_streaming = False
                elif command == '#CP':      # Capture
                    if is_Head and hold_camera:
                        is_capture = True
                        print("in CP")
                elif command == '#MS':      # Stop motors in Wheel module
                    print("Motor Stop")
                    i2c_write_Wheel('@WMS000!')
                elif command == '#BW':      # Drive the Robot backward (fix speed)
                    print("Backward")
                    i2c_write_Wheel('@WBW000!')
                elif command == '#FL':      # Forward and turn left (fix speed)
                    print("Forward Left")
                    i2c_write_Wheel('@WFL000!')
                elif command == '#FR':      # Forward and turn right (fix speed)
                    print("Forward Right")
                    i2c_write_Wheel('@WFR000!')
                elif command == '#SL':      # Spin the Robot to the left (fix speed)
                    print("Spin Left")
                    i2c_write_Wheel('@WSL000!')
                elif command == '#SR':      # Spin the Robot to the right (fix speed)
                    print("Spin Right")
                    i2c_write_Wheel('@WSR000!')
                else:
                    print('Unknown Command :[2] ' + data_recv)
            else:
                print('Unknown Command[1] : ' + data_recv)
        except OSError as msg_er:
            # ignore error
            print(msg_er)
            Show = 1
            findAddress()
            Show = 0
            #conn_control.close()
            #conn_streaming.close()
            continue
    conn.close()                    #Close the connection
    conn_streaming.close()
    is_connect = False




    JoyStick = [int(data_recv[i:i+3])-100 for i in range(0, len(data_recv), 3)]
    #MoveDegree = int(np.degrees(np.arctan2(JoyStick[1],JoyStick[0])))
    MoveSpeed  = int(np.sqrt(np.power(JoyStick[0],2)+np.power(JoyStick[1],2)))
    i2c_data_string = str(JoyStick[0])+':'+str(JoyStick[1])+':'+str(MoveSpeed)
    #bus.write_block_data(address,0x01,list(str.encode(i2c_data_string)))
    bus.write_block_data(address,0x02,list(str.encode(str(MoveSpeed))))
    #print(str(MoveDegree)+'-'+str(MoveSpeed))
    #MoveSpeed  = int(np.sqrt(np.power(JoyStick[0],2)+np.power(JoyStick[1],2)))
