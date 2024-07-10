from ._anvil_designer import TimesheetsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Timesheets(TimesheetsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.load_timesheets()

    def load_timesheets(self):
        allWorkRecords = anvil.server.call('getTimesheetsManagers')
        self.rpTimesheets.items = allWorkRecords

    def confirmation(self, action):
        return confirm(f"Are you sure you want to {action}?")

    def rejectSelected(self, **event_args):
        if self.confirmation("reject selected items"):
            selected_ids = [item['WorkID'] for item in self.rpTimesheets.items if item['selected']]
            anvil.server.call('updateApprovalStatus', selected_ids, False)
            self.load_timesheets()

    def rejectAll(self, **event_args):
        if self.confirmation("reject all items"):
            all_ids = [item['WorkID'] for item in self.rpTimesheets.items]
            anvil.server.call('updateApprovalStatus', all_ids, False)
            self.load_timesheets()

    def approveSelected(self, **event_args):
        if self.confirmation("approve selected items"):
            selected_ids = [item['WorkID'] for item in self.rpTimesheets.items if item['selected']]
            anvil.server.call('updateApprovalStatus', selected_ids, True)
            self.load_timesheets()

    def approveAll(self, **event_args):
        if self.confirmation("approve all items"):
            all_ids = [item['WorkID'] for item in self.rpTimesheets.items]
            anvil.server.call('updateApprovalStatus', all_ids, True)
            self.load_timesheets()
