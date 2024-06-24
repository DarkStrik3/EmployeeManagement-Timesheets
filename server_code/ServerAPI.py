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
  try:
    rows = app_tables.tblworkrecords.search(tables.order_by("ClockIn"), ascending=False)
    topRow = rows[0]
    clockOut = row["ClockOut"] # checks if the most recent work has a clock out
    if clockOut is None:
      return True # The Clockout row is empty, meaning that they haven't clocked out yet and are still working
    else:
      return False # The most recent work record has a clock out, meaning that the employee is going to start working.
  except:
    return False # The employee has no history of working at all.


@anvil.server.callable
def getUserTimesheets(ID, approved):
  try:
    userWork = app_tables.tblworkrecords.search(tables.order_by("Date"), ascending = False, UserID=ID, Approval=approved)
    return userWork
  except:
    return None


@anvil.server.callable
def getTimesheetsManagers():
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
  

def createID():
  try:
    lastID = app_tables.users.search(tables.order_by("UserID", ascending=False))[0]['UserID']
    newID = int(lastID) + 1
    return newID
  except:
    return 0 # there aren't any prior users, meaning that a new user would have the ID of 0.

def newWorkId(ID):
  try:
    lastID = app_tables.tblworkrecords.search(tables.order_by("WorkID", ascending=False, UserID=ID))[0]['WorkID']
    newID = int(lastID) + 1
    return newID
  except:
    return 0 # there wasn't any prior work, meaning that the users


@anvil.server.callable
def setClock(ID):
  clockStatus = getIfWorking(ID)
  if not clockStatus:
    user = app_tables.tbluserdetails.get(UserID=ID)
    clockIn = datetime.now()
    clockDate = date.today()
    app_tables.tblworkrecords.add_row(UserID=ID, WorkID=newWorkId(ID), ClockIn=clockIn, PayRate=user['BasicRate'], Date=clockDate)
  else:
    row = app_tables.tblworkrecords.search(tables.order_by("ClockIn", ascending=False, UserID=ID))[0]
    clockOutTime = datetime.date.now()
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