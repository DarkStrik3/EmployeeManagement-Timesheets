from ._anvil_designer import EmployeeDashboardTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta, timezone
import WorkRecordTemplateEmployee
from ..Functions import Other

class EmployeeDashboard(EmployeeDashboardTemplate):
    def __init__(self, **properties):
        """
        Purpose: Initialize the EmployeeDashboard form with default properties.
        Input: **properties (dict) - additional properties.
        Process: Sets form components and initializes user data.
        Output: None
        """
        self.init_components(**properties)
        self.user = anvil.users.get_user()
        self.userID = self.user["UserID"]
        self.refresh()

    def refresh(self, **event_args):
        """
        Purpose: Refresh the dashboard with the latest data.
        Input: **event_args (dict) - event arguments.
        Process: Updates working status, work records, and balance.
        Output: None
        """
        workingStatus = anvil.server.call("getIfWorking", self.userID)
        allWorkRecords = anvil.server.call('getUserTimesheets', self.userID)
        payout = anvil.server.call('getTotalBalance', self.userID)
        approvedPayout = anvil.server.call('getTotalApprovedBalance', self.userID)
        self.lblBalance.text = f"Balance: ${payout:.2f}"  # Display balance with 2 decimal places
        self.lblApprovedBalance.text = f"Approved Balance: ${approvedPayout:.2f}"

        # Update clock in/out button based on working status
        if workingStatus:
            self.btnClockinout.text = "Clock Out"
            self.btnClockinout.background = "#aa6041"
            self.btnClockinout.tag = 1
            row = anvil.server.call("getClockedInRow", self.userID)
            clockInTime = (row['ClockIn']).replace(tzinfo=timezone.utc)
            currentTime = datetime.utcnow().replace(tzinfo=timezone.utc)
            elapsedTime = currentTime - clockInTime          
            self.update_timer(elapsedTime.total_seconds())
            self.workTimer.interval = 1
        else:
            self.btnClockinout.text = "Clock In"
            self.btnClockinout.background = "#3e8a38"
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
        """
        Purpose: Handle clock in and clock out actions.
        Input: **event_args (dict) - event arguments.
        Process: Toggles clock in/out status and updates the server.
        Output: None
        """
        self.btnClockinout.enabled = False
        if self.btnClockinout.tag == 0:
            self.btnClockinout.text = "Clock Out"
            self.btnClockinout.background = "#aa6041"
            self.btnClockinout.tag = 1
            anvil.server.call("setClock", self.userID)
            self.lblTimer.tag = 0
            self.workTimer.interval = 1
            self.btnClockinout.enabled = True
        else:
            self.btnClockinout.text = "Clock In"
            self.btnClockinout.background = "#3e8a38"
            self.btnClockinout.tag = 0
            anvil.server.call("updateClock", self.userID)
            self.workTimer.interval = 0
            alert("Final Work time " + self.lblTimer.text + ". \n\n*Note: This was calculated locally. The final work time will not be exactly the same.")
            self.lblTimer.text = "00:00:00"
            self.lblTimer.tag = 0
            self.btnClockinout.enabled = True

        # Refresh the panel after clocking in/out
        self.refresh()

    def timerTick(self, **event_args):
        """
        Purpose: Update the work timer every tick.
        Input: **event_args (dict) - event arguments.
        Process: Increments the timer if the user is clocked in.
        Output: None
        """
        if self.btnClockinout.tag == 1:
            previousTime = self.lblTimer.tag
            newTime = previousTime + 1
            self.update_timer(newTime)

    def update_timer(self, total_seconds):
        """
        Purpose: Update the timer label with the elapsed time.
        Input: total_seconds (int) - total elapsed seconds.
        Process: Converts seconds to hours, minutes, and seconds and updates the label.
        Output: None
        """
        self.lblTimer.tag = total_seconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int((total_seconds % 3600) % 60)
        self.lblTimer.text = f"{hours:02}:{minutes:02}:{seconds:02}"
