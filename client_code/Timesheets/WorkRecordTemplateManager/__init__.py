from ._anvil_designer import WorkRecordTemplateManagerTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class WorkRecordTemplateManager(WorkRecordTemplateManagerTemplate):
    def __init__(self, **properties):
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

        self.lblUserID.text = self.item['item']['UserID']
        self.lblName.text = userRow['FullName'] if userRow else "Unknown"
        self.lblWorkID.text = self.item['item']['WorkID']
        self.lblDate.text = self.item['item']['Date'].strftime('%d/%m/%Y')
        self.lblPayout.text = f"${self.item['item']['Payout']:.2f}" if self.item['item']['Payout'] is not None else 'N/A'
        self.lblRate.text = f"${self.item['item']['PayRate']:.2f}/hr" if self.item['item']['PayRate'] is not None else 'N/A'
        self.lblTimeWorked.text = f"{self.item['item']['HoursWorked']:.2f} hours" if self.item['item']['HoursWorked'] is not None else 'N/A'
        self.cbApproval.checked = self.item['item']['Approval']
        self.cbPaid.checked = self.item['item']['Paid']

        # Make the approval and paid checkboxes read-only
        self.cbApproval.enabled = False
        self.cbPaid.enabled = False

    def selectedChange(self, **event_args):
        self._parent.changeSelectedStatus(self.item['item']['WorkID'], self.cbSelect.checked)
