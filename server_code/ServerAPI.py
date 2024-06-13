import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import *
from argon2 import PasswordHasher


# GETTERS
@anvil.server.callable
def Authenticate(inputEmail, password):
  try:
    existingRow = app_tables.tblauthentication.get(Email=inputEmail)
    if existingRow['Password'] == hashPassword(password):
      return existingRow['AuthenticationID']
    else: return "404"
  except:
    return "404"

@anvil.server.callable
def getUserInfo(ID, AuthOrUser):
  if not AuthOrUser:
    userRow = app_tables.tbluserdetails.get(UserID=ID)
  elif AuthOrUser:
    userRow = app_tables.tbluserdetails.get(AuthenticationID=ID)
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





# SETTERS

@anvil.server.callable
def hashPassword(plain_password):
    ph = PasswordHasher() # Initialize the Argon2 Password Hasher
    return ph.hash(plain_password)


def newID():
  lastID = app_tables.tblauthentication.search(tables.order_by("AuthenticationID", ascending=False))[0]['AuthenticationID']
  newID = int(LastID) + 1
  while len(str(newNum)) < 6:
    newNum = "0" + str(nuwNum)
  return newNum


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
  newID = newID()
  app_tables.tblauthentication.add_row(AuthenticationID=newID, Email=newEmail, Password=hashPassword(password))
  app_tables.tbluserdetails.add_row(UserID=newID, AuthenticationID=newID, Email=newEmail, DoB=DateOfBirth, Gender=newGender, Group=newGroup, PhoneNumber=newPhoneNumber, BasicRate=baseRate, ExtendedRate=extendRate, PublHolRate=pubHolRate, TFN=newTFN, Profile=profileImg)