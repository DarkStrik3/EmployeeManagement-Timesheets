from ._anvil_designer import frmManagerDashboardTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..EmployeeManagement import EmployeeManagement
from ..AnalyticsReporting import AnalyticsReporting
from ..Settings import Settings
from ..Timesheets import Timesheets
from ..AddUser import AddUser
from ..EditUser import EditUser
from ..frmProfileTimesheets import frmProfileTimesheets
from ..frmProfileUserDetails import frmProfileUserDetails
from ..Functions import Other


class frmManagerDashboard(frmManagerDashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()
    self.userID = self.user['UserID']
    self.userDetails = anvil.server.call('getUserInfo', self.userID)
    self.lblProfileName.text = self.userDetails['FullName']
    self.imgProfile.source = self.userDetails['Profile']
    self.selectEmployeeManagement()
    

  def signOut(self, **event_args):
    anvil.users.logout()
    open_form('frmLogin')

  def selectEmployeeManagement(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(EmployeeManagement(p_parent=self), full_width_row=True)
    self.btnEmplManage.background = "#8f8f8f"
    self.btnAnalyticReport.background = "#333333"
    self.btnTimesheets.background = "#333333"
    self.btnSettings.background = "#333333"

  def selectAnalyticsReport(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(AnalyticsReporting(), full_width_row=True)
    self.btnEmplManage.background = "#333333"
    self.btnAnalyticReport.background = "#8f8f8f"
    self.btnTimesheets.background = "#333333"
    self.btnSettings.background = "#333333"

  def selectTimesheets(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(Timesheets(), full_width_row=True)
    self.btnEmplManage.background = "#333333"
    self.btnAnalyticReport.background = "#333333"
    self.btnTimesheets.background = "#8f8f8f"
    self.btnSettings.background = "#333333"

  def selectSettings(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(Settings(), full_width_row=True)
    self.btnEmplManage.background = "#333333"
    self.btnAnalyticReport.background = "#333333"
    self.btnTimesheets.background = "#333333"
    self.btnSettings.background = "#8f8f8f"

  def selectAddNewUser(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(AddUser(), full_width_row=True)
    self.btnEmplManage.background = "#333333"
    self.btnAnalyticReport.background = "#333333"
    self.btnTimesheets.background = "#333333"
    self.btnSettings.background = "#333333"

  # Open your own profile
  def openOwnProfileUserDetails(self, **event_args):
    self.openProfileUserDetails(self.userID)

  # Open an employee profile
  def openProfileUserDetails(self, userID, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(frmProfileUserDetails(employeeID=userID, p_parent=self), full_width_row=True)

  # Still inside the User Profile, check their timesheets.
  def openProfileTimesheets(self, userID, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(frmProfileTimesheets(employeeID=userID, p_parent=self), full_width_row=True)

  # Open the edit user page.
  def editUser(self, userID, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(EditUser(employeeID=userID, p_parent=self), full_width_row=True)
