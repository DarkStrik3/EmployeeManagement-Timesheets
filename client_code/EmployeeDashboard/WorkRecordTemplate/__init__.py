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
    self.lblWorkID.text = "WorkID: " + str(self.item['WorkID'])
    self.lblDate.text = "Date: " + str(self.item['Date'])
    self.lblHoursWorked.text = "Time worked: " + str(self.item['HoursWorked'])
    self.lblPayout.text = "Payout: " + str(self.item['Payout'])
    self.lblPayRate.text = "Payrate: " + str(self.item['PayRate'])
