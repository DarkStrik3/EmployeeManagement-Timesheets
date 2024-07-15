from ._anvil_designer import WorkRecordTemplateEmployeeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class WorkRecordTemplateEmployee(WorkRecordTemplateEmployeeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.border = "thin solid"
    self.lblWorkID.text = "WorkID: " + str(self.item['WorkID'])
    self.lblDate.text = "Date: " + str(self.item['Date'])
    
    # Calculate hours and minutes from HoursWorked
    try:
      total_seconds = self.item['HoursWorked'] * 3600  # Convert hours to seconds
      hours = int(total_seconds // 3600)
      minutes = int((total_seconds % 3600) // 60)mployee
      self.lblHoursWorked.text = f"Time Worked: {hours}h {minutes}m"
      self.lblPayout.text = "Payout: $" + str(round(self.item['Payout'], 2))
    except:
      self.lblHoursWorked.text = " Time Worked: WIP"
      self.lblPayout.text = "Payout: WIP"
      
