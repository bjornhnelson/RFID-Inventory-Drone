import datetime
import csv

def getTimeStamp(line):
   dateArr = []
   timeArr = []
   date = line[2]
   time = line[3]

   dateArr = date.split('-', 2)
   year = int(dateArr[0])
   month = int(dateArr[1])
   day = int(dateArr[2])

   timeArr = time.split(':', 2)
   hour = int(timeArr[0])
   minute = int(timeArr[1])
   second = int(timeArr[2])

   print("year " + str(year) + " month "+  str(month) + " day " + str(day) + " time: " + time)
   # We may need to change the timezone but not sure - Caleb Rabbon 6/7/2020
   timestamp = datetime.datetime(int(year), month, day, hour, minute, second).timestamp()
   print(timestamp)
   return timestamp

def getID(line):
    return line[0]

def main():
   with open('ministock.csv', 'r') as csv_file:
       csv_reader = csv.reader(csv_file)

       next(csv_reader)

       for line in csv_reader:
           timestamp = getTimeStamp(line)
           print(timestamp)
           print(getID(line))
   
   
   timestamp = datetime.datetime(1970, 1, 1, 0, 0, 0).timestamp()
   print(timestamp)
   
   timestamp = datetime.datetime(1970, 1, 1, 1, 0, 0).timestamp()
   print("additional hour so + 3600")
   print(timestamp)
   
   timestamp = datetime.datetime(1970, 1, 1, 1, 1, 0).timestamp()
   print("+60")
   print(timestamp)
   
   timestamp = datetime.datetime(1970, 1, 1, 1, 1, 1).timestamp()
   print("+1")
   print(timestamp)
   #E20019C60906AAF1135D1AAA,4,2018-02-03,16:07:37,b1951afa
   

if __name__== "__main__":
   main()
