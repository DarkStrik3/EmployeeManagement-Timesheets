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
        """
        Initialize the RowTemplate1 form with the provided item properties.
        """
        self.init_components(**properties)  # Set up the form properties and data bindings
        # Set the labels and checkboxes using the properties from the item
        self.lblWorkID.text = str(self.item["WorkID"])  # Display the WorkID
        self.lblClockIn.text = str(self.item["ClockIn"])  # Display the ClockIn time
        self.lblClockOut.text = str(self.item["ClockOut"])  # Display the ClockOut time
        self.lblHoursWorked.text = Other.convertFloatToString(self.item["HoursWorked"])  # Convert hours worked to string format
        self.lblDate.text = str(self.item["Date"])  # Display the date
        self.lblPayout.text = str(self.item["Payout"])  # Display the payout amount
        self.lblPayRate.text = str(self.item["PayRate"])  # Display the pay rate
        self.cbApproval.checked = self.item["Approval"]  # Set the approval checkbox status
        self.cbPaid.checked = self.item["Paid"]  # Set the paid checkbox status
