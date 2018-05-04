import socket

################### ENTER IP ADDRESS OF ARDUINO #######################

UDP_IP = "192.168.2.9"
UDP_PORT = 4210 ##no need to change

#######################################################################

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.connect((UDP_IP, UDP_PORT))
print("Binding done")

############## ENTER THE HEX VALUE OF KNOWN FINGERPTINT ################

hex1="FFFFFFFFFFFFFFFFFF014D100000FF1EFF0EFE00FC00FC00F800F800F800F800F800F800F800F800FC00FC00FC00FC00000000000000000000000000000000006388C4DE4B97139E489F119E382C4DDE50B64A5E50BFA03E4910D43F611E1A7F43B24B7F60A99C1D3FA8A87B46A90F555D2CDBF54DB0C6D3542A082C50298AAB00000000000000002D46EF01FFFFFFFF02008200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFF84EF01FFFFFFFF020082030148100000FF02FF00FE00FE00FC00FC00F800F800FC00FC00FC00FC00FC00FE00FE00FE00FF00000000000000000000000000000000004A8CD3BE4F9213DE6517DA7E4C99D19E3C270DDE54B18ABE4B3F89BE74C28756472D0B5F563AE01F64249C1D432368B760A81C7746240E3450ABE30C54A406CD00000000000000002CB8EF01FFFFFFFF080082000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

########################################################################

def compare(s1,s2):
    length=len(s1)
    s=0
    for i in range(length):
        s=s+(int(s1[i],16)-int(s2[i],16))/length
    return abs(s)*100


status="first time"
start="start"
MESSAGE1="fingerprint matched"
MESSAGE2="fingerptint not matched"


while True:
    #-------------------- WILL SEND ONLY ONCE ---------------------------
    if (status == "first time"):
        sock.sendto(start.encode('utf-8'),(UDP_IP,UDP_PORT))
        status="second"
    #-------------------------------------------------------------------

    #--------------------- RECEIVE HEX FROM ARDUINO -------------------------
    data,addr=sock.recvfrom(1024)
    data=data.decode('utf-8')
    err=compare(data,hex1)
    print(err)
    #--------------------------------------------------------------------
    #--------------------------SEND REPLY TO ARDUINO--------------------------
    if (err<40):
        sock.sendto(MESSAGE1.encode('utf-8'),(UDP_IP,UDP_PORT))
    else:
        sock.sendto(MESSAGE2.encode('utf-8'),(UDP_IP,UDP_PORT))
    #----------------------------------------------------------------------
