class PozyxPoint:

    def __init__(self, x, y, z, timestamp):
        self.x = x
        self.y = y
        self.z = z
        self.timestamp = timestamp

    @property
    def getTimestamp(self):
        return '{}'.format(self.timestamp)

    def __repr__(self):
        return "PozyxPoint ('{}', '{}', '{}', '{}')".format(self.x, self.y, self.z, self.timestamp)
