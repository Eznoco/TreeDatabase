#
# Made by Ezra Billings and Kieran Larrabee
#
#I realized that there is a much easier way to do this, but by organizing into classes I think it makes it easier to grow in the future
#For example, if later I needed a way get all the trees for a species object, I could add a method called getTreeList() to species which could returen a bunch of tree objects
import csv
import mariadb
from datetime import datetime


CSV_FILE = "Street_Tree_Inventory_-_Active_Records.csv"
#CSV_FILE = "tree.csv"

##############################################################
# Database class wraps mariadb connection and cursor function#
##############################################################
class Db:
    #sets up database configuration. tells program how to connect to database. This part was required me to look things up since it was quite challenging
    config = {
        "user": "root", 
        "password": "",
        "host": "127.0.0.1",
        "port": 3306,
        "database": "tree"
    }

    def __init__(self):
        self.cursor = None #how to work with queries
        self.connection = None #connection to the database

    def dbConnect(self):
        self.connection = mariadb.connect(
            user = self.config["user"], 
            password = self.config["password"], 
            host = self.config["host"], 
            port = self.config["port"], 
            database = self.config["database"] 
        )
        self.cursor = self.connection.cursor()

    #executes a sql query
    def execute(self, query, row):
        return self.cursor.execute(query, row)

    #returns the next row returned by a SELECT statement
    def fetchone(self): 
        return self.cursor.fetchone()

    #returns the auto_incremented number
    def lastrowid(self):
        return self.cursor.lastrowid

    #the way to end transaction is by commiting it
    def commit(self):
        return self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
 
################
# Species class#
################
class Species:
    #Used by the execute method to check if a species is already in the database and to fill the obect with what's in the database
    RESTORE_BY_NAME_QUERY = "SELECT id, name, mature_size, functional_type FROM species WHERE name = ?" 
    
    #Used by execute method to insert a species into the database
    INSERT_STATEMENT = "INSERT INTO species (name, mature_size, functional_type) VALUES (?, ?, ?)"
    
    #constructor
    def __init__(self, db, name, matureSize, functionalType):
        self.oid = 0
        self.db = db
        self.name = name
        self.matureSize = matureSize
        self.functionalType = functionalType

    #toString
    def __str__(self):
        return (
            f"Species {self.oid}: "
            f"Name({self.name}), "
            f"MatureSize({self.matureSize}), "
            f"FunctionalType({self.functionalType}) "
        )

    #calls execute with the select statement then fills in the fields of the object then returns the id. returns 0 if not found
    def restoreByName(self):
        self.db.execute(self.RESTORE_BY_NAME_QUERY, (self.name,))
        row = self.db.fetchone() #returns the first row aquired by the execute method
        if row:
            self.oid = row[0]
            self.name = row[1]
            self.matureSize = row[2]
            self.functionalType = row[3]
            return self.oid
        return 0

    #Calls execute with the insert statement
    def insert(self):
        if self.oid == 0: #if it already has an Id then it's already in the database
            self.db.execute(self.INSERT_STATEMENT, (self.name, self.matureSize, self.functionalType))
            self.oid = self.db.lastrowid()
        return self.oid

#################
# Neighboorhood #
#################
class Neighborhood:
    RESTORE_BY_NAME_QUERY = "SELECT id, name FROM neighborhood WHERE name = ?"
    INSERT_STATEMENT = "INSERT INTO neighborhood (name) VALUES (?)"

    def __init__(self, db, name):
        self.oid = 0
        self.db = db
        self.name = name

    def __str__(self):
        return (
            f"Neighborhood {self.oid}: "
            f"Name({self.name}), "
        )

    def restoreByName(self):
        self.db.execute(self.RESTORE_BY_NAME_QUERY, (self.name,))
        row = self.db.fetchone()
        if row:
            self.oid = row[0]
            self.name = row[1]
            return self.oid
        return 0

    def insert(self):
        if self.oid == 0:
            self.db.execute(self.INSERT_STATEMENT, (self.name,))
            self.oid = self.db.lastrowid()
        return self.oid

####################
# site_description #
####################
class SiteDescription:
    RESTORE_BY_PARTS_QUERY = """
        SELECT id, site_type, site_size, site_width, wires, improvement 
        FROM site_description 
        WHERE site_type = ? AND site_size = ? AND site_width = ? AND wires = ? AND improvement = ?
    """
    INSERT_STATEMENT = "INSERT INTO site_description (site_type, site_size, site_width, wires, improvement) VALUES (?, ?, ?, ?, ?)"

    def __init__(self, db, siteType, siteSize, siteWidth, wires, improvement):
        self.oid = 0
        self.db = db
        self.siteType = siteType
        self.siteSize = siteSize
        self.siteWidth = siteWidth
        self.wires = wires 
        self.improvement = improvement 

    def __str__(self):
        return (
            f"SiteDescription {self.oid}: "
            f"Type({self.siteType}), "
            f"Size({self.siteSize}), "
            f"Width({self.siteWidth}), "
            f"Wires({self.wires}), "
            f"Improvement({self.improvement}), "
        )

    def restoreByParts(self):
        self.db.execute(self.RESTORE_BY_PARTS_QUERY, (self.siteType, self.siteSize, self.siteWidth, self.wires, self.improvement))
        row = self.db.fetchone()
        if row:
            self.oid = row[0]
            self.siteType = row[1]
            self.siteSize = row[2]
            self.siteWidth = row[3]
            self.wires = row[4]
            self.improvement = row[5]
            return self.oid
        return 0

    def insert(self):
        if self.oid == 0:
            self.db.execute(self.INSERT_STATEMENT, (self.siteType, self.siteSize, self.siteWidth, self.wires, self.improvement))
            self.oid = self.db.lastrowid()
        return self.oid

###########
# address #
###########
class Address:
    RESTORE_BY_PARTS_QUERY = """
        SELECT id, street_address, city, state, zip, neighborhood_id 
        FROM address 
        WHERE street_address = ? AND city = ? AND state = ? AND zip = ?
    """
    INSERT_STATEMENT = "INSERT INTO address (street_address, city, state, zip, neighborhood_id) VALUES (?, ?, ?, ?, ?)"

    def __init__(self, db):
        self.oid = 0
        self.db = db
        self.streetAddress = None
        self.city = None
        self.state = None
        self.zip = None
        self.neighborhoodId = None

    def __str__(self):
        return (
            f"Address {self.oid}: "
            f"StreetAddress({self.streetAddress}), "
            f"City({self.city}), "
            f"state({self.state}), "
            f"Zip({self.zip}), "
            f"NeighborhoodId({self.neighborhoodId}), "
        )

    #Sometimes the state is the full name and sometimes it's only two letters. Only Oregon is here since it is the only state in the table, but more can be added if needed
    def findState(self, state):
        if len(state) == 2:
            return state
        mapping = {"OREGON":"OR"} 
        value = mapping[state]
        if value == None:
            print(f"Error: unknown state {state}")
        return value

    #parses the address into its individual parts
    def parse(self, wholeAddress):
        parts = wholeAddress.strip().split(",")
        self.streetAddress = parts[0].strip()
        self.city = parts[1].strip()
        self.state = self.findState(parts[2].strip())
        self.zip = parts[3].strip()

    #We can't get this from the csv so we need a method to set it later
    def setNeighborhoodId(self, nId):
        self.neighborhoodId = nId 

    def restoreByParts(self):
        self.db.execute(self.RESTORE_BY_PARTS_QUERY, (self.streetAddress, self.city, self.state, self.zip))
        row = self.db.fetchone()
        if row:
            self.oid = row[0]
            self.streetAddress = row[1]
            self.city = row[2]
            self.state = row[3]
            self.zip = row[4]
            self.neighborhoodId = row[5]
            return self.oid
        return 0

    def insert(self):
        if self.oid == 0:
            self.db.execute(self.INSERT_STATEMENT, (self.streetAddress, self.city, self.state, self.zip, self.neighborhoodId))
            self.oid = self.db.lastrowid()
        return self.oid
        
####################
# Tree #
####################
class Tree:
    INSERT_STATEMENT = """
        INSERT INTO tree (x_coord, y_coord, date_inventoried, diameter, tree_condition, address_id, species_id, site_description_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    def __init__(self, db, x, y, inventoryDate, diameter, condition):
        self.oid = 0
        self.db = db
        self.x = x
        self.y = y
        if len(inventoryDate) > 19:
            inventoryDate = inventoryDate[:-3] #gets rid of last three characters (timezone)
        self.inventoryDate = datetime.strptime(inventoryDate, "%Y/%m/%d %H:%M:%S") #converts string to datetime type
        self.diameter = diameter
        self.condition = condition
        self.addressId = None
        self.siteDescriptionId = None
        self.speciesId = None

    def setAddressId(self, aId):
        self.addressId = aId

    def setSpeciesId(self, sId):
        self.speciesId = sId

    def setSiteDescriptionId(self, sdId):
        self.siteDescriptionId = sdId

    def __str__(self):
        return (
            f"Tree {self.oid}: "
            f"X({self.x}), "
            f"Y({self.y}), "
            f"Date Inventoried({self.inventoryDate}), "
            f"Diameter({self.diameter}), "
            f"Condition({self.condition}), "
            f"AddressId({self.addressId}), "
            f"SpeciesId({self.speciesId}), "
            f"SiteDescriptionId({self.siteDescriptionId}) "
        )

    def insert(self):
        if self.oid == 0:
            self.db.execute(self.INSERT_STATEMENT, (self.x, self.y, self.inventoryDate, self.diameter, self.condition, self.addressId, self.speciesId, self.siteDescriptionId))
            self.oid = self.db.lastrowid()
        return self.oid
        
################
# main program #
################
def main():
    db = Db() #instantiate database wrapper
    db.dbConnect() #tell program to connect to the database
    csvfile = open(CSV_FILE, newline = "", encoding = 'utf-8-sig') #ran into issue with UTF8 encoding so i used exel export format. I had AI help me with this
    reader = csv.DictReader(csvfile) #contents of csv
    speciesCount = 0
    siteDescriptionCount = 0
    neighborhoodCount = 0
    addressCount = 0
    treeCount = 0
    for row in reader: #step through every row in csv file
        #species
        species = Species(db, row["SPECIES"].strip(), row["MATURE_SIZE"].strip(), row["FUNCTIONAL_TYPE"].strip()) #Creating a species object with data from relavent colomns
        speciesId = species.restoreByName() #checks if it's already in the table
        if speciesId == 0: #If its not in the table
            speciesId = species.insert() #insert it into the table and keep the ID for later
            #db.commit() #execute may auto commit but this is just in case it doesn't
            speciesCount += 1

        #Neighborhood. Same idea as species
        neighborhood = Neighborhood(db, row["Neighborhood"].strip())
        neighborhoodId = neighborhood.restoreByName()
        if neighborhoodId == 0:
            neighborhoodId = neighborhood.insert()
            #db.commit()
            neighborhoodCount += 1

        #Site Description. Similar to above
        siteDescription = SiteDescription(db, row["Site_Type"].strip(), row["Site_Size"].strip(), row["Site_Width"], row["Wires"], row["SITE_IMPROVEMENT"].strip())
        siteDescriptionId = siteDescription.restoreByParts()
        if siteDescriptionId == 0:
            siteDescriptionId = siteDescription.insert()
            #db.commit()
            siteDescriptionCount += 1

        #Address. Similar to above
        address = Address(db)
        address.parse(row["Address"])
        addressId = address.restoreByParts()
        if addressId == 0:
            address.setNeighborhoodId(neighborhoodId)
            addressId = address.insert()
            #db.commit()
            addressCount += 1

        #We're assuming that every tree is unique so we're not checking if it's already there
        tree = Tree(db, row["X"], row["Y"], row["Date_Inventoried"], row["DIAMETER"], row["Condition"].strip())
        tree.setAddressId(addressId)
        tree.setSpeciesId(speciesId)
        tree.setSiteDescriptionId(siteDescriptionId)
        tree.insert()
        #db.commit()
        treeCount += 1

    print("Rows Inserted: ") 
    print(f"    Tree: {treeCount}")
    print(f"    Species: {speciesCount}")
    print(f"    Neighborhood: {neighborhoodCount}")
    print(f"    Site Description: {siteDescriptionCount}")
    print(f"    Address: {addressCount}")

    db.commit()
    db.close() #closing the database connection 
    csvfile.close() #close the csv file

if __name__ == "__main__":
    main()


