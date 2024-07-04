from ._anvil_designer import frmProfileTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class frmProfile(frmProfileTemplate):
  def __init__(self, employeeID, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    userRow = anvil.server.call('getUserInfo', employeeID)
    self.lblFullNAME.text = str(userRow['FullName'])
    self.lblEmail.text = str(userRow['Email'])
    self.lblDoB.text = str(user)


    
