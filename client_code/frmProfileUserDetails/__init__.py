from ._anvil_designer import frmProfileUserDetailsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Functions import Other


class frmProfileUserDetails(frmProfileUserDetailsTemplate):
  def __init__(self, employeeID, p_parent, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self._parent = p_parent
    self.employeeId = employeeID
    # Displaying all of the Employee details.
    userRow = anvil.server.call('getUserInfo', employeeID)
    self.imgProfilePicture.source = userRow['Profile']
    self.lblFullNAME.text = str(userRow['FullName'])
    self.lblWorkType.text = str(userRow['Employment'])
    self.lblGroup.text = str(userRow['Group'])
    self.lblEmail.text = str(userRow['Email'])
    self.lblPhoneNumber.text = str(userRow['PhoneNumber'])
    self.lblDoB.text = str(userRow['DoB'])
    self.lblBaseRate.text = str(userRow['BasicRate'])
    self.lblExtendedRate.text = str(userRow["ExtendedRate"])
    self.lblPublicHolidayRate.text = str(userRow["PublHolRate"])
    self.lblUserID.text = str(userRow["UserID"])
    self.lblJobTitle.text = str(userRow['Title'])
    self.lblGender.text = str(userRow['Gender'])
    self.lblTFN.text = str(userRow['TFN'])

  def editProfile(self, **event_args):
    self._parent.editUser(self.employeeId)

  def openTimesheets(self, **event_args):
    self._parent.openProfileTimesheets(self.employeeId)

