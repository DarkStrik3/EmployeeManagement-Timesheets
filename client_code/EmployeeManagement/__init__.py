from ._anvil_designer import EmployeeManagementTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class EmployeeManagement(EmployeeManagementTemplate):
  def __init__(self, p_parent):
    # Set Form properties and Data Bindings.
    self.init_components()
    self._parent = p_parent
    # Any code you write here will run before the form opens.

  def addUser(self, **event_args):
    self._parent.selectAddNewUser()


