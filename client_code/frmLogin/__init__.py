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
            if user:
                ID = user['UserID']
                userGroup = user['Group']
                if str(userGroup) == "Warehouse":
                    open_form('frmEmployeeDashboard', userID=ID)
                else:
                    open_form('frmManagerDashboard', userID=ID)
        except Exception as e:
            print("form open error:", e)

