from ._anvil_designer import TimesheetsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Functions import Other
from ..Functions import Validation

class Timesheets(TimesheetsTemplate):
    def __init__(self, **properties):
        """
        Initialize the Timesheets form, set up data bindings, and load initial data.
        """
        self.init_components(**properties)
        self.dateFormat = "%d/%m/%Y"  # Date format used throughout the form
        self.dpDateFilter.format = self.dateFormat  # Set the date picker format
        self.user_info_cache = {}  # Cache for storing user information
        self.workRecordSelected = {}  # Dictionary to track selection status of work records

        # Load all work records and initialize selection statuses
        self.getAllWorkRecords()
        self.loadTimesheets(self.allWorkRecords)
        self.resortTimesheets()

    def getAllWorkRecords(self, **event_args):
        """
        Fetch all work records from the server and initialize their selection statuses.
        """
        self.allWorkRecords = anvil.server.call('getTimesheetsManagers')
        for record in self.allWorkRecords:
            self.workRecordSelected[record['WorkID']] = False

    def changeSelectedStatus(self, workID, status, **event_args):
        """
        Update the selection status of a work record.
        """
        self.workRecordSelected[workID] = status

    def getAllSelected(self):
        """
        Get a list of IDs of all selected work records.
        """
        return [workID for workID, selected in self.workRecordSelected.items() if selected]

    def getUserRow(self, user_id):
        """
        Retrieve user information from cache or fetch from the server if not cached.
        """
        if user_id not in self.user_info_cache:
            self.user_info_cache[user_id] = anvil.server.call('getUserInfo', user_id)
        return self.user_info_cache[user_id]

    def resortInputTimesheets(self, timesheets, **event_args):
        """
        Sort the timesheets based on the selected sorting criteria.
        """
        sortBy = self.ddSort.selected_value
        if sortBy == "WorkID":
            newOrder = Other.QuickSort(timesheets, "WorkID")
        elif sortBy == "Date":
            newOrder = Other.QuickSort(timesheets, "Date")
        elif sortBy == "Payout":
            newOrder = Other.QuickSort(timesheets, "Payout")
        elif sortBy == "Work Time":
            newOrder = Other.QuickSort(timesheets, "HoursWorked")
        self.loadTimesheets(newOrder)

    def resortTimesheets(self, **event_args):
        """
        Resort the timesheets using the current criteria.
        """
        self.resortInputTimesheets(self.allWorkRecords)

    def filterTimsheetsDropdown(self, **event_args):
      """
      Only for dropdowns, so no changes would be made if filters arent enabled.
      """
      if self.cbFiltersEnabled.checked:
        self.filterTimesheets()
  
    def filterTimesheets(self, **event_args):
        """
        Filter timesheets based on user-selected filters and update the display.
        """
        if self.cbFiltersEnabled.checked:
            newFilter = []
            for record in self.allWorkRecords:
                userRow = self.getUserRow(record['UserID'])
                add = True
                if self.dpDateFilter.date:
                    record_date_str = record['Date'].strftime(self.dateFormat)
                    filter_date_str = self.dpDateFilter.date.strftime(self.dateFormat)
                    if record_date_str != filter_date_str:
                        add = False
                if self.cbApprovedFilter.checked is not None and record['Approval'] != self.cbApprovedFilter.checked:
                    add = False
                if self.cbPaidFilter.checked is not None and record['Paid'] != self.cbPaidFilter.checked:
                    add = False
                if self.ddGender.selected_value and str(self.ddGender.selected_value) != "All" and userRow['Gender'] != str(self.ddGender.selected_value):
                    add = False
                if self.ddGroup.selected_value and str(self.ddGroup.selected_value) != "All" and userRow['Group'] != str(self.ddGroup.selected_value):
                    add = False
                if add:
                    newFilter.append(record)
            self.loadTimesheets(newFilter)
            self.resortInputTimesheets(newFilter)
            return newFilter
        else:
            self.loadTimesheets(self.allWorkRecords)
            self.resortTimesheets()

    def loadTimesheets(self, allWorkRecords, **event_args):
        """
        Load the timesheets into the repeating panel and update the totals.
        """
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

    def sortFilteredRecords(self, **event_args):
        """
        Sort the records based on current filters and sorting criteria.
        """
        if self.cbFiltersEnabled.checked:
            filteredRecords = self.filterTimesheets()
            self.resortInputTimesheets(filteredRecords)
        else:
            self.resortTimesheets()

    def rejectSelected(self, **event_args):
        """
        Reject the selected work records by updating their approval status.
        """
        if confirm("Are you sure you want to reject selected items? Rejected items are deleted."):
            selectedIDs = self.getAllSelected()
            anvil.server.call('updateApprovalStatus', selectedIDs, False)
            self.getAllWorkRecords()
            self.sortFilteredRecords()

    def rejectAll(self, **event_args):
        """
        Reject all work records by updating their approval status.
        """
        if confirm("Are you sure you want to reject all items? Rejected items are deleted."):
            allIDs = [item['item']['WorkID'] for item in self.rpTimesheets.items]
            anvil.server.call('updateApprovalStatus', allIDs, False)
            self.getAllWorkRecords()
            self.sortFilteredRecords()

    def approveSelected(self, **event_args):
        """
        Approve the selected work records by updating their approval status.
        """
        if confirm("Are you sure you want to approve selected items?"):
            selectedIDs = self.getAllSelected()
            anvil.server.call('updateApprovalStatus', selectedIDs, True)
            self.getAllWorkRecords()
            self.sortFilteredRecords()

    def approveAll(self, **event_args):
        """
        Approve all work records by updating their approval status.
        """
        if confirm("Are you sure you want to approve all items?"):
            allIDs = [item['item']['WorkID'] for item in self.rpTimesheets.items]
            anvil.server.call('updateApprovalStatus', allIDs, True)
            self.getAllWorkRecords()
            self.sortFilteredRecords()

    def markSelectedPaid(self, **event_args):
        """
        Mark selected work records as paid.
        """
        if confirm("Are you sure you want to mark selected items as paid? This action cannot be undone."):
            selectedIDs = self.getAllSelected()
            anvil.server.call('updatePaymentStatus', selectedIDs)
            self.getAllWorkRecords()
            self.sortFilteredRecords()

    def markAllPaid(self, **event_args):
        """
        Mark all work records as paid.
        """
        if confirm("Are you sure you want to mark all items as paid? This action cannot be undone."):
            allIDs = [item['item']['WorkID'] for item in self.rpTimesheets.items]
            anvil.server.call('updatePaymentStatus', allIDs)
            self.getAllWorkRecords()
            self.sortFilteredRecords()
