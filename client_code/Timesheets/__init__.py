from ._anvil_designer import TimesheetsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Timesheets(TimesheetsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.

  def confirmation(self, btnName):
    cont = confirm("Are you sure you want to proceed with: " + str(btnName) + "?")
    if cont:
      return True
    else:
      return False

  def rejectSelected(self, **event_args):
    if self.confirmation("Reject Selected"):
      pass

  def rejectAll(self, **event_args):
    if self.confirmation("Reject All"):
      pass

  def approveSelected(self, **event_args):
    if self.confirmation("Approve Selected"):
      pass
      
  def approveAll(self, **event_args):
    if self.confirmation("Approve All"):
      pass