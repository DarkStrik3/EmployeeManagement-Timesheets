from ._anvil_designer import TimesheetsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Timesheets(TimesheetsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.

  def confirm(btnName):
    cont = confirm("Are you sure you want to proceed with: " + str(btnName) + "?")
    if cont:
      return True
    else:
      return False