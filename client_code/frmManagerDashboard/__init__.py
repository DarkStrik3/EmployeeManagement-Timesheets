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
      """
      Initialize the Manager Dashboard form with user details and default view.
      """
      self.init_components(**properties)  # Set up form components and data bindings
      self.user = anvil.users.get_user()  # Get the currently logged-in user
      self.userID = self.user['UserID']  # Store the user ID
      self.userDetails = anvil.server.call('getUserInfo', self.userID)  # Fetch user information
      self.lblProfileName.text = self.userDetails['FullName']  # Display user's full name
      self.imgProfile.source = self.userDetails['Profile']  # Display user's profile picture
      self.selectEmployeeManagement()  # Load the Employee Management view by default

    def disableInput(self, **event_args):
      self.btnAnalyticReport.enabled = False
      self.btnEmplManage.enabled = False
      self.btnTimesheets.enabled = False
      self.btnSettings.enabled = False

    def enableInput(self, **event_args):
      self.btnAnalyticReport.enabled = True
      self.btnEmplManage.enabled = True
      self.btnTimesheets.enabled = True
      self.btnSettings.enabled = True
  
    def signOut(self, **event_args):
      """
      Log out the user and open the login form.
      """
      anvil.users.logout()
      open_form('frmLogin')

    def selectEmployeeManagement(self, **event_args):
      """
      Load the Employee Management component into the view.
      """
      self.disableInput() # Disable button spam/abuse
      self.cpDashboards.clear()
      self.spacermanagerHome.height = 0
      self.cpDashboards.add_component(EmployeeManagement(p_parent=self), full_width_row=True)
      self.btnEmplManage.background = "#8f8f8f"
      self.btnAnalyticReport.background = "#333333"
      self.btnTimesheets.background = "#333333"
      self.btnSettings.background = "#333333"
      self.enableInput() # Re-enable button input

    def selectAnalyticsReport(self, **event_args):
      """
      Load the Analytics Reporting component into the view.
      """
      self.disableInput() # Disable button spam/abuse
      self.cpDashboards.clear()
      self.spacermanagerHome.height = 0
      self.cpDashboards.add_component(AnalyticsReporting(), full_width_row=True)
      self.btnEmplManage.background = "#333333"
      self.btnAnalyticReport.background = "#8f8f8f"
      self.btnTimesheets.background = "#333333"
      self.btnSettings.background = "#333333"
      self.enableInput() # Re-enable button input

    def selectTimesheets(self, **event_args):
      """
      Load the Timesheets component into the view.
      """
      self.disableInput() # Disable button spam/abuse
      self.cpDashboards.clear()
      self.spacermanagerHome.height = 0
      self.cpDashboards.add_component(Timesheets(), full_width_row=True)
      self.btnEmplManage.background = "#333333"
      self.btnAnalyticReport.background = "#333333"
      self.btnTimesheets.background = "#8f8f8f"
      self.btnSettings.background = "#333333"
      self.enableInput() # Re-enable button input

    def selectSettings(self, **event_args):
      """
      Load the Settings component into the view.
      """
      self.disableInput() # Disable button spam/abuse
      self.cpDashboards.clear()
      self.spacermanagerHome.height = 515
      self.cpDashboards.add_component(Settings(), full_width_row=True)
      self.btnEmplManage.background = "#333333"
      self.btnAnalyticReport.background = "#333333"
      self.btnTimesheets.background = "#333333"
      self.btnSettings.background = "#8f8f8f"
      self.enableInput() # Re-enable button input

    def selectAddNewUser(self, **event_args):
      """
      Load the Add User component into the view.
      """
      self.cpDashboards.clear()
      self.spacermanagerHome.height = 330
      self.cpDashboards.add_component(AddUser(), full_width_row=True)
      self.btnEmplManage.background = "#333333"
      self.btnAnalyticReport.background = "#333333"
      self.btnTimesheets.background = "#333333"
      self.btnSettings.background = "#333333"

    def openOwnProfileUserDetails(self, **event_args):
      """
      Open the current user's profile details.
      """
      self.openProfileUserDetails(self.userID)

    def openProfileUserDetails(self, userID, **event_args):
      """
      Load the profile details of the specified user into the view.
      """
      self.cpDashboards.clear()
      self.spacermanagerHome.height = 330
      self.cpDashboards.add_component(frmProfileUserDetails(employeeID=userID, p_parent=self), full_width_row=True)

    def openProfileTimesheets(self, userID, **event_args):
      """
      Load the timesheets for the specified user into the view.
      """
      self.cpDashboards.clear()
      self.spacermanagerHome.height = 330
      self.cpDashboards.add_component(frmProfileTimesheets(employeeID=userID, p_parent=self), full_width_row=True)

    def editUser(self, userID, **event_args):
      """
      Load the Edit User component for the specified user into the view.
      """
      self.cpDashboards.clear()
      self.spacermanagerHome.height = 330
      self.cpDashboards.add_component(EditUser(userID, self, True), full_width_row=True)
