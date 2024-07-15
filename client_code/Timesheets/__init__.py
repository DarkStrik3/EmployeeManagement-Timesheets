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
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.dateFormat = "%d/%m/%Y"
        self.dpDateFilter.format = self.dateFormat
        self.allWorkRecords = anvil.server.call('getTimesheetsManagers')
        self.user_info_cache = {}  # Dictionary to store userRow data
        self.loadTimesheets(self.allWorkRecords)
        self.resortTimesheets()

    def getUserRow(self, user_id):
        if user_id not in self.user_info_cache:
            self.user_info_cache[user_id] = anvil.server.call('getUserInfo', user_id)
        return self.user_info_cache[user_id]

    def resortInputTimesheets(self, timesheets, **event_args):
      sortBy = self.ddSort.selected_value
      if sortBy == "WorkID":
          newOrder = Other.QuickSort(timesheets, "WorkID")
          self.loadTimesheets(newOrder)
      elif sortBy == "Date":
          newOrder = Other.QuickSort(timesheets, "Date")
          self.loadTimesheets(newOrder)
      elif sortBy == "Payout":
          newOrder = Other.QuickSort(timesheets, "Payout")
          self.loadTimesheets(newOrder)      
      elif sortBy == "Work Time":
          newOrder = Other.QuickSort(timesheets, "HoursWorked")
          self.loadTimesheets(newOrder)
  
    def resortTimesheets(self, **event_args):
      sortBy = self.ddSort.selected_value
      if sortBy == "WorkID":
          newOrder = Other.QuickSort(self.allWorkRecords, "WorkID")
          self.loadTimesheets(newOrder)
          return newOrder
      elif sortBy == "Date":
          newOrder = Other.QuickSort(self.allWorkRecords, "Date")
          self.loadTimesheets(newOrder)
          return newOrder
      elif sortBy == "Payout":
          newOrder = Other.QuickSort(self.allWorkRecords, "Payout")
          self.loadTimesheets(newOrder)     
          return newOrder
      elif sortBy == "Work Time":
          newOrder = Other.QuickSort(self.allWorkRecords, "HoursWorked")
          self.loadTimesheets(newOrder)
          return newOrder

    def filterTimesheets(self, **event_args):
      if self.cbFiltersEnabled.checked:
          newFilter = []
          for record in self.allWorkRecords:
              userRow = self.getUserRow(record['UserID'])
              add = True
              # Check date filter
              if self.dpDateFilter.date:
                  record_date_str = record['Date'].strftime(self.dateFormat)
                  filter_date_str = (self.dpDateFilter.date).strftime(self.dateFormat)
                  if record_date_str != filter_date_str:
                      add = False
              # Check approval filter
              if self.cbApprovedFilter.checked is not None and record['Approval'] != self.cbApprovedFilter.checked:
                  add = False
              # Check paid filter
              if self.cbPaidFilter.checked is not None and record['Paid'] != self.cbPaidFilter.checked:
                  add = False
              # Check gender filter
              if self.ddGender.selected_value and str(self.ddGender.selected_value) != "All" and userRow['Gender'] != str(self.ddGender.selected_value):
                  add = False
              # Check group filter
              if self.ddGroup.selected_value and str(self.ddGroup.selected_value) != "All" and userRow['Group'] != str(self.ddGroup.selected_value):
                  add = False
              if add:
                  newFilter.append(record)
          self.loadTimesheets(newFilter)
          self.resortInputTimesheets(newFilter)
          return newFilter
      else:
          # Restore unfiltered records while retaining sorting
          self.loadTimesheets(self.allWorkRecords)
          self.resortTimesheets()


    def loadTimesheets(self, allWorkRecords, **event_args):
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
      if self.cbFiltersEnabled.checked:
        filteredRecords = self.filterTimesheets()
        sortedRecords = self.resortInputTimesheets(filteredRecords)
      else:
        self.resortTimesheets()

    def rejectSelected(self, **event_args):
        if confirm("Are you sure you want to reject selected items? Rejected items are deleted."):
            selectedIDs = [item['item']['WorkID'] for item in self.rpTimesheets.items if item['item']['Approved']]
            anvil.server.call('updateApprovalStatus', selectedIDs, False)
            self.sortFilteredRecords()

    def rejectAll(self, **event_args):
        if confirm("Are you sure you want to reject all items? Rejected items are deleted."):
            allIDs = [item['item']['WorkID'] for item in self.rpTimesheets.items]
            anvil.server.call('updateApprovalStatus', allIDs, False)
            self.sortFilteredRecords()

    def approveSelected(self, **event_args):
        if self.confirmation("approve selected items"):
            selected_ids = [item['item']['WorkID'] for item in self.rpTimesheets.items if item['item']['Approved']]
            anvil.server.call('updateApprovalStatus', selected_ids, True)
            self.sortFilteredRecords()

    def approveAll(self, **event_args):
        if self.confirmation("approve all items"):
            allIDs = [item['item']['WorkID'] for item in self.rpTimesheets.items]
            anvil.server.call('updateApprovalStatus', allIDs, True)
            self.sortFilteredRecords()

    def markSelectedPaid(self, **event_args):
      if self.confirmation("mark selected selected items as paid"):
            selectedIDs = [item['item']['WorkID'] for item in self.rpTimesheets.items if item['item']['Paid']]
            anvil.server.call('updatePaymentStatus', selectedIDs, True)
            self.sortFilteredRecords()

    def markAllPaid(self, **event_args):
      if self.confirmation("mark all items as paid"):
        allIDs = [item['item']['WorkID'] for item in self.rpTimesheets.items]
        anvil.server.call('updatePaymentStatus', allIDs)
        self.sortFilteredRecords()
