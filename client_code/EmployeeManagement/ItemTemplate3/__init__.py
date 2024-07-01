from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate3(ItemTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.lblEmplName.text = self.item["FullName"]
    self.lblEmplID.text = self.item["UserID"]
    self.imgProfileImage.source = self.item["Profile"]
    self.lblEmplEmployment.text = self.item["EmploymentType"]