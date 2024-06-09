from ._anvil_designer import frmLoginTemplate
from anvil import *
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
    userIdentification = anvil.server.call("Authenticate", self.txtEmail.text, self.txtPassword.text)
    if userIdentification == "404":
      alert("This user does not exist, or the inputed password is incorrect. Please try again.")
      self.txtEmail.text = ""
      self.txtPassword.text = ""
    else:
      userRow = anvil.server.call('getUserInfo', userIdentification, True)
      userID = userRow["UserID"]
      title = userRow['Title']
      if title == "base employee":
        open_form("frmEmployeeDashboard", userID)
      else:
        open_form('frmManagerDashboard', userID)
