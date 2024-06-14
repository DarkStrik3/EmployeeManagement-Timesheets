from ._anvil_designer import AddUserTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Validation import *


class AddUser(AddUserTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.userID = properties["userID"]
    # Any code you write here will run before the form opens.

  def addNewUser(self, **event_args):
    try:
      assert Validation.validateName(self.txtFullName.text)
      assert Validation.validateEmail(self.txtEmail.text)
      assert Validation.validateRate(float(self.txtBaseRate.text), float(self.txtExtendedRate.text), float(self.txtPubHolRate.text))
      anvil.server.call('addNewuser', )
    except:
      alert("At least one of the entries is either blank or incorrectly filled out. Please try again.")
