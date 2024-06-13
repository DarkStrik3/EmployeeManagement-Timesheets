from ._anvil_designer import frmAddUserTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class frmAddUser(frmAddUserTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.userID = properties["userID"]
    # Any code you write here will run before the form opens.

  def Proceed(self, **event_args):
    userIdentification = anvil.server.call("getUserID", self.txtUsername.text)
    open_form("frmEmployeeDashboard", userIdentification)
