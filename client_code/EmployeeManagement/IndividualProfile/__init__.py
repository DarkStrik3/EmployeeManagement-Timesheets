from ._anvil_designer import IndividualProfileTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class IndividualProfile(IndividualProfileTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self._parent = self.item['parent']
        self.user = anvil.server.call("getUser", self.item['employee']["UserID"])
        # Any code you write here will run before the form opens.
        self.lblEmplName.text = self.item['employee']["FullName"]
        self.lblEmplID.text = self.item['employee']["UserID"]
        self.imgProfileImage.source = self.item['employee']["Profile"]
        self.lblEmplEmployment.text = self.item['employee']["Employment"]
        if not self.user['enabled']:
          self.btnArchiveProfile.text = "Unarchive"

          
    def editUser(self, **event_args):
      self._parent.editUserDetails(self.item['employee']["UserID"])

    def openUser(self, **event_args):
      self._parent.openProfileUserDetails(self.item['employee']["UserID"])

    def archiveUser(self, **event_args):
      if self.user['enabled']:
        if confirm("Are you sure you want to archive " + self.item['employee']["FullName"] + "'s account?"):
          anvil.server.call("archiveUser", self.item['employee']["UserID"], True, None)
          # refreshes the entire repeating panel
          self._parent.sortFilteredEmployees()
      elif not self.user['enabled']:
        if confirm("Are you sure you want to unarchive " + self.item['employee']["FullName"] + "'s account?"):
          employmentType = confirm("How are they employed?", buttons=["Full Time", "Part Time", "Contractor"])
          if employmentType:
            anvil.server.call("archiveUser", self.item['employee']["UserID"], False, employmentType)
            # refreshes the entire repeating panel
            self._parent.sortFilteredEmployees()
