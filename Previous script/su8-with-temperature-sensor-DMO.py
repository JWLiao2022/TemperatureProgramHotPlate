from time import time, sleep
import RPi.GPIO as GPIO
import os
import glob



######User input parameters######
###Step resolution is 1/8 *4 (0.9^0), giving ~ 0.7572^0 per step 

#Temperature0 = 0 #degreeC, initial temperature

Temperature1 = 65 #degreeC
TempHoldTime1 = 60 #seconds
TempRampRate1 = 10 #seconds/step

Temperature2 = 95 #degreeC
TempHoldTime2 = 300 #seconds
TempRampRate2 = 10 #seconds/step

TempReduceRate = 10 #seconds/step



TempResolution = 0.7572 #degree C/step at half resolution
#TempResolution = 1.0 #degree C/step at half resolution x10 at Cav

######End of user input parameters######

######function to make sure the sleep function giving enough sleep time
def trusty_sleep(n):
    start = time()
    while(time() - start < n):
        sleep(n - (time()-start))

######main######

#####set up the thermal sensor######

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string)/1000.0

    return temp_c

def cali_temp():
    ####calibration factors, obtained by experiment
    a = 1.4839289
    b = -13.0432541
    ###end of calibration factors section
    readTemp = read_temp()
    caliTemp = a * readTemp + b
    return round(caliTemp)

#####end of set-up temperature functions#####


DIR = 20 ###GPIO pin 20
STEP = 21 ###GPIO pin 21
ENA = 23 ###GPIO pin 23
RaiseT = 1 #clockwise
ReduceT = 0 #counterclockwise

##### set the security steps
#SPR1 = (Temperature1 - Temperature0)/TempResolution
#SPR1 = int(round(SPR1)) #steps for raising the temperature to the Temperature1  

#SPR2 = (Temperature2 - Temperature1)/TempResolution
#SPR2 = int(round(SPR2)) #steps for raising the temperature from Temperature1 to Temperature2

#SPR3 = SPR1 + SPR2 #steps for reducing the temperature

securityStep = (150 - 25)/TempResolution
securityStep = int(round(securityStep))

###


GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

MODE = (14, 15, 18)
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
GPIO.output(MODE, RESOLUTION['1/8'])


###set the output temperature as a function of time

#Heating
#From room temperature to the Temperature1
print("Ramping the temperature to {:d} degree C".format(Temperature1))


GPIO.output(DIR, RaiseT)
#step_count = SPR1
delay = TempRampRate1

currentTemp = cali_temp()
currentStepcount = 1
startTime = time()

outputFileName = 'outputTempTime.txt'
f1 = open(outputFileName, 'w+')
f1.write('Time(seconds)    Temperature (0C)\n')
f1.close

while (currentTemp < Temperature1) and (currentStepcount < securityStep):
    print("current temperature is {} degree C at time of {} seconds...".format(currentTemp, time() - startTime))
    f1 = open(outputFileName, 'a')
    f1.write("{}   {} \n".format(time() - startTime, currentTemp))
    f1.close()
    
    GPIO.output(ENA, GPIO.LOW)
    sleep(0.5)

    for x in range(4):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.02)
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.02)

    GPIO.output(ENA, GPIO.HIGH)
    sleep(delay)

    currentTemp = cali_temp()
    currentStepcount += 1

#Hold the temperature
print("Holding at the first target temperature of {} degreeC. Real temperature is  {} degree C.".format(Temperature1, currentTemp))
trusty_sleep(TempHoldTime1)

#From the Temperature1 to the Temperature2
print("Ramping the temperature to {:d} degreeC.".format(Temperature2))
#step_count = SPR2
delay = TempRampRate2

currentTemp = cali_temp()

while (currentTemp < Temperature2) and (currentStepcount < securityStep):
    print("current temperature is {} degree C at time of {} seconds...".format(currentTemp, time()-startTime))
    f1 = open(outputFileName, 'a')
    f1.write("{}   {}\n".format(time() - startTime, currentTemp))
    f1.close()
            
    GPIO.output(ENA, GPIO.LOW)
    sleep(0.5)

    for x in range(4):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.02)
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.02)

    GPIO.output(ENA, GPIO.HIGH)
    sleep(delay)

    currentTemp = cali_temp()
    currentStepcount += 1


#Hold the temperature
#GPIO.output(ENA, GPIO.HIGH)

print("Holding at the second target temperature of {:d} degreeC.".format(Temperature2))

trusty_sleep(TempHoldTime2)
                    

#Cool down
print("Cooling down...")
step_count=currentStepcount
GPIO.output(DIR, ReduceT)
delay = TempReduceRate

currentTemp = cali_temp()

for x in range(step_count):
    print("current temperature is {} degree C at time of {} seconds...".format(currentTemp, time()-startTime))
    f1 = open(outputFileName, 'a')
    f1.write("{}   {}\n".format(time() - startTime, currentTemp))
    f1.close()
            
    GPIO.output(ENA, GPIO.LOW)
    sleep(0.5)
    
    for y in range(4):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.02)
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.02)

    GPIO.output(ENA, GPIO.HIGH)
    sleep(delay)
    currentTemp = cali_temp()


GPIO.cleanup()
