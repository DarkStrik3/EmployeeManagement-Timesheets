from ._anvil_designer import frmProfileTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class frmProfile(frmProfileTemplate):
  def __init__(self, employeeID, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Setting all parts that are only required for the employee view to be invisible.
    self.imgHeader.visible = False
    self.btnMenu.visible = False
    self.imgProfile.visible = False
    self.lblProfileName.visible = False
    self.btnBack.visible = False

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

    # Displaying the employee's work records.
    userWorkRecords = anvil.server.call('getUserTimesheets', employeeID)
    self.rpPastWork.items = userWorkRecords


    
