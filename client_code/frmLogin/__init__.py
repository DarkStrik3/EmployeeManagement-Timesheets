from ._anvil_designer import frmLoginTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class frmLogin(frmLoginTemplate):
    def __init__(self, **properties):
        """
        Initialize the Login form and set up any necessary components.
        """
        self.init_components(**properties)  # Set up the form properties and data bindings

    def login(self, **event_args):
        """
        Handle user login process.
        """
        # Display the login form and get user credentials
        user = anvil.users.login_with_form(
            show_signup_option=False,  # Do not show the signup option
            allow_remembered=False,    # Do not allow remembered login
            remember_by_default=False,  # Do not remember login by default
            allow_cancel=True          # Allow the user to cancel the login
        )
        
        if user:
            ID = user['UserID']  # Get the user ID
            userGroup = user['Group']  # Get the user group
            
            # Open the appropriate dashboard based on user group
            if userGroup == "Warehouse":
                open_form("frmEmployeeDashboard", userID=ID)  # Open the Employee Dashboard for warehouse employees
            else:
                open_form('frmManagerDashboard', userID=ID)  # Open the Manager Dashboard for managers/accountants
