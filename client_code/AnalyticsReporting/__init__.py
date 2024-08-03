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
        """
        Purpose: Initialize the AnalyticsReporting form with default properties.
        Input: **properties (dict) - properties to initialize the form.
        Process: Sets form components, binds data, and retrieves initial data from the server.
        Output: None
        """
        self.init_components(**properties)  # Initialize form components with properties
        self.user = anvil.users.get_user()  # Get the current user
        self.userID = self.user["UserID"]  # Store the user's ID
        # Any code you write here will run before the form opens.
        self.allRecords = anvil.server.call('getTimesheetsManagers')  # Retrieve all timesheet records for managers
        self.allUsers = anvil.server.call('getAllEmployees', self.userID, "UserID", True)  # Retrieve all employees' data
        self.refreshGraphs()  # Refresh the graphs with the retrieved data

    def refreshGraphs(self, **event_args):
        """
        Purpose: Refresh and update all graphs based on user selections.
        Input: **event_args (dict) - event arguments.
        Process: Filters records, calculates totals, and updates various graphs.
        Output: None
        """
        timeChoice = self.ddDates.selected_value  # Get selected time range
        typeChoice = self.ddGroup.selected_value  # Get selected group type
        infoChoice = self.ddInfoShown.selected_value  # Get selected information type

        # Filter records based on the selected time range
        filteredRecords = self.filterRecordsByTime(self.allRecords, timeChoice)

        # Calculate and display total payout, total time worked, and total employees
        totalPayout, totalTime, totalEmployees = self.calculateTotals(filteredRecords, typeChoice)
        self.lblPayout.text = f"${totalPayout:.2f}"  # Display total payout
        self.lblTime.text = f"{totalTime:.2f}h"  # Display total time worked
        self.lblEmployees.text = str(totalEmployees)  # Display total number of employees

        typeArr = []  # Initialize array for type categories
        infoArr = []  # Initialize array for information values

        if typeChoice == "Groups":
            typeArr = ["Warehouse", "Management", "Admin", "Accounting"]
            warehouse = management = admin = accounting = 0  # Initialize counters
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
            infoArr = [warehouse, management, admin, accounting]  # Populate information array

        elif typeChoice == "Employment Type":
          typeArr = ["Full Time", "Part Time", "Contractor"]
          fullTime = 0
          partTime = 0
          contractor = 0
          for record in filteredRecords:
              recordUser = self.allUsers[record['UserID']]
              if str(recordUser['Employment']).strip() == "Part Time":
                  if infoChoice == "Payout":
                      partTime += record['Payout']
                  elif infoChoice == "Time Worked":
                      partTime += record['HoursWorked']
              elif str(recordUser['Employment']).strip() == "Full Time":
                  if infoChoice == "Payout":
                      fullTime += record['Payout']
                  elif infoChoice == "Time Worked":
                      fullTime += record['HoursWorked']
              elif str(recordUser['Employment']).strip() == "Contractor":
                  if infoChoice == "Payout":
                      contractor += record['Payout']
                  elif infoChoice == "Time Worked":
                      contractor += record['HoursWorked']
          infoArr = [fullTime, partTime, contractor]


        elif typeChoice == "Employees":
          totalAmountPerEmployee = {user['UserID']: 0 for user in self.allUsers}  # Initialize total amount per employee
          for record in filteredRecords:
              if infoChoice == "Payout":
                  totalAmountPerEmployee[record['UserID']] += float(record['Payout'])
              elif infoChoice == "Time Worked":
                  totalAmountPerEmployee[record['UserID']] += float(record['HoursWorked'])
          typeArr = [user['FullName'] for user in self.allUsers]  # List of employee names
          infoArr = [totalAmountPerEmployee[user['UserID']] for user in self.allUsers]  # Corresponding amounts


        # Set Plots

        # Update the pie chart
        self.plotPieDistribution.data = go.Pie(labels=typeArr, values=infoArr, hole=0.3)  # Create pie chart
        self.plotPieDistribution.layout.update(
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='#333333',  # Background color for the plotting area
            paper_bgcolor='#333333',  # Background color for the entire graph
            font=dict(color='white')  # Text color for better visibility against the dark background
        )

        # Update the top bar chart
        self.plotGroupStats.data = go.Bar(x=typeArr, y=infoArr)  # Create bar chart
        self.plotGroupStats.layout.update(
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='#333333',  # Background color for the plotting area
            paper_bgcolor='#333333',  # Background color for the entire graph
            font=dict(color='white')  # Text color for better visibility against the dark background
        )

        # Update the bottom graph (e.g., Date distribution)
        self.plotDateDistribution.data = self.getDateDistribution(filteredRecords, infoChoice)  # Create date distribution bar chart
        self.plotDateDistribution.layout.update(
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='#333333',  # Background color for the plotting area
            paper_bgcolor='#333333',  # Background color for the entire graph
            font=dict(color='white')  # Text color for better visibility against the dark background
        )

        # Refresh the employee info table
        self.refreshEmployeeInfoTable()  # Update the employee info table

    def refreshEmployeeInfoTable(self, **event_args):
        """
        Purpose: Refresh and update the employee information table.
        Input: **event_args (dict) - event arguments.
        Process: Accumulates data based on user selection and binds it to the table.
        Output: None
        """
        infoChoice = self.ddTableInfoShown.selected_value  # Get selected information type for the table
        employeeData = []  # Initialize employee data list

        for user in self.allUsers:
            name = user['FullName']  # Get employee's full name
            if infoChoice == "Payout":
                totalPayout = sum(record['Payout'] for record in self.allRecords if record['UserID'] == user['UserID'])
                employeeData.append({'name': name, 'info': f"${totalPayout:.2f}"})  # Append total payout
            elif infoChoice == "Time Worked":
                totalTime = sum(record['HoursWorked'] for record in self.allRecords if record['UserID'] == user['UserID'])
                employeeData.append({'name': name, 'info': f"{totalTime:.2f}h"})  # Append total time worked
            elif infoChoice == "Pay Rate":
                payRate = user['BasicRate']  # Get basic pay rate
                extendedRate = user['ExtendedRate']  # Get extended pay rate
                holidayRate = user['PublHolRate']  # Get public holiday pay rate
                employeeData.append({'name': name, 'info': f"{payRate}, {extendedRate}, {holidayRate}"})  # Append pay rates
            elif infoChoice == "User ID":
                userID = user['UserID']  # Get user ID
                employeeData.append({'name': name, 'info': str(userID)})  # Append user ID

        # Bind the data to the repeating panel
        self.rpTable.items = employeeData  # Update table items with employee data

    def filterRecordsByTime(self, records, timeChoice, **event_args):
        """
        Purpose: Filter records based on the selected time range.
        Input: records (list), timeChoice (str), **event_args (dict).
        Process: Filters the records based on the time choice selected by the user.
        Output: Filtered list of records.
        """
        # Determine the start date based on time choice
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

        end_date = datetime.now().date() + timedelta(days=1)  # Set end date as tomorrow

        return [record for record in records if start_date <= record['ClockIn'].date() < end_date]  # Filter records within the date range

    def calculateTotals(self, records, typeChoice, **event_args):
        """
        Purpose: Calculate total payout, total time worked, and total employees.
        Input: records (list), typeChoice (str), **event_args (dict).
        Process: Iterates through records to calculate the totals.
        Output: totalPayout (float), totalTime (float), totalEmployees (int).
        """
        totalPayout = 0
        totalTime = 0
        totalEmployees = set()

        for record in records:
            totalPayout += record['Payout']  # Sum up total payout
            totalTime += record['HoursWorked']  # Sum up total hours worked
            totalEmployees.add(record['UserID'])  # Add unique employees to the set

        return totalPayout, totalTime, len(totalEmployees)  # Return totals

    def getDateDistribution(self, records, infoChoice, **event_args):
        """
        Purpose: Get date distribution data for a bar chart.
        Input: records (list), infoChoice (str), **event_args (dict).
        Process: Accumulates data for each date based on information choice.
        Output: Bar chart data (plotly.graph_objects.Bar).
        """
        date_dict = {}
        for record in records:
            date_str = record['ClockIn'].strftime('%Y-%m-%d')  # Format date as string
            if date_str not in date_dict:
                date_dict[date_str] = 0  # Initialize date entry
            if infoChoice == "Payout":
                date_dict[date_str] += record['Payout']  # Add payout to the date entry
            elif infoChoice == "Time Worked":
                date_dict[date_str] += record['HoursWorked']  # Add hours worked to the date entry

        dates = list(date_dict.keys())  # Get list of dates
        values = list(date_dict.values())  # Get corresponding values

        return go.Bar(x=dates, y=values)  # Create and return bar chart

    def downloadUserDetails(self, **event_args):
        """
        Purpose: Download user details as a CSV file.
        Input: **event_args (dict).
        Process: Confirms with the user, retrieves CSV data from the server, and initiates download.
        Output: None
        """
        filter_option = confirm("Are you sure you want to download all user details? (User profile images will not be included)")
        if filter_option:
            csv_data = anvil.server.call('getUserDetailsForDownload', True)  # Get user details for download
        else:
            return  # Cancel was selected, do nothing

        # Encode the CSV data to bytes
        csv_bytes = csv_data.encode('utf-8')

        # Create a file and download it
        media = anvil.BlobMedia('text/csv', csv_bytes, name='user_details.csv')  # Create media object for CSV
        download(media)  # Initiate download

    def downloadWorkRecords(self, **event_args):
        """
        Purpose: Download work records as a CSV file.
        Input: **event_args (dict).
        Process: Confirms with the user, retrieves CSV data from the server based on selection, and initiates download.
        Output: None
        """
        try:
            filter_option = confirm("Do you want to download all data or filtered data based on the selected time period?", buttons=["All", "Filtered", "Cancel"])
            if filter_option == "All":
                csv_data = anvil.server.call('getWorkRecordsForDownloads', "All Time")  # Get all work records
            elif filter_option == "Filtered":
                time_choice = self.ddDates.selected_value  # Get selected time range
                csv_data = anvil.server.call('getWorkRecordsForDownloads', time_choice)  # Get filtered work records
            else:
                return  # Cancel was selected, do nothing

            # Encode the CSV data to bytes
            csv_bytes = csv_data.encode('utf-8')

            # Create a file and download it
            media = anvil.BlobMedia('text/csv', csv_bytes, name='work_records.csv')  # Create media object for CSV
            download(media)  # Initiate download
        except:
            alert("There isn't any data to download for the specified time period.")  # Show alert if no data available
