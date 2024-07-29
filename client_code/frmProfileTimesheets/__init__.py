from ._anvil_designer import frmProfileTimesheetsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Functions import Other

class frmProfileTimesheets(frmProfileTimesheetsTemplate):
    def __init__(self, employeeID, p_parent, **properties):
        """
        Initialize the Profile Timesheets form with employee details and work records.
        """
        self.init_components(**properties)  # Set up the form properties and data bindings
        self._parent = p_parent  # Reference to the parent form
        self.employeeId = employeeID  # Store the ID of the employee
        # Fetch and display the employee's name
        userRow = anvil.server.call("getUserInfo", employeeID)
        self.lblFullNAME.text = str(userRow["FullName"])
        # Fetch and display the employee's work records
        userWorkRecords = anvil.server.call("getUserTimesheets", employeeID)
        self.rpPastWork.items = userWorkRecords  # Set the work records to the repeating panel

    def editProfile(self, **event_args):
        """
        Open the Edit User form for the current employee.
        """
        self._parent.editUser(self.employeeId)  # Call the parent's editUser method with the current employee's ID

    def openUserDetails(self, **event_args):
        """
        Open the Profile User Details form for the current employee.
        """
        self._parent.openProfileUserDetails(self.employeeId)  # Call the parent's openProfileUserDetails method with the current employee's ID
