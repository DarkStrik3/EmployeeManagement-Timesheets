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
        """
        Initialize the frmProfileUserDetails form with the provided employee ID and parent form.
        """
        self.init_components(**properties)  # Set up the form properties and data bindings
        self._parent = p_parent  # Store reference to the parent form
        self.employeeId = employeeID  # Store the employee ID

        # Retrieve and display the employee's details
        userRow = anvil.server.call('getUserInfo', employeeID)
        self.imgProfilePicture.source = userRow['Profile']  # Display the profile picture
        self.lblFullNAME.text = str(userRow['FullName'])  # Display the full name
        self.lblWorkType.text = str(userRow['Employment'])  # Display the type of employment
        self.lblGroup.text = str(userRow['Group'])  # Display the group
        self.lblEmail.text = str(userRow['Email'])  # Display the email address
        self.lblPhoneNumber.text = str(userRow['PhoneNumber'])  # Display the phone number
        self.lblDoB.text = str(userRow['DoB'])  # Display the date of birth
        self.lblBaseRate.text = str(userRow['BasicRate'])  # Display the basic rate of pay
        self.lblExtendedRate.text = str(userRow["ExtendedRate"])  # Display the extended rate of pay
        self.lblPublicHolidayRate.text = str(userRow["PublHolRate"])  # Display the public holiday rate of pay
        self.lblUserID.text = str(userRow["UserID"])  # Display the user ID
        self.lblJobTitle.text = str(userRow['Title'])  # Display the job title
        self.lblGender.text = str(userRow['Gender'])  # Display the gender
        self.lblTFN.text = str(userRow['TFN'])  # Display the tax file number (TFN)

    def editProfile(self, **event_args):
        """
        Call the parent form's method to edit the user profile.
        """
        self._parent.editUser(self.employeeId)

    def openTimesheets(self, **event_args):
        """
        Call the parent form's method to open the user's timesheets.
        """
        self._parent.openProfileTimesheets(self.employeeId)
