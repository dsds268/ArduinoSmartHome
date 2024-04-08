#Imports#

#Allow Serial Connection
import serial
import time

#Import MySQL Connection
import pymysql

#Date time to get current time for banner
from datetime import datetime

#Setup Serial Connection
arduino = serial.Serial('/dev/ttyS3', 9600) #S3 == COM4

#Get Current Time
time = datetime.now() 

#SQL Statments
average_temp_sql = "SELECT ROUND(AVG(temperature), 2) FROM (SELECT temperature FROM Home_TempLog ORDER BY tempId DESC LIMIT 20) AS RecentTwentyTemperatures" #Gets the average temperature from the last 20 temperature inputs 
fan_temp_sql = "SELECT Fan_enable_override FROM Smart_Home_Settings;" #Gets override setting

#Database Settings
host = "localhost"
name = "dsds"
password = ""
database = "SmartHome_db"

#Print Startup Banner
print("Welcome " + name + " The Time is Currently: " + time.strftime("%H:%M"))

#Database Connection
dbConn = pymysql.connect(host, name, password, database) or die("Could not connect to database")

print(dbConn) #Print Connection Output if failed

home = "activated" #Const Value

print("Smart Home Activated") #Tell User Smart Home Is Running

while home == "activated":
    
    #Remove "B" and "/n" by stripping and decoding the values
    led_brightness = arduino.readline().decode('utf-8').rstrip()
    humidity = arduino.readline().decode('utf-8').rstrip()
    temperature = arduino.readline().decode('utf-8').rstrip()
    
    #Output the values
    print("Humidity: ")
    print(humidity)
    print("Temperature: ")
    print(temperature)
    print("LED Brightness: ")
    print(led_brightness)


    with dbConn:
        
        #If the DHT11 Module Stops Reading, It will Return NAN
        if humidity or temperature != "nan":
            
            cursor = dbConn.cursor() #Upload New Data to mysql

            cursor.execute("INSERT INTO Home_TempLog (temperature, humidity, LED) VALUES (%s, %s, %s)", (temperature, humidity, led_brightness))
            
            dbConn.commit() #Commit and Close Use Case

        
        cursor.execute(average_temp_sql) #Execute Average Last 20 Values 
        
        average_temp = cursor.fetchone()[0] #Using Temperature Update Fan Speed
        
        cursor.execute(fan_temp_sql)
        
        fan_temp = cursor.fetchone()[0] #Get Saved Conditional Setting

        cursor.close()

    #Print Values to Panel
    print("Average Temperature: ")
    print(average_temp)
    
    print("To Activate Fan Temp Must be Higher Than: ")
    print(fan_temp)

    #If the current AVG temp is greater than the conditional temp then activate
    #fan to cool down
    if (average_temp > fan_temp):
            print("Fan Activated")
            arduino.write(b'7')
             
    else:
            print("Fan Deactivated")
            arduino.write(b'8')
            
        
