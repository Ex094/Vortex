import os, subprocess, time

class Vortex:
    
    result = ""
    count = 0
    driveList = []
    device = ""
    iso_path = ""
    
    def burn(self):
        print("\t>> Burning ISO to USB, This might take some time...")
        #Prepare DD Command
        self.command = "dd bs=4M if='{}' of={}".format(self.iso_path, self.device)
        
        #Starting Burning
        if(subprocess.call(self.command, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) == 0):
            print("\t>> ISO Burned Successfully!")
        else:
            print("\t>> Unable to burn ISO to the USB")
    
    def displayInfo(self):
        print("""
        Selected Disk: {}
        ISO Path: {}
        """.format(self.device, self.iso_path))
    
    def prepareISO(self, path):
        if((not os.path.isfile(path))):
            print("\t>> ISO File was not found, Terminating...")
            quit()
        elif(".iso" not in path):
            print("\t>> Invalid file, File with .ISO Extension required!")
            quit()
        else:
            self.iso_path = path
            
    
    def prepareDisk(self, userChoice):
        if(int(userChoice) > self.count):
            print("\t>> No such device in the list!")
            quit()
        else:
            #Prepare device path
            self.device = "/dev/{}".format(self.driveList[int(userChoice) - 1])
            self.command = "umount {}".format(self.device)
            
            #Unmount the device
            if(subprocess.call(self.command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) == 0):
                print("\t>> Device Unmounted!")
            else:
                print("\t>> Device already unmounted!")
            
    
    def getDisks(self):
        
        self.command = 'lsblk --output KNAME,MAJ:MIN,RM,SIZE,LABEL | grep "sd[a-z]\W*[0-9]*:[0-9]*\W*[1]"'
        
        try:
            self.result = subprocess.check_output(self.command, shell=True)
        except subprocess.CalledProcessError as err:
            print("\t>> No Drives Found!\n")
            quit()
            
        self.output = self.result.decode("UTF-8").split("\n")
        
        print("Disks Found:\n")
        
        for self.dev in self.output:
            self.drive = list(filter(None, str(self.dev).split(" ")))
            if("1" in self.drive):
                self.drive.pop(1) ##Remvoing
                self.drive.pop(1) ##Useless Values
                self.count+=1
                self.driveList.append(self.drive[0])
                print(str(self.count) + ") " + " ".join(self.drive))
        
        
    
    def clearScreen(self):
        os.system("clear")

def main():
    vortex = Vortex()
    
    vortex.clearScreen()
    
    print("""
        #########################################
        # Vortex, A tool for burning ISO to USB #
        #########################################
        
        | Please make sure you have inserted the USB
        | on which you wish to burn the ISO.
        
        | By Ex094
        | http://www.procurity.wordpress.com
        """)
    
    vortex.getDisks()
    
    choice = input("\n\n>> Please select your Device: ")
    vortex.prepareDisk(choice)
    
    time.sleep(1)
    
    path = raw_input("\n>> Path to ISO File: ")
    vortex.prepareISO(path)
    
    vortex.clearScreen()
    
    vortex.displayInfo()
    
    raw_input("\t>> Press Any Key to Continue..")
    
    vortex.clearScreen()
    
    vortex.burn()
    
if __name__ == "__main__":
    main()