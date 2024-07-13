from ._anvil_designer import TimesheetsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Functions import Other

class Timesheets(TimesheetsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.allWorkRecords = anvil.server.call('getTimesheetsManagers')
        self.user_info_cache = {}  # Dictionary to store userRow data
        self.loadTimesheets(self.allWorkRecords)

    def getUserRow(self, user_id):
        if user_id not in self.user_info_cache:
            self.user_info_cache[user_id] = anvil.server.call('getUserInfo', user_id)
        return self.user_info_cache[user_id]

    def resortTimesheets(self, **event_args):
        sortBy = self.ddSort.selected_value
        if sortBy == "WorkID":
            newOrder = Other.QuickSort(self.allWorkRecords, "WorkID")
            self.loadTimesheets(newOrder)
        elif sortBy == "Date":
            newOrder = Other.QuickSort(self.allWorkRecords, "Date")
            self.loadTimesheets(newOrder)
        elif sortBy == "Payout":
            newOrder = Other.QuickSort(self.allWorkRecords, "Payout")
            self.loadTimesheets(newOrder)      
        elif sortBy == "Work Time":
            newOrder = Other.QuickSort(self.allWorkRecords, "HoursWorked")
            self.loadTimesheets(newOrder)

    def filterTimesheets(self, **event_args):
        newFilter = []
        if self.cbFiltersEnabled.checked:
            for record in self.allWorkRecords:
                userRow = self.getUserRow(record['UserID'])
                add = True
                # Date format for comparison
                date_format = "%Y-%m-%d"
                # Check date filter
                if self.dpDateFilter.date:
                    record_date_str = record['Date'].strftime(date_format)
                    filter_date_str = self.dpDateFilter.date.strftime(date_format)
                    if record_date_str != filter_date_str:
                        add = False
                # Check approval filter
                if self.cbApprovedFilter.checked is not None and record['Approval'] != self.cbApprovedFilter.checked:
                    add = False
                # Check paid filter
                if self.cbPaidFilter.checked is not None and record['Paid'] != self.cbPaidFilter.checked:
                    add = False
                # Check gender filter
                if self.ddGender.selected_value and userRow['Gender'] != str(self.ddGender.selected_value):
                    add = False
                # Check group filter
                if self.ddGroup.selected_value and userRow['Group'] != str(self.ddGroup.selected_value):
                    add = False
                if add:
                    newFilter.append(record)
        
        self.filteredWorkRecords = newFilter
        self.loadTimesheets(self.filteredWorkRecords)

    def loadTimesheets(self, allWorkRecords):
        totalUnapproved = 0
        totalUnpaid = 0
        for record in allWorkRecords:
            if not record['Approval']:
                totalUnapproved += 1
            if not record['Paid']:
                totalUnpaid += 1
        self.lblTotalPending.text = str(totalUnapproved)
        self.lblTotalUnpaid.text = str(totalUnpaid)
    
        self.rpTimesheets.items = [{'item': d, 'user_info_cache': self.user_info_cache, 'p_parent': self} for d in allWorkRecords]

    def confirmation(self, action):
        return confirm(f"Are you sure you want to {action}?")

    def rejectSelected(self, **event_args):
        if self.confirmation("reject selected items"):
            selected_ids = [item['item']['WorkID'] for item in self.rpTimesheets.items if item['item']['selected']]
            anvil.server.call('updateApprovalStatus', selected_ids, False)
            self.loadTimesheets()

    def rejectAll(self, **event_args):
        if self.confirmation("reject all items"):
            all_ids = [item['item']['WorkID'] for item in self.rpTimesheets.items]
            anvil.server.call('updateApprovalStatus', all_ids, False)
            self.loadTimesheets()

    def approveSelected(self, **event_args):
        if self.confirmation("approve selected items"):
            selected_ids = [item['item']['WorkID'] for item in self.rpTimesheets.items if item['item']['selected']]
            anvil.server.call('updateApprovalStatus', selected_ids, True)
            self.loadTimesheets()

    def approveAll(self, **event_args):
        if self.confirmation("approve all items"):
            all_ids = [item['item']['WorkID'] for item in self.rpTimesheets.items]
            anvil.server.call('updateApprovalStatus', all_ids, True)
            self.loadTimesheets()
