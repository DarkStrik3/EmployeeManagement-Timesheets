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
    user = anvil.users.login_with_form(show_signup_option=False, allow_remembered=True, remember_by_default=True, allow_cancel=True)
    print(user)
    if user:
      userRow = anvil.users.get_user()
      userID = userRow['UserID']
      userGroup = userRow['Group']
      if userGroup == "Warehouse":
        open_form("frmEmployeeDashboard", userID=userID)
      else:
        open_form('frmManagerDashboard', userID=userID)
    else:
      alert("Login failed. Please try again.")
    
    #userIdentification = anvil.server.call("Authenticate", self.txtEmail.text, self.txtPassword.text)
    #if userIdentification == "404":
      #alert("This user does not exist, or the inputed password is incorrect. Please try again.")
      #self.txtEmail.text = ""
      #self.txtPassword.text = ""
    #else:
      #userRow = anvil.server.call('getUserInfo', userIdentification, True)
      #userID = userRow["UserID"]
      #group = userRow['Group']
      #if group == "Warehouse":
        #anvil.
        #open_form("frmEmployeeDashboard")
        
      #else:
        #open_form('frmManagerDashboard')
