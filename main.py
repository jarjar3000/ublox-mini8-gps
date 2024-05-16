from ublox_gps import MicropyGPS

import machine, utime, time

uart = machine.UART(0, baudrate=9600, tx=0, rx=1)
gps = MicropyGPS()

# Infinite loop until buton push
with open("logs.txt", "a") as file:
    file.write("date, time, latitude, longitude, speed, altitude, satelites in use\n")
    while True:
        try:
            if uart.any():
                try:
                    data = uart.read().decode()  # Remove the errors='ignore'
                except UnicodeError:
                    print("Decoding error encountered")
                    continue  # Skip the iteration if decoding fails
            
                # Update gps object to reflect location
                for x in data:
                    gps.update(x)
                
                # Print number of active satelites
                print(str(gps.satellites_in_use))
                
                # Timestamp in better format
                timestamp_str = ""
                for x in gps.timestamp:
                    timestamp_str += str(x)
                    timestamp_str += ":"
                    
                timestamp_str = timestamp_str.strip(":")
                      
                # Write to file
                file.write(gps.date_string() + "," + timestamp_str + "," + gps.latitude_string() + "," +  gps.longitude_string() + "," + gps.speed_string() + ","  + str(gps.altitude) + "," + str(gps.satellites_in_use) + "\n")
                
                #Flush
                file.flush()
                
        except Exception as error:
            #Flush
            file.flush()
            print("Done with error", error)
            file.write("Adios")
            file.close()
            break
