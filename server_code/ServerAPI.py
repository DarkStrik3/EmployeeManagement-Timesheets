import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, date, timedelta


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
def getIfWorking(ID):
    try:
        rows = app_tables.tblworkrecords.search(tables.order_by("ClockIn", ascending=False), UserID=ID)
        if rows:
            topRow = rows[0]
            clockOut = topRow["ClockOut"]
            if clockOut is None:
                return True  # The ClockOut field is empty, meaning that they haven't clocked out yet and are still working
        return False  # The most recent work record has a ClockOut, meaning that the employee is not currently working
    except:
        return False  # The employee has no history of working at all


@anvil.server.callable
def getUserTimesheets(ID):
  try:
    userWork = app_tables.tblworkrecords.search(tables.order_by("WorkID", ascending = False), UserID=ID)
    return userWork
  except:
    return None

@anvil.server.callable
def getTimesheetsManagers():
  timesheets = app_tables.tblworkrecords.search(tables.order_by("Date", ascending=False))
  return timesheets

@anvil.server.callable
def getUserSettings(ID):
  setting = app_tables.tblsettings.get(UserID=ID)
  return setting
  
@anvil.server.callable
def getAllEmployees(callerID, sortBy):
    employees = app_tables.tbluserdetails.search(tables.order_by(sortBy, ascending=True), UserID = q.none_of(callerID))
    return employees

@anvil.server.callable
def getTotalBalance(ID):
    payout = 0.0
    try:
      allWorkRecords = app_tables.tblworkrecords.search(UserID=ID)
      for workRecord in allWorkRecords:
        if workRecord['Payout'] is not None:
          payout += float(workRecord['Payout'])
      return payout
    except:
        return 0.0

@anvil.server.callable
def getTotalApprovedBalance(ID):
    payout = 0.0
    try:
      allWorkRecords = app_tables.tblworkrecords.search(UserID=ID, Approval=True)
      for workRecord in allWorkRecords:
        if workRecord['Payout'] is not None:
          payout += float(workRecord['Payout'])
      return payout
    except:
        return 0.0


@anvil.server.callable
def getClockedInRow(ID):
  row = app_tables.tblworkrecords.search(tables.order_by("ClockIn", ascending=False), UserID=ID)[0]
  return row


# SETTERS


@anvil.server.callable
def archiveUser(userID):
  userDetails = app_tables.tbluserdetails.get(UserID=userID)
  userDetails.update(Employment="Not in Employment")
  user = app_tables.users.get(UserID=userID)
  user.update(enabled=False)
  

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
    lastID = app_tables.tblworkrecords.search(tables.order_by("WorkID", ascending=False))[0]['WorkID']
    newID = int(lastID) + 1
    return newID
  except:
    return 0 # there wasn't any prior work, meaning that the users

@anvil.server.callable
def setClock(ID):
    user = app_tables.tbluserdetails.get(UserID=ID)
    clockIn = datetime.now().replace(tzinfo=None)
    clockDate = date.today()
    app_tables.tblworkrecords.add_row(WorkID=newWorkId(ID), UserID=ID, ClockIn=clockIn, Date=clockDate, PayRate=user['BasicRate'])

@anvil.server.callable
def updateClock(ID):
    row = app_tables.tblworkrecords.search(tables.order_by("ClockIn", ascending=False), UserID=ID)[0]
    clockOutTime = datetime.now().replace(tzinfo=None)
    totalWork = clockOutTime - row['ClockIn'].replace(tzinfo=None)
    total_hours = totalWork.total_seconds() / 3600  # convert total work time to hours
    payout = total_hours * row['PayRate']
    row.update(ClockOut=clockOutTime, Payout=payout, HoursWorked=total_hours)



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
        Title=title,
        Group=newGroup, 
        PhoneNumber=newPhoneNumber, 
        BasicRate=baseRate, 
        ExtendedRate=extendRate, 
        PublHolRate=pubHolRate, 
        TFN=newTFN, 
        Profile=profileImg,
        Employment=employmentType
       )

@anvil.server.callable
def editUser(userID, username, Email, phoneNumber, dateOfBirth, gender, employmentType, group, title, baseRate, extendRate, pubHolRate, tfn, profileImg):
  oldRow = app_tables.tbluserdetails.get(UserID=userID)
  oldRow.update(FullName=username, 
                Email=Email, 
                PhoneNumber=phoneNumber, 
                DoB=dateOfBirth, 
                Gender=gender, 
                Employment=employmentType, 
                Group=group, 
                Title=title, 
                BasicRate=baseRate, 
                ExtendedRate=extendRate, 
                PublHolRate=pubHolRate, 
                TFN=tfn, 
                Profile=profileImg
               )
  user = app_tables.users.get(UserID=userID)
  user.update(email=Email, Group=group)
