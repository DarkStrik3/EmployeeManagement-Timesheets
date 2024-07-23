from ._anvil_designer import frmEmployeeDashboardTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..EmployeeDashboard import EmployeeDashboard
from ..frmProfileUserDetails import frmProfileUserDetails
from ..frmProfileTimesheets import frmProfileTimesheets
from ..Settings import Settings
from ..Functions import Other

class frmEmployeeDashboard(frmEmployeeDashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties.
    self.init_components(**properties)
    self.user = anvil.users.get_user()
    self.userID = self.user['UserID']
    # Any code you write here will run before the form opens.
    userRow = anvil.server.call('getUserInfo', self.userID)
    self.lblProfileName.text = userRow['FullName']
    self.imgProfile.source = userRow['Profile']
    self.openEmployeeDashboard()


  def openEmployeeDashboard(self, **event_args):
    self.cpEmployeeDashboard.clear()
    self.cpEmployeeDashboard.add_component(EmployeeDashboard())


  def openProfileUserDetails(self, employeeID, **event_args):
    self.cpEmployeeDashboard.clear()
    self.cpEmployeeDashboard.add_component(frmProfileUserDetails(self.userID, self))

  def openProfileTimesheets(self, employeeID, **event_args):
    self.cpEmployeeDashboard.clear()
    self.cpEmployeeDashboard.add_component(frmProfileTimesheets(self.userID, self))

  def openSettings(self, **event_args):
    self.cpEmployeeDashboard.clear()
    self.cpEmployeeDashboard.add_component(Settings())

  def signOut(self, **event_args):
    anvil.users.logout()
    open_form('frmLogin')

  def menu(self, **Event_args):
    choice = confirm(title="Pages:\n", buttons=[("Dashboard", 1), ("Profile", 2), ("Settings", 3)], dismissible=True)
    if choice == 1:
      self.openEmployeeDashboard()
    elif choice == 2:
      self.openProfileUserDetails(self.userID)
    elif choice == 3:
      self.openSettings()
      