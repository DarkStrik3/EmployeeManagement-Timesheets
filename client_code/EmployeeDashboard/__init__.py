from ._anvil_designer import EmployeeDashboardTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, date, timedelta


class EmployeeDashboard(EmployeeDashboardTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.user = anvil.users.get_user()
        self.userID = self.user["UserID"]
        self.refresh()

    def refresh(self, **event_args):
        workingStatus = anvil.server.call("getIfWorking", self.userID)
        allWorkRecords = anvil.server.call('getUserTimesheets', self.userID)
        
        # Update clock in/out button based on working status
        if workingStatus:
            self.btnClockinout.text = "Clock Out"
            self.btnClockinout.background = "#ff0000"
            self.btnClockinout.tag = 1
        else:
            self.btnClockinout.text = "Clock In"
            self.btnClockinout.background = "#088000"
            self.btnClockinout.tag = 0
        
        try:
            # Clear existing items
            self.rpApprovedWork.items = []
            self.rpPendingWork.items = []
            
            # Assign new items
            self.rpApprovedWork.items = [d for d in allWorkRecords if d['Approval']][-4:]
            self.rpPendingWork.items = [d for d in allWorkRecords if not d['Approval']][-4:]
            
            # Refresh data bindings to ensure everything is up to date
            self.refresh_data_bindings()
            
        except Exception as e:
            print(e)

    def clock(self, **event_args):
        if self.btnClockinout.tag == 0:
            self.btnClockinout.text = "Clock Out"
            self.btnClockinout.background = "#ff0000"
            self.btnClockinout.tag = 1
            anvil.server.call("setClock", self.userID)
        else:
            self.btnClockinout.text = "Clock In"
            self.btnClockinout.background = "#088000"
            self.btnClockinout.tag = 0
            anvil.server.call("updateClock", self.userID)
        
        # Refresh the panel after clocking in/out
        self.refresh()
