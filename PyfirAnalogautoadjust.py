import os 
import time 
import math
import pyfirmata
from gpiozero import LED
os.system("sudo chmod 777 /dev/ttyS0")
board = pyfirmata.ArduinoMega("/dev/ttyS0")
mcureset = LED(18) # Getting the microcontroller reset automaticly 
mcureset.off()
SENSOR_PIN =3

it = pyfirmata.util.Iterator(board)
it.start()
board.analog[SENSOR_PIN].enable_reporting()
#print("Rebooting robotics arm")
#os.system("python3 Pyfiranaloginput.py")
#Self calibration before running motor
Faultdetect = []
#Initial data structure management 
Initialdegree = []
Initialdata = []
Initialmemdata = [0] #Mem the trigger data and if detected mem initial data then stop motor 
#Terminal data structure management 
Terminaldegree = []
Terminaldata = [] 
Terminalmemdata = [4946] #Mem the trigger data and if detected mem terminal data turn off the motor and check statement of Initial data 
def sumsignal(list): 
      sum = 0 
      for i in list:
           sum += i
      return sum 

while True:
    light_level = board.analog[SENSOR_PIN].read()
    print("Reading from analog sensor: %s" % light_level)
    
    if light_level  == None: 
        #Activate trigger reset
        Faultdetect.append(light_level)
    if len(Faultdetect) > 2: 
           Faultdetect.clear()
    if len(Faultdetect) -1 == 1: 
        #os.system("echo $?")
        print("Activate microcontroller resetting")
        mcureset.on()
        time.sleep(0.04)
        mcureset.off()
        time.sleep(2)
        os.system("python3 Pyfiranaloginput.py")
    if light_level != None:
          print("Initiate calibration progress....")
          print("Previous fault status detect:",Faultdetect) 
          Anglebase = ((light_level*10000-235)/(49-int(Initialmemdata[0])*1000))*180
          
          print(int(Anglebase))
          if int(Anglebase) > 90:
              print("Mem more than 90 degree")
              Terminaldegree.append(int(Anglebase))
              Terminaldata.append(light_level)
              print(Terminaldata)
              if len(Terminaldegree) != [] or len(Terminaldegree) >=3:
                 Triggerstatement = int(Terminaldegree[len(Terminaldegree)-1]) - int(Terminaldegree[len(Terminaldegree)-2])
                 if Triggerstatement == 0:
                      print("The last value statement",Terminaldegree[len(Terminaldegree)-1])
                      print("Calibrating...") #Checking the 0 degree calibration 
                      print(Terminaldata[len(Terminaldata)-1])
                      Terminalmemdata.clear()
                      Terminalmemdata.append(Terminaldata[len(Terminaldata)-1])
          if int(Anglebase) < 90:
              print("Mem less than 90 degree")   
              Initialdegree.append(int(Anglebase))
              Initialdata.append(light_level)
              print(Initialdegree) 
              if len(Initialdegree) != [] or len(Initialdegree) >=3:
                 Triggerstatement = int(Initialdegree[len(Initialdegree)-1]) - int(Initialdegree[len(Initialdegree)-2])
                 if Triggerstatement == 0:
                      print("The last value statement",Initialdegree[len(Initialdegree)-1])
                      print("Calibrating...") #Checking the 0 degree calibration 
                      print(Initialdata[len(Initialdata)-1]) #Getting the Initial data list to compute in the summation 
                      Initialmemdata.clear()
                      Initialmemdata.append(Initialdata[len(Initialdata)-1]) #Getting the initial mem data from the initial grigger data to processing the algorithm adjustment
    board.pass_time(0.2)
