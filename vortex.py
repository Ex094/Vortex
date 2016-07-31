import os, subprocess, time, re

count = 0
driveList = []

def clear():
    os.system('clear')

clear()

print("""
    #########################################
    # Vortex, A tool for burning ISO to USB #
    #########################################

    Please make sure you have inserted the USB
    on which you wish to burn the ISO.

""")

#input("Press Any Key To Continue...")

command = 'lsblk --output KNAME,MAJ:MIN,RM,SIZE,LABEL | grep "sd[a-z]\W*[0-9]*:[0-9]*\W*[1]"'
result = subprocess.check_output(command, shell=True)
output = result.decode("UTF-8").split("\n")

print("Disks Found:")
for dev in output:
    drive = list(filter(None, str(dev).split(" ")))
    if("1" in drive):
        drive.pop(1) ##Remvoing
        drive.pop(1) ##Useless Values
        count+=1
        driveList.append(drive[0])
        print(str(count) + ") " + " ".join(drive))

#Get user choice for the device
choice = input("\nPlease select your USB Device: ")
if(int(choice) > count):
    print("No such device found!")

#Prepare device path e.g /dev/sd[alphabet]
device = "/dev/{}".format(driveList[int(choice) - 1])

#Unmount the device for writing
command = "umount {}".format(device)
subprocess.Popen(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#Get the disk location e.g /dev/sd[alphabet] No Numbers
if(device[len(device) - 1] == 1):
    disk = device[:len(device) -1]
else:
    disk = device

#Get path to the ISO file to be burned
iso_path = input("Path to your .ISO file: ")
if((not os.path.isfile(iso_path)) and (".iso" not in iso_path)):
    print("Invalid Path or .ISO file!")
    quit()

clear()

#Display info to the user
print("""Selected Disk: {}
ISO Path: {}
""".format(disk, iso_path))
input("Press enter to Proceed...")

choice = input("Given the information, Do you want to continue? (y/n)")
if(choice.lower() == 'n'):
    quit()

clear()

print("Burning ISO to USB, This might take some time...")
#Burn ISO to USB
command = "dd bs=4M if='{}' of={}".format(iso_path, disk)
output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
print("Burning Complete!")
