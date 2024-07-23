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
    self.btnEmplManage.background = "#6e6e6e"
    self.btnAnalyticReport.background = ""
    self.btnTimesheets.background = ""
    self.btnSettings.background = ""

  def selectAnalyticsReport(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(AnalyticsReporting(), full_width_row=True)
    self.btnEmplManage.background = ""
    self.btnAnalyticReport.background = "#6e6e6e"
    self.btnTimesheets.background = ""
    self.btnSettings.background = ""

  def selectTimesheets(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(Timesheets(), full_width_row=True)
    self.btnEmplManage.background = ""
    self.btnAnalyticReport.background = ""
    self.btnTimesheets.background = "#6e6e6e"
    self.btnSettings.background = ""

  def selectSettings(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(Settings(), full_width_row=True)
    self.btnEmplManage.background = ""
    self.btnAnalyticReport.background = ""
    self.btnTimesheets.background = ""
    self.btnSettings.background = "#6e6e6e"

  def selectAddNewUser(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(AddUser(), full_width_row=True)
    self.btnEmplManage.background = ""
    self.btnAnalyticReport.background = ""
    self.btnTimesheets.background = ""
    self.btnSettings.background = ""

  def openProfileUserDetails(self, userID, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(frmProfileUserDetails(employeeID=userID, p_parent=self), full_width_row=True)

  def openProfileTimesheets(self, userID, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(frmProfileTimesheets(employeeID=userID, p_parent=self), full_width_row=True)
  
  def editUser(self, userID, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(EditUser(employeeID=userID, p_parent=self), full_width_row=True)
