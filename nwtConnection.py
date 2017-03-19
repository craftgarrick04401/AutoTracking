from networktables import NetworkTables as nwt
import logging, os, time

class nwtConnection(object):

    def __init__(self, roborioAddress, sdTableName, cpTableName):
        
        self.address = str(roborioAddress)
        logging.basicConfig(level=logging.DEBUG)
        nwt.initialize(server=roborioAddress)
        self.sd = nwt.getTable(sdTableName)
        self.cp = nwt.getTable(cpTableName)

    def find_stream(self):

        print("Connecting to " + self.address + " ...")

        while nwt.getRemoteAddress() == None:
            time.sleep(1)

        print("Obtaining the stream URL ...")

        for i in range(len(self.cp.getKeys())):
            if self.cp.getKeys()[i] == 'streams':
                self.streamURL = self.cp.getStringArray(self.cp.getKeys()[i])[0].split("mjpg:")[1]
                print("Stream found at " + self.streamURL)
                break
        else:
            print("Could not find stream")
            os._exit(0)

if __name__ == '__main__':

    rio = nwtConnection('roborio-4546-frc.local', '/SmartDashboard/', '/CameraPublisher/USB Camera 0/')

    rio.find_stream()
