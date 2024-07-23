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
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self._parent = p_parent
    self.employeeId = employeeID
    userSettings = anvil.server.call('getUserSettings', self.userID)
    Other.apply_mode(userSettings['DarkMode'], self)  # Apply mode using helper function
    # Displaying the Employee name.
    userRow = anvil.server.call("getUserInfo", employeeID)
    self.lblFullNAME.text = str(userRow["FullName"])
    # Displaying the employee's work records.
    userWorkRecords = anvil.server.call("getUserTimesheets", employeeID)
    self.rpPastWork.items = userWorkRecords

  def editProfile(self, **event_args):
    self._parent.editUser(self.employeeId)

  def openUserDetails(self, **event_args):
    self._parent.openProfileUserDetails(self.employeeId)
