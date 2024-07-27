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
    """
    Authenticate a user based on their email.
    
    Input:
    - inputEmail (str): The email of the user.
    
    Output:
    - existingRow (Row or None): The row from the 'users' table if the email exists, otherwise None.
    """
    existingRow = app_tables.users.get(Email=inputEmail)
    return existingRow

@anvil.server.callable
def getUser(ID):
  """
    Retrieve the user row.
    
    Input:
    - ID (str): The UserID of the user.
    
    Output:
    - user (Row or None): The row from the 'users' table corresponding to the UserID, otherwise None.
    """
  user = app_tables.users.get(UserID=ID)
  return user

@anvil.server.callable
def getUserInfo(ID):
    """
    Retrieve detailed information for a user.
    
    Input:
    - ID (str): The UserID of the user.
    
    Output:
    - userRow (Row or None): The row from the 'tbluserdetails' table corresponding to the UserID, otherwise None.
    """
    userRow = app_tables.tbluserdetails.get(UserID=ID)
    return userRow

@anvil.server.callable
def getIfWorking(ID):
    """
    Check if a user is currently working based on their clock-in and clock-out records.
    
    Input:
    - ID (str): The UserID of the user.
    
    Output:
    - (bool): True if the user is currently working, otherwise False.
    """
    try:
        # Search for the user's work records, ordered by ClockIn in descending order
        rows = app_tables.tblworkrecords.search(tables.order_by("ClockIn", ascending=False), UserID=ID)
        if rows:
            topRow = rows[0]
            clockOut = topRow["ClockOut"]
            if clockOut is None:
                return True  # User is still working as they haven't clocked out
        return False  # User is not currently working
    except:
        return False  # No work records found, user is not currently working

@anvil.server.callable
def getWorkRecordsForDownloads(time_filter):
    """
    Retrieve work records based on a time filter for downloading as CSV.
    
    Input:
    - time_filter (str): The time filter for the records, e.g., "All Time", "Today", "Yesterday".
    
    Output:
    - csv_data (str): CSV formatted string of the filtered work records.
    """
    if time_filter == "All Time":
        records = app_tables.tblworkrecords.search()
    else:
        start_date = get_start_date(time_filter)
        records = app_tables.tblworkrecords.search(ClockIn=q.greater_than_or_equal_to(start_date))

    record_data = []
    for record in records:
        # Prepare data for CSV
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
    """
    Retrieve user details for downloading as CSV.
    
    Input:
    - include_all (bool): Whether to include all users or filter out certain users.
    
    Output:
    - csv_data (str): CSV formatted string of the user details.
    """
    users = app_tables.tbluserdetails.search() if include_all else app_tables.tbluserdetails.search(UserID=q.none_of([]))
    user_data = []
    for user in users:
        # Prepare data for CSV
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
    """
    Retrieve all timesheets for a specific user.
    
    Input:
    - ID (str): The UserID of the user.
    
    Output:
    - userWork (SearchIterator or None): An iterator over the user's work records, or None if an error occurs.
    """
    try:
        userWork = app_tables.tblworkrecords.search(tables.order_by("WorkID", ascending=False), UserID=ID)
        return userWork
    except:
        return None

@anvil.server.callable
def getTimesheetsManagers():
    """
    Retrieve all timesheets for managers, ordered by date.
    
    Input: None
    
    Output:
    - timesheets (SearchIterator): An iterator over all work records.
    """
    timesheets = app_tables.tblworkrecords.search(tables.order_by("Date", ascending=False))
    return timesheets

@anvil.server.callable
def getUserSettings(ID):
    """
    Retrieve settings for a specific user.
    
    Input:
    - ID (str): The UserID of the user.
    
    Output:
    - setting (Row or None): The row from the 'tblsettings' table corresponding to the UserID, otherwise None.
    """
    setting = app_tables.tblsettings.get(UserID=ID)
    return setting
  
@anvil.server.callable
def getAllEmployees(callerID, sortBy, includeUser):
    """
    Retrieve all employees, with optional inclusion of the calling user, sorted by a specified field.
    
    Input:
    - callerID (str): The UserID of the calling user.
    - sortBy (str): The field to sort by.
    - includeUser (bool): Whether to include the calling user in the results.
    
    Output:
    - employees (SearchIterator): An iterator over the user details records.
    """
    if includeUser:
        employees = app_tables.tbluserdetails.search(tables.order_by(sortBy, ascending=True))
    else:
        employees = app_tables.tbluserdetails.search(tables.order_by(sortBy, ascending=True), UserID=q.none_of(callerID))
    return employees

@anvil.server.callable
def getTotalBalance(ID):
    """
    Calculate the total unpaid balance for a specific user.
    
    Input:
    - ID (str): The UserID of the user.
    
    Output:
    - payout (float): The total unpaid balance.
    """
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
    """
    Calculate the total approved but unpaid balance for a specific user.
    
    Input:
    - ID (str): The UserID of the user.
    
    Output:
    - payout (float): The total approved but unpaid balance.
    """
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
    """
    Retrieve the work record where the user is currently clocked in.
    
    Input:
    - user_id (str): The UserID of the user.
    
    Output:
    - clocked_in_row (Row or None): The row from the 'tblworkrecords' table where the user is clocked in, otherwise None.
    """
    clocked_in_row = app_tables.tblworkrecords.get(UserID=user_id, ClockOut=None)
    if clocked_in_row:
        # Ensure the ClockIn time is returned in UTC
        clocked_in_row['ClockIn'] = clocked_in_row['ClockIn'].replace(tzinfo=timezone.utc)
    return clocked_in_row

# SETTERS

@anvil.server.callable
def archiveUser(userID, do_or_undo, employmentType):
    """
    Archive a user by updating their employment status and disabling their account. Or vice versa.
    
    Input:
    - userID (str): The UserID of the user. Whether to eanble or disable an account.
    
    Output: Changes the user to not employed, and disables their login. Or vice versa.
    """
    if do_or_undo:
      userDetails = app_tables.tbluserdetails.get(UserID=userID)
      userDetails.update(Employment="Not in Employment")
      user = app_tables.users.get(UserID=userID)
      user.update(enabled=False)
    elif not do_or_undo:
      userDetails = app_tables.tbluserdetails.get(UserID=userID)
      userDetails.update(Employment=employmentType)
      user = app_tables.users.get(UserID=userID)
      user.update(enabled=True)

@anvil.server.callable
def changeSettings(userID, checkedStatus):
    """
    Update the dark mode setting for a user.
    
    Input:
    - userID (str): The UserID of the user.
    - checkedStatus (bool): The new status of the dark mode setting.
    
    Output: None
    """
    userSettings = app_tables.tblsettings.get(UserID=userID)
    userSettings.update(DarkMode=checkedStatus)

@anvil.server.callable
def setClock(ID):
    """
    Clock in a user and create a new work record.
    
    Input:
    - ID (str): The UserID of the user.
    
    Output: None
    """
    user = app_tables.tbluserdetails.get(UserID=ID)
    clockIn = datetime.now().replace(tzinfo=timezone.utc)
    clockDate = date.today()
    app_tables.tblworkrecords.add_row(WorkID=newWorkId(ID), UserID=ID, ClockIn=clockIn, Date=clockDate, Approval=False, Paid=False)

@anvil.server.callable
def updateClock(ID):
    """
    Clock out a user, update the work record with clock-out time and calculate payout.
    
    Input:
    - ID (str): The UserID of the user.
    
    Output: None
    """
    row = app_tables.tblworkrecords.search(tables.order_by("ClockIn", ascending=False), UserID=ID)[0]
    user = app_tables.tbluserdetails.get(UserID=ID)
    clockOutTime = datetime.now().replace(tzinfo=timezone.utc)
    totalWork = clockOutTime - row['ClockIn'].replace(tzinfo=timezone.utc)
    total_hours = totalWork.total_seconds() / 3600  # convert total work time to hours
    if total_hours > 3:
        payout = total_hours * user['ExtendedRate']
        payrate = user['ExtendedRate']
    else:
        weekno = datetime.today().weekday()
        if weekno < 5:  # day is weekday and worked less than 3 hours
            payout = total_hours * user['BasicRate']
            payrate = user['BasicRate']
        else:  # 5 Sat, 6 Sun
            payout = total_hours * user['ExtendedRate']
            payrate = user['ExtendedRate']
    row.update(ClockOut=clockOutTime, Payout=payout, HoursWorked=total_hours, PayRate=payrate)

@anvil.server.callable
def addNewuser(username, newEmail, password, newPhoneNumber, DateOfBirth, newGender, employmentType, newGroup, title, baseRate, extendRate, pubHolRate, newTFN, profileImg):
    """
    Add a new user to the system and create related records.
    
    Input:
    - username (str): The full name of the user.
    - newEmail (str): The email of the user.
    - password (str): The password for the user.
    - newPhoneNumber (str): The phone number of the user.
    - DateOfBirth (date): The date of birth of the user.
    - newGender (str): The gender of the user.
    - employmentType (str): The employment type of the user.
    - newGroup (str): The group of the user.
    - title (str): The title of the user.
    - baseRate (float): The basic pay rate of the user.
    - extendRate (float): The extended pay rate of the user.
    - pubHolRate (float): The public holiday pay rate of the user.
    - newTFN (str): The tax file number of the user.
    - profileImg (Media object): The profile image of the user.
    
    Output: None
    """
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
    """
    Edit an existing user's details.
    
    Input:
    - userID (str): The UserID of the user.
    - username (str): The full name of the user.
    - Email (str): The email of the user.
    - phoneNumber (str): The phone number of the user.
    - dateOfBirth (date): The date of birth of the user.
    - gender (str): The gender of the user.
    - employmentType (str): The employment type of the user.
    - group (str): The group of the user.
    - title (str): The title of the user.
    - baseRate (float): The basic pay rate of the user.
    - extendRate (float): The extended pay rate of the user.
    - pubHolRate (float): The public holiday pay rate of the user.
    - tfn (str): The tax file number of the user.
    - profileImg (Media object): The profile image of the user.
    
    Output: Changes to the user details database.
    """
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
    """
    Update the approval status of work records.
    
    Input:
    - workIDs (list of str): The list of WorkIDs to update.
    - status (bool): The new approval status.
    
    Output: Update timesheets (work record table)
    """
    for workID in workIDs:
        row = app_tables.tblworkrecords.get(WorkID=workID)
        if status:
            row.update(Approval=True)
        else:
            if not row['Approval'] and not row['Paid']:
                row.delete()

@anvil.server.callable
def updatePaymentStatus(workIDs):
    """
    Update the payment status of work records to paid.
    
    Input:
    - workIDs (list of str): The list of WorkIDs to update.
    
    Output: None
    """
    for workID in workIDs:
        row = app_tables.tblworkrecords.get(WorkID=workID)
        if row:
            row.update(Paid=True)

# OTHER FUNCTIONS

def createID():
    """
    Create a new unique UserID.
    
    Output:
    - newID (int): The new unique UserID.
    """
    try:
        lastID = app_tables.users.search(tables.order_by("UserID", ascending=False))[0]['UserID']
        newID = int(lastID) + 1
        return newID
    except:
        return 0  # Return 0 if there are no prior users

def newWorkId(ID):
    """
    Create a new unique WorkID.
    
    Output:
    - newID (int): The new unique WorkID.
    """
    try:
        lastID = app_tables.tblworkrecords.search(tables.order_by("WorkID", ascending=False))[0]['WorkID']
        newID = int(lastID) + 1
        return newID
    except:
        return 0  # Return 0 if there are no prior work records

def get_start_date(time_filter):
    """
    Calculate the start date based on a time filter.
    
    Input:
    - time_filter (str): The time filter, e.g., "Today", "Yesterday", "Last 7 days".
    
    Output:
    - start_date (datetime): The calculated start date.
    """
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
    """
    Convert a list of dictionaries to CSV format.
    
    Input:
    - data (list of dict): The data to convert to CSV.
    
    Output:
    - csv_string (str): The CSV string representation of the data.
    """
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()
