from ._anvil_designer import AnalyticsReportingTemplate
from anvil import *
import anvil.users
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

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
    typeArr = []
    infoArr = []
    if typeChoice == "Groups":
      typeArr = ["Warehouse", "Management", "Admin", "Accounting"]
      warehouse = 0
      management = 0
      admin = 0
      accounting = 0
      for record in self.allRecords:
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
      for record in self.allRecords:
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
      for record in self.allRecords:
        if infoChoice == "Payout":
          totalAmount += float(record['Payout'])
        elif infoChoice == "Time Worked":
          totalAmount += float(record['HoursWorked'])
      infoArr.append(totalAmount)

    # Set Plots
    self.plotPieDistribution.data = go.Pie(labels=typeArr, values=infoArr)
    self.plotGroupStats.data = go.Bar(x=typeArr, y=infoArr)
    
    
    
    