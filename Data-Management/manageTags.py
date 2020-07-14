import csv, sys

class Tag:
    def __init__(self,tagID,description,weight,timeEntered,shipDate):
        self.ID = tagID
        self.description = str(description)
        self.weight = weight
        self.timeEntered = str(timeEntered)
        self.shipDate = str(shipDate)
        
        self.lastScanned = None
        self.x = None
        self.y = None
        self.z = None
        
        self.next = None
        self.prev = None

class QueueLinked():

    def __init__(self):     
        self.numTags = 0 #counts ALL tags
        self.head = None #makes linked list of tags

    def addTag(self, tagID, description, weight, timeEntered, shipDate):
        #Creates a new tag using the tag's ID.
        '''Can feed info in now or later with other calls'''
        newTag = Tag(tagID,description,weight,timeEntered,shipDate)
        if self.head == None: #new tag becomes head if there is no head
            self.head = newTag
        else:
            cur = self.head
            while cur.next != None: #continue until end of linked list
                if str(cur.ID) == str(tagID): #if tag already on list, return False
                    return False
                cur = cur.next
            cur.next = newTag #puts newTag at end of linked list
            newTag.prev = cur #ensures each tag knows the tag before/after it
        self.numTags += 1     #keeps track of the size of linked list
        return True
    

    def removeTag(self, tagID):
        #removes the tag associated with its ID
        if self.head == None:
            return False
        if self.head.ID == tagID:
            #if the tag is the head, make the next tag the new head
            if self.head.next: #sets next tag's prev to None if there is a second tag
                self.head.next.prev = None
            self.head = self.head.next #sets to None if there is no tag
            self.numTags -= 1
            return True
        else:
            if self.head.next == None: #no tags other than head, not in list
                return False
            cur = self.head.next
            while cur != None: #look through each tag to find the ID
                if cur.ID == tagID:
                    if cur.next == None:
                        #if at end of list, make prev tag's next = None
                        cur.prev.next = None
                    else:
                        #else, swap prev.next with cur.next and next.prev with cur.prev
                        cur.prev.next = cur.next
                        cur.next.prev = cur.prev
                    self.numTags -= 1
                    return True
                cur = cur.next
            return False #ID does not exist in the linked list

    def returnTagInfo(self, tagID):
        #finds tag and returns its relevant info
        cur = self.head
        while cur != None:
            if cur.ID == tagID:
                return cur.ID,cur.description,cur.weight,cur.shipDate,cur.timeScanned,cur.pos
            cur = cur.next
        return False #if tag cannot be found, return False
        
    ### BELOW ARE CSV FUNCTIONS ###    
        
    def outputToCSV(self, fileName):
        #overwrites CSV file with all tags in LinkedList to CSV file
        with open(fileName, 'w') as file:
            writer = csv.DictReader(file)
            cur = self.head
            file.write("Tag ID:, Description:, Weight (lbs):, Time Entered:, Ship Date:, Last Scanned:, X:, Y:, Z: \n")
            while cur != None:
                entry = str(cur.ID) + "," + cur.description + "," + \
                        str(cur.weight) + "," + str(cur.timeEntered) + "," + \
                        str(cur.shipDate)
                if cur.lastScanned:
                    #if positional data exists, append it
                    entry += "," + str(cur.lastScanned) + "," + str(cur.x) + \
                             "," + str(cur.y) + "," + str(cur.z)
                print(entry)
                file.write(entry)
                file.write("\n")
                cur = cur.next
        return True
        
    def makeFromCSV(self, fileName):
        #reads info from CSV and replaces LinkedList with values
        try:
            with open(fileName, 'r') as file:
                reader = csv.reader(file)
                self.head = None #reset head, thus deleting entire LinkedList
                for row in reader:
                    if row[0].isdigit():
                        self.addTag(row[0],row[1],row[2],row[3],row[4])
            return True
        except FileNotFoundError:
            return False

    def updatePositions(self, fileName):
        #opens a file with tagID, time read, and X, Y, Z positions. Updates those values
        try:
            with open(fileName, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    #iterate across all entries
                    print(row)
                    if row[0].isdigit():
                        #check if this exists in the LL yet
                        cur = self.head
                        exists = True
                        while str(cur.ID) != str(row[0]):
                            if cur.next == None:
                                #entered ID does not exist in memory
                                exists = False
                                break
                            cur = cur.next
                        
                        if exists:
                            #update this Tag with given info if it exists
                            cur.lastScanned = row[1]
                            cur.x = row[2]
                            cur.y = row[3]
                            cur.z = row[4]
            return True
        except FileNotFoundError:
            return False

def main():
    q = QueueLinked()
    
    option = input("Would you like to Build from CSV or Create from scratch? (B or C): ")
    while option.lower() not in ("b", "c"):
        option = input("Please type B to build from CSV or C to create from scratch: ")
    
    fileName = None
    if option == "b":
        #we're building a Linked List from an existing CSV
        fileName = input("Please enter the name of the file (without the extention): ") + ".csv"
        while q.makeFromCSV(fileName) == False:
            fileName = input("That didn't work. Please type the existing file name EXACTLY.") + ".csv"
    
    option = input("\nPlease enter a command (enter 'help' to list options): ")
    while 1:
        #loop until internal break statements are met
        if option.lower() == "help":
            print("\tType 'add' to add a new tag\n",
                  "\tType 'del' to delete an existing tag\n",
                  "\tType 'pos' to update an existing tag's positional arguments\n",
                  "\tType 'q' to update the csv file then quit\n",
                  "\tType 'quit without saving' to quit WITHOUT saving"
                  "\tType 'print' to print out all tag info (useful mainly for debugging)")
                  
        elif option.lower() == "add":
            #add a new tag to the Linked List    
            tagID = input("Enter tag ID: ")
            tagDesc = input("Enter the tag description (ex: Produce, Power Tools, etc): ")
            tagWeight = input("Enter the weight of the shipment (in lbs): ")
            tagTimeEntered = input("Enter the time this tag entered the warehouse (ex: June 20, 2020 = 6/20/2020): ")
            tagShipDate = input("Enter a ship date for the shipment (ex: December 1, 2020 = 12/1/2020): ")
            
            q.addTag(tagID, tagDesc, tagWeight, tagTimeEntered, tagShipDate)
        
        elif option.lower() == "del":
            #delete an existing tag from the LinkedList
            tagID = input("Enter existing tag ID to remove from memory: ")
            while q.removeTag(tagID) == False:
                tagID = input("ERROR: ID does not exist in tag memory: ")
                if tagID == "q":
                    break
            
        elif option.lower() == "pos":
            #update X,Y,Z and the latest read time for all relevant tags
            posFile = input("Enter the name of the csv file with positional data (without the extention): ") + ".csv"
            while q.updatePositions(posFile) == False:
                posFile = input("That file cannot be accessed. Please type the existing file name EXACTLY: ") + ".csv"
                if posFile == "q.csv":
                    break
            
        elif option.lower() == "q":
            #update CSV then quit
            if not fileName:
                fileName = input("Enter the name of the output csv file to make: ") + ".csv"
            q.outputToCSV(fileName)
            break
            
        elif option.lower() == "quit without saving":
            #quit without saving
            break
        
        elif option.lower() == "print":
            cur = q.head
            while cur != None:
                print(cur.ID,cur.description,cur.weight,cur.timeEntered,cur.shipDate, cur.lastScanned,cur.x,cur.y,cur.z)
                cur = cur.next
            
        option = input("\nPlease enter a command (enter 'help' for options): ")

if __name__ == "__main__":
    main()

'''
#test cases below, comment out when testing code
q = QueueLinked()
fileName = "values.csv"
#q.makeFromCSV(values.csv)
#print(q.returnTagInfo(12))

q.addTag(13, "Dell", 500, "1/1/2000", "1/1/2030")
q.addTag(8, "Cookies", 1000, "7/7/2007", "1/1/2022")
q.addTag(83, "Nike", 250, "6/1/2020", "9/1/2020")

#q.returnTagInfo(12)

q.removeTag(8)

#q.outputToCSV(fileName)
q.addTag(99, "Salami", 100, "3/30/2011", "5/4/2025")
q.addTag(67, "Sausages", 1, "11/11/2016", "10/31/2020")
#q.outputToCSV(fileName)
#q.updatePositions("dummy.csv")
q.outputToCSV(fileName)
print("DONE!")
'''