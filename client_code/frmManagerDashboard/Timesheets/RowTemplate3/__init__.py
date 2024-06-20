from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    timesheet = anvil.server.call('getTimesheets')
    self.item = timesheet
    # Any code you write here will run before the form opens.
