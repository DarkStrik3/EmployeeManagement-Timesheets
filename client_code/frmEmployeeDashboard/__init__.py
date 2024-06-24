from ._anvil_designer import frmEmployeeDashboardTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class frmEmployeeDashboard(frmEmployeeDashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties.
    self.init_components(**properties)
    self.user = anvil.users.get_user()
    self.userID = self.user['UserID']

    # Set Form Data bindings.
    self.rpLeft.items = anvil.server.call("getUserTimesheets", self.userID, True)
    self.rpRight.items = anvil.server.call("getUserTimesheets", self.userID, False)
    # Any code you write here will run before the form opens.
    self.refresh()

  
  def refresh(self, **event_args):
    workingStatus = anvil.server.call('getIfWorking', self.userID)
    if workingStatus:
      self.btnClockinout.text = "Clock Out"
      self.btnClockinout.background = "#ff0000"
      self.btnClockinout.tag = 1
    elif not workingStatus:
      self.btnClockinout.text = "Clock In"
      self.btnClockinout.background = "#088000"
      self.btnClockinout.tag = 0
      
      

  def clock(self, **event_args):
    anvil.server.call('setClock', self.userID)
    self.refresh()

  def profile(self, **event_args):
    userID = self.userID
    open_form('frmProfile', userID)