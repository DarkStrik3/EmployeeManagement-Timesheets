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
        Initialize the Manager Dashboard form and set up user details.
        """
        self.init_components(**properties)  # Set up the form properties and data bindings

        # Get the current logged-in user
        self.user = anvil.users.get_user()
        self.userID = self.user['UserID']
        
        # Fetch user details from the server
        self.userDetails = anvil.server.call('getUserInfo', self.userID)
        
        # Set user details in the form
        self.lblProfileName.text = self.userDetails['FullName']
        self.imgProfile.source = self.userDetails['Profile']
        
        # Load the Employee Management component by default
        self.selectEmployeeManagement()

    def signOut(self, **event_args):
        """
        Log out the user and open the login form.
        """
        anvil.users.logout()  # Log out the current user
        open_form('frmLogin')  # Redirect to the login form

    def selectEmployeeManagement(self, **event_args):
        """
        Display the Employee Management component and update button backgrounds.
        """
        self.cpDashboards.clear()  # Clear current content in the dashboard panel
        self.cpDashboards.add_component(EmployeeManagement(p_parent=self), full_width_row=True)  # Add Employee Management component
        # Update button backgrounds to indicate selection
        self.btnEmplManage.background = "#8f8f8f"
        self.btnAnalyticReport.background = "#333333"
        self.btnTimesheets.background = "#333333"
        self.btnSettings.background = "#333333"

    def selectAnalyticsReport(self, **event_args):
        """
        Display the Analytics Reporting component and update button backgrounds.
        """
        self.cpDashboards.clear()  # Clear current content in the dashboard panel
        self.cpDashboards.add_component(AnalyticsReporting(), full_width_row=True)  # Add Analytics Reporting component
        # Update button backgrounds to indicate selection
        self.btnEmplManage.background = "#333333"
        self.btnAnalyticReport.background = "#8f8f8f"
        self.btnTimesheets.background = "#333333"
        self.btnSettings.background = "#333333"

    def selectTimesheets(self, **event_args):
        """
        Display the Timesheets component and update button backgrounds.
        """
        self.cpDashboards.clear()  # Clear current content in the dashboard panel
        self.cpDashboards.add_component(Timesheets(), full_width_row=True)  # Add Timesheets component
        # Update button backgrounds to indicate selection
        self.btnEmplManage.background = "#333333"
        self.btnAnalyticReport.background = "#333333"
        self.btnTimesheets.background = "#8f8f8f"
        self.btnSettings.background = "#333333"

    def selectSettings(self, **event_args):
        """
        Display the Settings component and update button backgrounds.
        """
        self.cpDashboards.clear()  # Clear current content in the dashboard panel
        self.cpDashboards.add_component(Settings(), full_width_row=True)  # Add Settings component
        # Update button backgrounds to indicate selection
        self.btnEmplManage.background = "#333333"
        self.btnAnalyticReport.background = "#333333"
        self.btnTimesheets.background = "#333333"
        self.btnSettings.background = "#8f8f8f"

    def selectAddNewUser(self, **event_args):
        """
        Display the Add User component and update button backgrounds.
        """
        self.cpDashboards.clear()  # Clear current content in the dashboard panel
        self.cpDashboards.add_component(AddUser(), full_width_row=True)  # Add Add User component
        # Update button backgrounds to indicate selection
        self.btnEmplManage.background = "#333333"
        self.btnAnalyticReport.background = "#333333"
        self.btnTimesheets.background = "#333333"
        self.btnSettings.background = "#333333"

    def openOwnProfileUserDetails(self, **event_args):
        """
        Open the current user's profile details.
        """
        self.openProfileUserDetails(self.userID)  # Open profile details for the current user

    def openProfileUserDetails(self, userID, **event_args):
        """
        Open the profile details of a specified user.
        """
        self.cpDashboards.clear()  # Clear current content in the dashboard panel
        self.cpDashboards.add_component(frmProfileUserDetails(employeeID=userID, p_parent=self), full_width_row=True)  # Add Profile User Details component

    def openProfileTimesheets(self, userID, **event_args):
        """
        Open the timesheets for a specified user.
        """
        self.cpDashboards.clear()  # Clear current content in the dashboard panel
        self.cpDashboards.add_component(frmProfileTimesheets(employeeID=userID, p_parent=self), full_width_row=True)  # Add Profile Timesheets component

    def editUser(self, userID, **event_args):
        """
        Open the Edit User component for a specified user.
        """
        self.cpDashboards.clear()  # Clear current content in the dashboard panel
        self.cpDashboards.add_component(EditUser(employeeID=userID, p_parent=self), full_width_row=True)  # Add Edit User component
