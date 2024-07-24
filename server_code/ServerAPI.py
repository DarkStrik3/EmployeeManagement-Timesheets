import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, date, timedelta, timezone
import csv
import io


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
def getWorkRecordsForDownloads(time_filter):
    if time_filter == "All Time":
        records = app_tables.tblworkrecords.search()
    else:
        start_date = get_start_date(time_filter)
        records = app_tables.tblworkrecords.search(ClockIn=q.greater_than_or_equal_to(start_date))

    record_data = []
    for record in records:
        record_data.append({
            'WorkID': record['WorkID'],
            'UserID': record['UserID'],
            'HoursWorked': record['HoursWorked'],
            'PayRate': record['PayRate'],
            'ClockIn': str(record['ClockIn']) if record['ClockIn'] else '',
            'ClockOut': str(record['ClockOut']) if record['ClockOut'] else '',
            'Date': str(record['Date']),
            'Payout': record['Payout'],
            'Approval': record['Approval'],
            'Paid': record['Paid']
        })
    csv_data = convert_to_csv(record_data)
    return csv_data

@anvil.server.callable
def getUserDetailsForDownload(include_all):
    users = app_tables.tbluserdetails.search() if include_all else app_tables.tbluserdetails.search(UserID=q.none_of([]))
    user_data = []
    for user in users:
        user_data.append({
            'UserID': user['UserID'],
            'FullName': user['FullName'],
            'Email': user['Email'],
            'PhoneNumber': user['PhoneNumber'],
            'DoB': str(user['DoB']),
            'Gender': user['Gender'],
            'Employment': user['Employment'],
            'Group': user['Group'],
            'Title': user['Title'],
            'BasicRate': user['BasicRate'],
            'ExtendedRate': user['ExtendedRate'],
            'PublHolRate': user['PublHolRate'],
            'TFN': user['TFN']
        })
    csv_data = convert_to_csv(user_data)
    return csv_data



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
def getAllEmployees(callerID, sortBy, includeUser):
    if includeUser:
      employees = app_tables.tbluserdetails.search(tables.order_by(sortBy, ascending=True))
    else:
      employees = app_tables.tbluserdetails.search(tables.order_by(sortBy, ascending=True), UserID = q.none_of(callerID))
    return employees

@anvil.server.callable
def getTotalBalance(ID):
    payout = 0.0
    try:
      allWorkRecords = app_tables.tblworkrecords.search(UserID=ID)
      for workRecord in allWorkRecords:
        if workRecord['Payout'] is not None and not workRecord['Paid']:
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
        if workRecord['Payout'] is not None and not workRecord['Paid']:
          payout += float(workRecord['Payout'])
      return payout
    except:
        return 0.0


@anvil.server.callable
def getClockedInRow(user_id):
    clocked_in_row = app_tables.tblworkrecords.get(UserID=user_id, ClockOut=None)
    if clocked_in_row:
        # Ensure the ClockIn time is returned in UTC
        clocked_in_row['ClockIn'] = clocked_in_row['ClockIn'].replace(tzinfo=timezone.utc)
    return clocked_in_row


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
  

@anvil.server.callable
def setClock(ID):
    user = app_tables.tbluserdetails.get(UserID=ID)
    clockIn = datetime.now().replace(tzinfo=timezone.utc)
    clockDate = date.today()
    app_tables.tblworkrecords.add_row(WorkID=newWorkId(ID), UserID=ID, ClockIn=clockIn, Date=clockDate, Approval=False, Paid=False)

@anvil.server.callable
def updateClock(ID):
    row = app_tables.tblworkrecords.search(tables.order_by("ClockIn", ascending=False), UserID=ID)[0]
    user = app_tables.tbluserdetails.get(UserID=ID)
    clockOutTime = datetime.now().replace(tzinfo=timezone.utc)
    totalWork = clockOutTime - row['ClockIn'].replace(tzinfo=timezone.utc)
    total_hours = totalWork.total_seconds() / 3600  # convert total work time to hours
    if total_hours > 3:
      payout = total_hours * user['ExtendedRate']
      payrate = user['ExtendedRate']
    else:
      weekno = datetime.datetime.today().weekday()
      if weekno < 5: # day is weekday and worked less than 3 hours
        payout = total_hours * user['BasicRate']
        payrate = user['BasicRate']
      else:  # 5 Sat, 6 Sun
        payout = total_hours * user['ExtendedRate']
        payrate = user['ExtendedRate']
    row.update(ClockOut=clockOutTime, Payout=payout, HoursWorked=total_hours, PayRate=payrate)



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

@anvil.server.callable
def updateApprovalStatus(workIDs, status):
  for workID in workIDs:
    row = app_tables.tblworkrecords.get(WorkID=workID)
    if status:
      row.update(Approval=True)
    else:
      if not row['Approval'] and not row['Paid']:
        row.delete()

@anvil.server.callable
def updatePaymentStatus(workIDs):
  for workID in workIDs:
    row = app_tables.tblworkrecords.get(WorkID=workID)
    if row:
      row.update(Paid=True)

# OTHER FUNCTIONS:

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

def get_start_date(time_filter):
    if time_filter == "Today":
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_filter == "Yesterday":
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    elif time_filter == "Last 7 days":
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
    elif time_filter == "Last Fortnight":
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=14)
    elif time_filter == "Last Month":
        return (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1)
    else:
        return datetime.min

def convert_to_csv(data):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

