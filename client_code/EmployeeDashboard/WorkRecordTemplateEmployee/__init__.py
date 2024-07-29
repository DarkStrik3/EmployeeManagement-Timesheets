from ._anvil_designer import WorkRecordTemplateEmployeeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...Functions import Other


class WorkRecordTemplateEmployee(WorkRecordTemplateEmployeeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.border = "thin solid"
    self.lblWorkID.text = "WorkID: " + str(self.item['WorkID'])
    self.lblDate.text = "Date: " + str(self.item['Date'])
    
    # Calculate hours and minutes from HoursWorked
    try:
      self.lblHoursWorked.text = Other.convertFloatToString(self.item['HoursWorked'])
      self.lblPayout.text = "Payout: $" + str(round(self.item['Payout'], 2))
    except: # The employee hasnt yet clocked out, meaning there isnt any data for hours worked or payout
      self.lblHoursWorked.text = " Time Worked: WIP"
      self.lblPayout.text = "Payout: WIP"
      
