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
        Initialize the Login form with default settings.
        """
        self.init_components(**properties)  # Set up form components and data bindings

    def login(self, **event_args):
        """
        Perform login using the built-in Anvil form and redirect based on user group.
        """
        try:
          user = anvil.users.login_with_form(show_signup_option=False, allow_remembered=False, remember_by_default=False, allow_cancel=True)
          ID = user['UserID']  # Retrieve user ID
          userGroup = user['Group']  # Retrieve user group
          if user:
              # Open the appropriate dashboard based on the user's group
              if userGroup == "Warehouse":
                  open_form("frmEmployeeDashboard", userID=ID) # Open employee Dashboard
              else:
                  open_form('frmManagerDashboard', userID=ID) # Open the dashboard thats shown to every other group (Managers, etc)
        except:
          pass

