from ublox_gps import MicropyGPS

import machine, utime

uart = machine.UART(0, baudrate=9600, tx=0, rx=1)
gps = MicropyGPS()

def main():
  with open("logs.txt", "a") as file:
    file.write("date, time, latitude, longitude, speed, altitude, satelites in use\n")
    while True:
      try:
        if uart.any():
          try:
            data = uart.read().decode() # Remove the errors='ignore'
          except UnicodeError:
            print("Decoding error encountered")
            continue # Skip the iteration if decoding fails

        # Update gps object to reflect location (parse)
        for x in data:
          gps.update(x)

        # Print number of active satelites
        print(str(gps.satelites_in_use))

        # Modify timestamp str to format it better
        timestamp_str = ""
        for x in gps.timestamp:
          timestamp_str += str(x)
          timestamp_str += ":"

        # Strip extra colon on right side
        timestamp_str = timestamp_str.strip(":")

        # Write to file
        # TODO: Finish this line
        file.write(gps.date_string())

      except KeyboardInterrupt:
        print("Done!")
        break

if __name__ == "__main__":
  main()
