from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate3(ItemTemplate3Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        self._parent = self.item['parent']
        # Any code you write here will run before the form opens.
        self.lblEmplName.text = self.item['employee']["FullName"]
        self.lblEmplID.text = self.item['employee']["UserID"]
        self.imgProfileImage.source = self.item['employee']["Profile"]
        self.lblEmplEmployment.text = self.item['employee']["Employment"]

    def editUser(self, **event_args):
      self._parent.editUserDetails(self.item['employee']["UserID"])

    def openUser(self, **event_args):
      self._parent.openProfile(self.item['employee']["UserID"])

    def archiveUser(self, **event_args):
      if confirm("Are you sure you want to archive " + self.item['employee']["FullName"] + "'s account?"):
        self._parent.archiveUser(self.item['employee']["UserID"])
