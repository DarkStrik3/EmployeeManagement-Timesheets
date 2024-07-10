from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate3(RowTemplate3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.init_data_bindings()

    def init_data_bindings(self):
        userRow = anvil.server.call('getUserInfo', self.item['UserID'])
        self.lblName.text = userRow['FullName']
        self.lblDate.text = self.item['Date'].strftime('%Y-%m-%d')
        self.lblPayout.text = f"${self.item['Payout']:.2f}"
        self.lblRate.text = f"${self.item['PayRate']:.2f}/hr"
        self.lblTimeWorked.text = f"{self.item['HoursWorked']:.2f} hours"
        self.cbApproval.checked = self.item['Approval']

    def cbApproval_change(self, **event_args):
        self.item['Approval'] = self.cbApproval.checked
        self.item['selected'] = True
