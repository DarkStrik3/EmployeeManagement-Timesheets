from ._anvil_designer import frmLoginTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class frmLogin(frmLoginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def login(self, **event_args):
    user = anvil.users.login_with_form(show_signup_option=False, allow_remembered=False, remember_by_default=False, allow_cancel=True)
    ID = user['UserID']
    userGroup = user['Group']
    if user:
      if userGroup == "Warehouse":
        open_form("frmEmployeeDashboard", userID=ID)
      else:
        open_form('frmManagerDashboard', userID=ID)
    else:
      alert("Login failed. Either the email or password is incorrect. Please try again.")
 