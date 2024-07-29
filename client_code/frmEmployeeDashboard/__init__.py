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
        """
        Initialize the Employee Dashboard form and set up the user profile.
        """
        self.init_components(**properties)
        self.user = anvil.users.get_user()  # Get the currently logged-in user
        self.userID = self.user['UserID']  # Store the user ID

        # Fetch user information from the server and set up the profile display
        userRow = anvil.server.call('getUserInfo', self.userID)
        self.lblProfileName.text = userRow['FullName']  # Set the profile name
        self.imgProfile.source = userRow['Profile']  # Set the profile image
        self.openEmployeeDashboard()  # Load the default employee dashboard component

    def openEmployeeDashboard(self, **event_args):
        """
        Load the Employee Dashboard component into the container.
        """
        self.cpEmployeeDashboard.clear()  # Clear the container
        self.cpEmployeeDashboard.add_component(EmployeeDashboard())  # Add the Employee Dashboard component

    def openProfileUserDetails(self, employeeID, **event_args):
        """
        Load the User Details profile component into the container.
        """
        self.cpEmployeeDashboard.clear()  # Clear the container
        self.cpEmployeeDashboard.add_component(frmProfileUserDetails(self.userID, self))  # Add the User Details component

    def openProfileTimesheets(self, employeeID, **event_args):
        """
        Load the Timesheets profile component into the container.
        """
        self.cpEmployeeDashboard.clear()  # Clear the container
        self.cpEmployeeDashboard.add_component(frmProfileTimesheets(self.userID, self))  # Add the Timesheets component

    def openSettings(self, **event_args):
        """
        Load the Settings component into the container.
        """
        self.cpEmployeeDashboard.clear()  # Clear the container
        self.cpEmployeeDashboard.add_component(Settings())  # Add the Settings component

    def signOut(self, **event_args):
        """
        Log out the current user and redirect to the login form.
        """
        anvil.users.logout()  # Log out the user
        open_form('frmLogin')  # Open the login form

    def menu(self, **Event_args):
        """
        Show a menu for selecting different pages and navigate accordingly.
        """
        choice = confirm(title="Pages:\n", buttons=[("Dashboard", 1), ("Profile", 2), ("Settings", 3)], dismissible=True)
        if choice == 1:
            self.openEmployeeDashboard()  # Open the Employee Dashboard
        elif choice == 2:
            self.openProfileUserDetails(self.userID)  # Open the Profile User Details
        elif choice == 3:
            self.openSettings()  # Open the Settings page
