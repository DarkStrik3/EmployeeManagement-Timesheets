from ._anvil_designer import IndividualProfileTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class IndividualProfile(IndividualProfileTemplate):
    def __init__(self, **properties):
        """
        Purpose: Initialize the IndividualProfile form with default properties.
        Input: 
            **properties (dict) - Additional properties.
        Process: Sets form components, initializes user data, and updates UI elements with user details.
        Output: None
        """
        self.init_components(**properties)
        self._parent = self.item['parent']
        self.user = anvil.server.call("getUser", self.item['employee']["UserID"])
        
        self.lblEmplName.text = self.item['employee']["FullName"]
        self.lblEmplID.text = self.item['employee']["UserID"]
        self.imgProfileImage.source = self.item['employee']["Profile"]
        self.lblEmplEmployment.text = self.item['employee']["Employment"]
        
        if not self.user['enabled']: # If the user is archived
          self.btnArchiveProfile.text = "Unarchive"
          self.lblEmplEmployment.text = "Not In Employment"
          self.lblEmplEmployment.foreground = "#aa6041"
          self.lblEmplID.foreground = "#aa6041"
          self.lblEmplName.foreground = "#aa6041"
          self.lblEmployeeIdentification.foreground = "#aa6041"
          self.lblEmploymentStat.foreground = "#aa6041"
          self.lblName.foreground = "#aa6041"

    def editUser(self, **event_args):
        """
        Purpose: Trigger the editing of user details for the selected employee.
        Input: **event_args (dict) - Additional event arguments.
        Process: Calls the parent form's editUserDetails method.
        Output: None
        """
        self._parent.editUserDetails(self.item['employee']["UserID"])

    def openUser(self, **event_args):
        """
        Purpose: Open the user details profile for the selected employee.
        Input: **event_args (dict) - Additional event arguments.
        Process: Calls the parent form's openProfileUserDetails method.
        Output: None
        """
        self._parent.openProfileUserDetails(self.item['employee']["UserID"])

    def archiveUser(self, **event_args):
        """
        Purpose: Archive or unarchive the user account based on its current state.
        Input: **event_args (dict) - Additional event arguments.
        Process: 
            - Asks for confirmation to archive/unarchive the user.
            - Calls the server to update the archive status.
            - Refreshes the parent form's employee list.
        Output: None
        """
        if self.user['enabled']:
            if confirm("Are you sure you want to archive " + self.item['employee']["FullName"] + "'s account?"):
                anvil.server.call("archiveUser", self.item['employee']["UserID"], True, None)
                self._parent.sortFilteredEmployees()  # Refreshes the entire repeating panel
        else:
            if confirm("Are you sure you want to unarchive " + self.item['employee']["FullName"] + "'s account?"):
                employmentType = confirm("How are they employed?", buttons=["Full Time", "Part Time", "Contractor"])
                if employmentType:
                    anvil.server.call("archiveUser", self.item['employee']["UserID"], False, employmentType)
                    self._parent.sortFilteredEmployees()  # Refreshes the entire repeating panel
