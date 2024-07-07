from ._anvil_designer import EmployeeDashboardTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class EmployeeDashboard(EmployeeDashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties.
    self.init_components(**properties)
    self.user = anvil.users.get_user()
    self.userID = self.user["UserID"]
    # Set Form Data bindings.
    allWorkRecords = anvil.server.call('getUserTimesheets', self.userID)
    try:
      self.rpApprovedWork.items = [d for d in allWorkRecords if d['Approval']]
      self.rpPendingWork.items = [d for d in allWorkRecords if not d['Approval']]
    except:
      pass
    # Any code you write here will run before the form opens.
    self.refresh()

  def refresh(self, **event_args):
    workingStatus = anvil.server.call("getIfWorking", self.userID)
    if workingStatus:
      self.btnClockinout.text = "Clock Out"
      self.btnClockinout.background = "#ff0000"
      self.btnClockinout.tag = 1
    else:
      self.btnClockinout.text = "Clock In"
      self.btnClockinout.background = "#088000"
      self.btnClockinout.tag = 0

  def clock(self, **event_args):
    if self.btnClockinout.tag == 0:
      self.btnClockinout.text = "Clock Out"
      self.btnClockinout.background = "#ff0000"
      self.btnClockinout.tag = 1
      anvil.server.call("setClock", self.userID)
    else:
      self.btnClockinout.text = "Clock In"
      self.btnClockinout.background = "#088000"
      self.btnClockinout.tag = 0
      anvil.server.call("updateClock", self.userID)
