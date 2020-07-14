import json
import sys
import datetime
import csv
import sqlite3
import numpy as np
import plotly.graph_objects as go
import skimage.io as sio

from pozyxpoint import PozyxPoint
from tag import Tag

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("""CREATE TABLE pozyxpoint (
            x real,
            y real,
            z real,
            timestamp real
            )""")

def insert_pozyxpoint(pt):
    with conn:
        c.execute("INSERT INTO pozyxpoint VALUES (:x, :y, :z, :t)", {'x': pt.x, 'y': pt.y, 'z': pt.z, 't': pt.timestamp})


def findAvgLocation(loc):
   xAvg = 0
   yAvg = 0
   zAvg = 0
   tAvg = 0
   elements = 0

   x = 0
   y = 1
   z = 2
   t = 3

#  Find totals
   for l in loc:
      elements += 1
      xAvg += l[x]
      yAvg += l[y]
      zAvg += l[z]
      tAvg += l[t]

   if(elements == 0):
      return PozyxPoint(0, 0, 0, 0)

   xAvg = xAvg / elements
   yAvg = yAvg / elements
   zAvg = zAvg / elements
   tAvg = tAvg / elements

   return PozyxPoint(xAvg, yAvg, zAvg, tAvg)

# Finds the average location of the input timestamp within +/- .75 seconds of the input timestamp
# Returns a PozyxPoint
def get_position(timestamp):
   locations = []
   c.execute("SELECT * FROM pozyxpoint WHERE abs(timestamp-:t) <= .75", {'t': timestamp})
   locations = c.fetchall()
   return findAvgLocation(locations)


def remove_pozyxpoint(timestamp):
    with conn:
        c.execute("DELETE from pozyxpoint WHERE timestamp= :t", {'t': pozyxpoint.timestamp})


def getTimeStamp(date, time):
   dateArr = []
   timeArr = []

   dateArr = date.split('-', 2)
   year = int(dateArr[0])
   month = int(dateArr[1])
   day = int(dateArr[2])

   timeArr = time.split(':', 2)
   hour = int(timeArr[0])
   minute = int(timeArr[1])
   second = int(timeArr[2])

   #print("year " + str(year) + " month "+  str(month) + " day " + str(day) + " time: " + time)
   # We may need to change the timezone but not sure - Caleb Rabbon 6/7/2020
   timestamp = datetime.datetime(year, month, day, hour, minute, second).timestamp()

   return timestamp

def getID(line):
    return line[0]

# Creates a list of tags from a ministock .csv file
def createTagList(filename):
   tagList = []

   with open(filename, 'r') as csv_file:
      csv_reader = csv.reader(csv_file)

      # Skip the header of the csv file
      next(csv_reader)

      for line in csv_reader:
         date = line[2]
         time = line[3]
         tagID = getID(line)
         timestamp = getTimeStamp(date, time)
         tag = Tag(tagID, date, time, timestamp)
         tagList.append(tag)

   return tagList

def createPozyxPoints(filename):
   coordsList = []

   jsonfile = open(filename, 'r')
   for line in jsonfile:
         json_line_list = json.loads(line)
         json_line = json_line_list[0]
         tag = json_line["tagId"]
         timestamp = json_line["timestamp"]

         # Get coordinate values in mm
         xmm = json_line["data"]["coordinates"]["x"]
         ymm = json_line["data"]["coordinates"]["y"]
         zmm = json_line["data"]["coordinates"]["z"]

         # Convert coordiates from mm to inches
         xinch = xmm * .0393701
         yinch = ymm * .0393701
         zinch = zmm * .0393701

         # Convert coordinates from inches to feet
         xfeet = xinch / 12
         yfeet = yinch / 12
         zfeet = zinch / 12
         pt = PozyxPoint(xfeet, yfeet, zfeet, timestamp)

         coordsList.append(pt)

   # Closing jsonfile
   jsonfile.close()

   return coordsList

# Takes in a tagList and the coordinates list and returns a final list of tuples representing the tag and its position
def findAllPositions(tagList, coordinates):
   finalList = []

   # Fill in the coordinate database
   for val in coordinates:
      insert_pozyxpoint(val)

   for tag in tagList:
      pt = get_position(tag.getTimestamp)
      finalList.append([tag, pt])

   return finalList

def checkArgs():
   if len(sys.argv) != 4:
      sys.exit("Usage Error: Not enough arguments \nExample Run: python3 finalGraph.py ministockData.csv pozyxData.json output.csv")

def getTimeStr(timestamp):
    result = datetime.datetime.fromtimestamp(timestamp).strftime("%m/%d/%Y, %H:%M:%S")
    return result

def createGraph(finalList):
   scaler = 2;
   xlist = []
   ylist = []
   zlist = []
   textlist = []

   tag_ind = 0
   pozyx_ind = 1

   for val in finalList:
       pos = val[pozyx_ind]
       xlist.append(pos.x)
       ylist.append(pos.y)
       zlist.append(pos.z)

       tag = val[tag_ind]
       textStr = "<b>Tag ID:</b> " + tag.tagID + "<br><b>Scan Time:</b> " + getTimeStr(pos.timestamp)
       textlist.append(textStr)

   fig = go.Figure(data=[go.Scatter3d(
       x=xlist,
       y=ylist,
       z=zlist,
       hovertemplate=
       '<b>x:</b> %{x:.4f}<br>' +
       '<b>y:</b> %{y:.4f}<br>' +
       '<b>z:</b> %{z:.4f}<br>' +
       '%{text}<extra></extra>',
       text=textlist,
       mode='markers',
       marker=dict(
           size=8,
           color=zlist,            # set color to an array/list of desired values
           colorscale='Viridis',   # choose a colorscale
           opacity=0.8
       )
   )])

   # Below adds a figure at Z coordinate 0
   # Below code from https://community.plotly.com/t/trying-to-add-a-png-jpg-image-to-a-3d-surface-graph-r/4192/2

   # Change the dimensions of the image
   # Parameters: Start Value, End Value, Number of points in between
   x = np.linspace(0, 12*scaler, 500) # 500 = width of image in pixels
   y = np.linspace(0, 18*scaler, 729) # 729 = height of image in pixels
   x, y = np.meshgrid(x, y)
   z = x

   image = sio.imread ("./floorplan.png")
   
   #print(image.shape)
   img = image[:,:, 1]
   Z = 0 * np.ones(z.shape)
   fig.add_surface(x=x, y=y, z=Z,
                   surfacecolor=np.flipud(img),
                   colorscale='matter_r',
                   showscale=False)
   # tight layout
   #fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))

   camera = dict(eye=dict(x=0.0, y=0.0, z=2.5))
   fig.update_layout(scene_camera=camera)
   fig.update_layout(scene=dict(
       xaxis_title='X (ft)',
       xaxis=dict(range=[0, 24]),
       yaxis_title='Y (ft)',
       yaxis=dict(range=[0, 36]),
       zaxis_title='Z (ft)',
       zaxis=dict(range=[0, 10])))

   fig.show()

def outputToCSV(finalList, fileName):
   with open(fileName, 'w') as file:
      writer = csv.DictReader(file)
      file.write("Tag ID:, Date:, Time:, X(ft):, Y(ft):, Z(ft): \n")
      for entry in finalList:
         tag = entry[0]
         pos = entry[1]
         data = str(tag.tagID) + "," + str(tag.date) + "," + str(tag.time) + "," + \
                str(pos.x) + "," + str(pos.y) + "," + str(pos.z) + "\n"
         file.write(data)

def main():
   checkArgs()
   tagList = []
   coordinates = []

   # Contains a tuple of tag and position
   finalList = []

   # Creates the list of tags from the ministock
   tagList = createTagList(sys.argv[1])

   # Creates a list of PozyxPoint objects
   coordinates = createPozyxPoints(sys.argv[2])

   finalList = findAllPositions(tagList, coordinates)

   for tag in finalList:
      print(tag)

   createGraph(finalList)
   
   outputToCSV(finalList, sys.argv[3])

   conn.close()

if __name__== "__main__":
   main()

