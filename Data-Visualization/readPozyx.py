import json

# Opening JSON file
f = open('positions.json', 'r')

# returns JSON object as a dictionary
data = json.load(f)

tagTimestamp = 1589960921

# Iterating through the json list
coordinates = []
for cur in data["positions"]:
    timestamp = cur["timestamp"]
    if (abs(timestamp - tagTimestamp) <= 0.3):
        x = cur["data"]["coordinates"]["x"]
        y = cur["data"]["coordinates"]["y"]
        z = cur["data"]["coordinates"]["z"]
        #print(timestamp)
        coordinates.append([x, y, z])

print(coordinates)
# Closing file
f.close()
