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
        payout = anvil.server.call('getTotalBalance', self.userID)
        approvedPayout = anvil.server.call('getTotalApprovedBalance', self.userID)
        self.lblBalance.text = f"Balance: ${payout:.2f}"  # Display balance with 2 decimal places
        self.lblApprovedBalance.text = f"Approved Balance: ${approvedPayout:.2f}"
        
        # Update clock in/out button based on working status
        if workingStatus:
            # User is clocked in, and is clocking out
            self.btnClockinout.text = "Clock Out"
            self.btnClockinout.background = "#ff0000"
            self.btnClockinout.tag = 1
            self.workTimer.interval = 0
            self.lblTimer.text = "00:00:00"
            
        else:
            # User was clocked out, and is clocking in
            self.btnClockinout.text = "Clock In"
            self.btnClockinout.background = "#088000"
            self.btnClockinout.tag = 0
            clockOutTime = datetime.now().replace(tzinfo=None)
            totalWork = clockOutTime - row['ClockIn'].replace(tzinfo=None)
            totalSeconds = totalWork.total_seconds()  # convert total work time to seconds
            hours = int(totalSeconds // 3600)
            minutes = int((totalSeconds % 3600) // 60)
            seconds = int((totalSeconds % 3600) % 60)
            self.lblTimer.tag = totalSeconds
            self.lblTimer.text = f"{hours:.0f}:{minutes:.0f}:{seconds:.0f}"
            
        try:
            # Clear existing items
            self.rpApprovedWork.items = []
            self.rpPendingWork.items = []
            
            # Assign new items
            self.rpApprovedWork.items = [d for d in allWorkRecords if d['Approval']][:4]
            self.rpPendingWork.items = [d for d in allWorkRecords if not d['Approval']][:4]
            
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


    def timerTick(self, **event_args):
      if self.btnClockinout.tag == 1:
        previousTime = self.lblTimer.tag
        newTime = previousTime + 1
        self.lblTimer.tag = newTime
        hours = int(newTime // 3600)
        minutes = int((newTime % 3600) // 60)
        seconds = int((newTime % 3600) % 60)
        self.lblTimer.text = f"{hours:.0f}:{minutes:.0f}:{seconds:.0f}"
