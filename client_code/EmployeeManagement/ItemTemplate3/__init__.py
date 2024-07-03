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
        self._parent = get_open_form()
        # Any code you write here will run before the form opens.
        self.lblEmplName.text = self.item["FullName"]
        self.lblEmplID.text = self.item["UserID"]
        self.imgProfileImage.source = self.item["Profile"]
        self.lblEmplEmployment.text = self.item["Employment"]

    def editUser(self, **event_args):
      self.raise_event('x-edit-user', user_id=self.item["UserID"])
  
    def openUser(self, **event_args):
        self.raise_event('x-open-user', user_id=self.item["UserID"])

    def archiveUser(self, **event_args):
      if confirm("Are you sure you want to archive " + self.item["FullName"] + "'s account?"):
        anvil.server.call("archiveUser", self.item["UserID"])
        self.raise_event('x-refresh')
