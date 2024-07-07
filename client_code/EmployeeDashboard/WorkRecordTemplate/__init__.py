from ._anvil_designer import WorkRecordTemplateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class WorkRecordTemplate(WorkRecordTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.lblWorkID = str(self.item['WorkID'])
    self.lblDate = str(self.item['Date'])
    self.lblHoursWorked = str(self.item['HoursWorked'])
    self.lblPayout = str(self.item['Payout'])
    self.lblPayRate = self.item['PayRate']
    # Any code you write here will run before the form opens.
