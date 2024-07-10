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
        self.dataBindings()

    def dataBindings(self):
        try:
            userRow = anvil.server.call('getUserInfo', self.item.get('UserID'))
        except Exception as e:
            print(f"Error fetching user info: {e}")
            userRow = None
        
        try:
            self.lblName.text = userRow.get('FullName', 'Unknown') if userRow else 'Unknown'
        except Exception as e:
            print(f"Error setting lblName: {e}")
            self.lblName.text = 'Unknown'

        try:
            self.lblDate.text = self.item['Date'].strftime('%Y-%m-%d') if self.item.get('Date') else 'N/A'
        except Exception as e:
            print(f"Error setting lblDate: {e}")
            self.lblDate.text = 'N/A'

        try:
            self.lblPayout.text = f"${self.item['Payout']:.2f}" if self.item.get('Payout') is not None else 'N/A'
        except Exception as e:
            print(f"Error setting lblPayout: {e}")
            self.lblPayout.text = 'N/A'

        try:
            self.lblRate.text = f"${self.item['PayRate']:.2f}/hr" if self.item.get('PayRate') is not None else 'N/A'
        except Exception as e:
            print(f"Error setting lblRate: {e}")
            self.lblRate.text = 'N/A'

        try:
            self.lblTimeWorked.text = f"{self.item['HoursWorked']:.2f} hours" if self.item.get('HoursWorked') is not None else 'N/A'
        except Exception as e:
            print(f"Error setting lblTimeWorked: {e}")
            self.lblTimeWorked.text = 'N/A'

        try:
            self.cbApproval.checked = self.item.get('Approval', False)
        except Exception as e:
            print(f"Error setting cbApproval: {e}")
            self.cbApproval.checked = False

    def cbApproval_change(self, **event_args):
        self.item['Approval'] = self.cbApproval.checked
        self.item['selected'] = True
