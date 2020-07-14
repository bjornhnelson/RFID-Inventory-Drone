class Tag:

    def __init__(self, tagID, date, time, timestamp):
        self.tagID = tagID
        self.date = date
        self.time = time
        self.timestamp = timestamp

    @property
    def getTimestamp(self):
        return '{}'.format(self.timestamp)

    def __repr__(self):
        return "Tag ('{}', '{}', '{}', '{}')".format(self.tagID, self.date, self.time, self.timestamp)
