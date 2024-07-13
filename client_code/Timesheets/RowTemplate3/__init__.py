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
        self._parent = self.item['p_parent']
        self.dataBindings()

    def dataBindings(self):
        user_id = self.item['item']['UserID']
        try:
            userRow = self._parent.getUserRow(user_id)
        except KeyError as e:
            print(f"Error fetching user info: {e}")
            userRow = None

        try:
            self.lblUserID.text = self.item['item']['UserID']
        except Exception as e:
            print(f"Error setting lblUserID: {e}")
            self.lblUserID.text = "Unknown"

        try:
            self.lblName.text = userRow['FullName'] if userRow else "Unknown"
        except Exception as e:
            print(f"Error setting lblName: {e}")
            self.lblName.text = "Unknown"

        try:
            self.lblWorkID.text = self.item['item']['WorkID']
        except Exception as e:
            print(f"Error setting lblWorkID: {e}")
            self.lblWorkID.text = "Unknown"

        try:
            self.lblDate.text = self.item['item']['Date'].strftime('%d/%m/%Y')
        except Exception as e:
            print(f"Error setting lblDate: {e}")
            self.lblDate.text = 'N/A'

        try:
            self.lblPayout.text = f"${self.item['item']['Payout']:.2f}" if self.item['item']['Payout'] is not None else 'N/A'
        except Exception as e:
            print(f"Error setting lblPayout: {e}")
            self.lblPayout.text = 'N/A'

        try:
            self.lblRate.text = f"${self.item['item']['PayRate']:.2f}/hr" if self.item['item']['PayRate'] is not None else 'N/A'
        except Exception as e:
            print(f"Error setting lblRate: {e}")
            self.lblRate.text = 'N/A'

        try:
            self.lblTimeWorked.text = f"{self.item['item']['HoursWorked']:.2f} hours" if self.item['item']['HoursWorked'] is not None else 'N/A'
        except Exception as e:
            print(f"Error setting lblTimeWorked: {e}")
            self.lblTimeWorked.text = 'N/A'

        try:
            self.cbApproval.checked = self.item['item']['Approval']
        except Exception as e:
            print(f"Error setting cbApproval: {e}")
            self.cbApproval.checked = False

    def cbApproval_change(self, **event_args):
        self.item['item']['Approval'] = self.cbApproval.checked
        self.item['item']['selected'] = True
