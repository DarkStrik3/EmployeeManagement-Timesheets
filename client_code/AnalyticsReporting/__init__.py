from ._anvil_designer import AnalyticsReportingTemplate
from anvil import *
import anvil.users
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AnalyticsReporting(AnalyticsReportingTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
    self.allRecords = anvil.server.call('getTimesheetsManagers')

  def refreshGraphs(self, **event_args):
    timeChoice = self.ddDates.selected_value
    typeChoice = self.ddGroup.selected_value
    infoChoice = self.ddInfoShown.selected_value
    for record in self.allRecords:
      if 
    