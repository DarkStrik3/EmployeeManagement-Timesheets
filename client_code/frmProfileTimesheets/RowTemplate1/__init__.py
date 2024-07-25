from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...Functions import Other


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.lblWorkID.text = str(self.item["WorkID"])
    self.lblClockIn.text = str(self.item["ClockIn"])
    self.lblClockOut.text = str(self.item["ClockOut"])
    self.lblHoursWorked.text = Other.convertFloatToString(self.item["HoursWorked"])
    self.lblDate.text = str(self.item["Date"])
    self.lblPayout.text = str(self.item["Payout"])
    self.lblPayRate.text = str(self.item["PayRate"])
    self.cbApproval.checked = self.item["Approval"]
    self.cbPaid.checked = self.item["Paid"]