from ._anvil_designer import AnalyticsReportingTemplate
from anvil import *
import anvil.users
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta, timezone
from ..Functions import Other

class AnalyticsReporting(AnalyticsReportingTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.users.get_user()
    self.userID = self.user["UserID"]
    # Any code you write here will run before the form opens.
    self.allRecords = anvil.server.call('getTimesheetsManagers')
    self.allUsers = anvil.server.call('getAllEmployees', self.userID, "UserID", True)
    self.refreshGraphs()

  def refreshGraphs(self, **event_args):
    timeChoice = self.ddDates.selected_value
    typeChoice = self.ddGroup.selected_value
    infoChoice = self.ddInfoShown.selected_value

    # Filter records based on the selected time range
    filteredRecords = self.filterRecordsByTime(self.allRecords, timeChoice)
    
    # Calculate and display total payout, total time worked, and total employees
    totalPayout, totalTime, totalEmployees = self.calculateTotals(filteredRecords, typeChoice)
    
    self.lblPayout.text = f"${totalPayout:.2f}"
    self.lblTime.text = f"{totalTime:.2f}h"
    self.lblEmployees.text = str(totalEmployees)

    typeArr = []
    infoArr = []

    if typeChoice == "Groups":
      typeArr = ["Warehouse", "Management", "Admin", "Accounting"]
      warehouse = 0
      management = 0
      admin = 0
      accounting = 0
      for record in filteredRecords:
        recordUser = self.allUsers[record['UserID']]
        if recordUser['Group'] == "Warehouse":
          if infoChoice == "Payout":
            warehouse += record['Payout']
          elif infoChoice == "Time Worked":
            warehouse += record['HoursWorked']
        elif recordUser['Group'] == "Management":
          if infoChoice == "Payout":
            management += record['Payout']
          elif infoChoice == "Time Worked":
            management += record['HoursWorked']
        elif recordUser['Group'] == "Admin":
          if infoChoice == "Payout":
            admin += record['Payout']
          elif infoChoice == "Time Worked":
            admin += record['HoursWorked']
        elif recordUser['Group'] == "Accounting":
          if infoChoice == "Payout":
            accounting += record['Payout']
          elif infoChoice == "Time Worked":
            accounting += record['HoursWorked']
      infoArr = [warehouse, management, admin, accounting]

    elif typeChoice == "Employment Type":
      typeArr = ["Full Time", "Part Time", "Contractor"]
      fullTime = 0
      partTime = 0
      contractor = 0
      for record in filteredRecords:
        recordUser = self.allUsers[record['UserID']]
        if recordUser['Employment'] == "Part-Time":
          if infoChoice == "Payout":
            partTime += record['Payout']
          elif infoChoice == "Time Worked":
            partTime += record['HoursWorked']
        elif recordUser['Employment'] == "Full-Time":
          if infoChoice == "Payout":
            fullTime += record['Payout']
          elif infoChoice == "Time Worked":
            fullTime += record['HoursWorked']
        elif recordUser['Employment'] == "Contractor":
          if infoChoice == "Payout":
            contractor += record['Payout']
          elif infoChoice == "Time Worked":
            contractor += record['HoursWorked']
      infoArr = [fullTime, partTime, contractor]

    elif typeChoice == "Employees":
      for user in self.allUsers:
        typeArr.append(user['FullName'])
      totalAmount = 0
      for record in filteredRecords:
        if infoChoice == "Payout":
          totalAmount += float(record['Payout'])
        elif infoChoice == "Time Worked":
          totalAmount += float(record['HoursWorked'])
      infoArr.append(totalAmount)

    # Set Plots
    self.plotPieDistribution.data = go.Pie(labels=typeArr, values=infoArr, hole=0.3)
    self.plotPieDistribution.layout.update(margin=dict(l=20, r=20, t=20, b=20))

    self.plotGroupStats.data = go.Bar(x=typeArr, y=infoArr)
    self.plotGroupStats.layout.update(margin=dict(l=20, r=20, t=20, b=20))

    # Implement bottom graph (e.g., Date distribution)
    self.plotDateDistribution.data = self.getDateDistribution(filteredRecords, infoChoice)
    self.plotDateDistribution.layout.update(margin=dict(l=20, r=20, t=20, b=20))

    # Refresh the employee info table
    self.refreshEmployeeInfoTable()

  def refreshEmployeeInfoTable(self, **event_args):
    infoChoice = self.ddTableInfoShown.selected_value
    employeeData = []

    for user in self.allUsers:
      name = user['FullName']
      if infoChoice == "Payout":
        totalPayout = sum(record['Payout'] for record in self.allRecords if record['UserID'] == user['UserID'])
        employeeData.append({'name': name, 'info': f"${totalPayout:.2f}"})
      elif infoChoice == "Time Worked":
        totalTime = sum(record['HoursWorked'] for record in self.allRecords if record['UserID'] == user['UserID'])
        employeeData.append({'name': name, 'info': f"{totalTime:.2f}h"})
      elif infoChoice == "Pay Rate":
        payRate = user['BasicRate']
        extendedRate = user['ExtendedRate']
        holidayRate = user['PublHolRate']
        employeeData.append({'name': name, 'info': f"{payRate}, {extendedRate}, {holidayRate}"})
      elif infoChoice == "User ID":
        userID = user['UserID']
        employeeData.append({'name': name, 'info': str(userID)})

    # Bind the data to the repeating panel
    self.rpTable.items = employeeData

  def filterRecordsByTime(self, records, timeChoice, **event_args):
    # Implement filtering logic based on timeChoice
    if timeChoice == "Today":
      start_date = datetime.now().date()
    elif timeChoice == "Yesterday":
      start_date = datetime.now().date() - timedelta(days=1)
    elif timeChoice == "Last 7 days":
      start_date = datetime.now().date() - timedelta(days=7)
    elif timeChoice == "Last Fortnight":
      start_date = datetime.now().date() - timedelta(days=14)
    elif timeChoice == "Last Month":
      start_date = datetime.now().date().replace(day=1) - timedelta(days=1)
      start_date = start_date.replace(day=1)
    elif timeChoice == "All Time":
      start_date = datetime.min.date()
    else:
      start_date = datetime.min.date()

    end_date = datetime.now().date() + timedelta(days=1)
    return [record for record in records if start_date <= record['ClockIn'].date() < end_date]

  def calculateTotals(self, records, typeChoice, **event_args):
    totalPayout = 0
    totalTime = 0
    totalEmployees = set()

    for record in records:
      totalPayout += record['Payout']
      totalTime += record['HoursWorked']
      totalEmployees.add(record['UserID'])
    
    return totalPayout, totalTime, len(totalEmployees)

  def getDateDistribution(self, records, infoChoice, **event_args):
    # Implement logic for date distribution bar chart
    date_dict = {}
    for record in records:
      date_str = record['ClockIn'].strftime('%Y-%m-%d')
      if date_str not in date_dict:
        date_dict[date_str] = 0
      if infoChoice == "Payout":
        date_dict[date_str] += record['Payout']
      elif infoChoice == "Time Worked":
        date_dict[date_str] += record['HoursWorked']
    
    dates = list(date_dict.keys())
    values = list(date_dict.values())

    return go.Bar(x=dates, y=values)

  def downloadUserDetails(self, **event_args):
    filter_option = confirm("Are you sure you want to download all user details? (User profile images will not be included)")
    if filter_option:
        csv_data = anvil.server.call('getUserDetailsForDownload', True)
    else:
        return  # Cancel was selected, do nothing

    # Encode the CSV data to bytes
    csv_bytes = csv_data.encode('utf-8')

    # Create a file and download it
    media = anvil.BlobMedia('text/csv', csv_bytes, name='user_details.csv')
    download(media)



  def downloadWorkRecords(self, **event_args):
    try:
      filter_option = confirm("Do you want to download all data or filtered data based on the selected time period?", buttons=["All", "Filtered", "Cancel"])
      if filter_option == "All":
          csv_data = anvil.server.call('getWorkRecordsForDownloads', "All Time")
      elif filter_option == "Filtered":
          time_choice = self.ddDates.selected_value
          csv_data = anvil.server.call('getWorkRecordsForDownloads', time_choice)
      else:
          return  # Cancel was selected, do nothing
  
      # Encode the CSV data to bytes
      csv_bytes = csv_data.encode('utf-8')
  
      # Create a file and download it
      media = anvil.BlobMedia('text/csv', csv_bytes, name='work_records.csv')
      download(media)
    except:
      alert("There isn't any data to download for the specified time period.")

