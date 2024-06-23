from ._anvil_designer import frmEmployeeDashboardTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class frmEmployeeDashboard(frmEmployeeDashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.users.get_user()
    self.userID = self.user['UserID']
    # Any code you write here will run before the form opens.

  def refresh(self, **event_args):
    working = anvil.server.call('getIfWorking', self.userID)
    if working:
      self.btnClockinout.text = "Clock Out"
      self.btnClockinout.background = "#ff0000"
    elif not working:
      self.btnClockinout.text = "Clock In"
      self.btnClockinout.background = "#088000"
      

  def clock(self, **event_args):
    pass

  def profile(self, **event_args):
    userID = self.userID
    open_form('frmProfile', userID)