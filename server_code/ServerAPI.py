import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import *

# GETTERS
@anvil.server.callable
def Authenticate(inputEmail):
    existingRow = app_tables.users.get(Email=inputEmail)
    return existingRow

@anvil.server.callable
def getUserInfo(ID):
  userRow = app_tables.tbluserdetails.get(UserID=ID)
  return userRow

@anvil.server.callable
def getIfWorking(userID):
  row = app_tables.tblworkrecords.search(tables.order_by("ClockIn"), ascending=False)
  try:
    clockOut = row["ClockOut"] # checks if the most recent work has a clock out
    return False
  except:
    True


@anvil.server.callable
def getTimesheets():
  timesheets = app_tables.tblworkrecords.search(tables.order_by("Date"), ascending=False)
  return timesheets

@anvil.server.callable
def getUserSettings(ID):
  setting = app_tables.tblsettings.get(UserID=ID)
  return setting
  


# SETTERS

@anvil.server.callable
def changeSettings(userID, checkedStatus):
  userSettings = app_tables.tblsettings.get(UserID=userID)
  userSettings.update(DarkMode=checkedStatus)
  

@anvil.server.callable
def createID():
  try:
    lastID = app_tables.users.search(tables.order_by("UserID", ascending=False))[0]['UserID']
    newID = int(lastID) + 1
    return newID
  except:
    return 0 # there aren't any prior users, meaning that a new user would have the ID of 0.


def newWorkId():
  # grabs the highest reference number from the work records table
  lastID = app_tables.tblworkrecords.search(tables.order_by("WorkID", ascending=False))[0]['WorkID']
  newNum = int(lastID) + 1 # adds 1 number to create the new highest reference ID
  while len(str(newNum)) < 6: # loop to add 0's to the WorkId to have matching lengths
    newNum = "0" + str(newNum)
  newId = str(newNum) # changes to string
  return newId # the new ID is returned for use in creating a new ID

@anvil.server.callable
def setClock(userID, clockStatus):
  user = app_tables.tbluserdetails.get(UserID=userID)
  if clockStatus:
    app_tables.tblworkrecords.add_row(UserID=user["UserID"], ClockIn=datetime.now(), PayRate=user['BasicRate'], Date=date.today(), WorkID=newWorkID())
  else:
    row = app_tables.tblworkrecords.search(tables.order_by("ClockIn", ascending=False, UserID = userId))[0]
    clockOutTime = datetime.now()
    totalWork = clockOutTime - row['ClockIn']
    payout = totalWork * row['PayRate']
    row.update(ClockOut=clockOutTime, Payout=payout, HoursWorked=totalWork)


@anvil.server.callable
def addNewuser(username, newEmail, password, newPhoneNumber, DateOfBirth, newGender, employmentType, newGroup, title, baseRate, extendRate, pubHolRate, newTFN, profileImg):
    newID = int(createID())
    user = anvil.users.signup_with_email(newEmail, password)
    user = app_tables.users.get(email=newEmail)
    user.update(UserID=newID, Group=newGroup)
    app_tables.tblsettings.add_row(UserID=newID, DarkMode=False)
    app_tables.tbluserdetails.add_row(
        UserID=newID, 
        FullName=username,
        Email=newEmail, 
        DoB=DateOfBirth, 
        Gender=newGender, 
        Group=newGroup, 
        PhoneNumber=newPhoneNumber, 
        BasicRate=baseRate, 
        ExtendedRate=extendRate, 
        PublHolRate=pubHolRate, 
        TFN=newTFN, 
        Profile=profileImg
    )