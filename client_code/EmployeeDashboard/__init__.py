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
          # User is clocked in
          self.btnClockinout.text = "Clock Out"
          self.btnClockinout.background = "#ff0000"
          self.btnClockinout.tag = 1
          row = anvil.server.call("getClockedInRow", self.userID)
          elapsed_time = datetime.now().replace(tzinfo=None) - row['ClockIn'].replace(tzinfo=None)
          self.update_timer(elapsed_time.total_seconds())
          self.workTimer.interval = 1
      else:
          # User is clocked out
          self.btnClockinout.text = "Clock In"
          self.btnClockinout.background = "#088000"
          self.btnClockinout.tag = 0
          self.workTimer.interval = 0
          self.lblTimer.text = "00:00:00"
          self.lblTimer.tag = 0

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
        self.workTimer.interval = 1
      else:
          self.btnClockinout.text = "Clock In"
          self.btnClockinout.background = "#088000"
          self.btnClockinout.tag = 0
          anvil.server.call("updateClock", self.userID)
          self.workTimer.interval = 0
          self.lblTimer.text = "00:00:00"
          self.lblTimer.tag = 0
        
      # Refresh the panel after clocking in/out
      self.refresh()


    def timerTick(self, **event_args):
        if self.btnClockinout.tag == 1:
            previousTime = self.lblTimer.tag
            newTime = previousTime + 1
            self.update_timer(newTime)

    def update_timer(self, total_seconds):
        self.lblTimer.tag = total_seconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int((total_seconds % 3600) % 60)
        self.lblTimer.text = f"{hours:02}:{minutes:02}:{seconds:02}"