from ._anvil_designer import EmployeeManagementTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Functions import Other

class EmployeeManagement(EmployeeManagementTemplate):
    def __init__(self, p_parent, **properties):
        self.init_components(**properties)
        self._parent = p_parent
        self.user = anvil.users.get_user()
        self.employees = anvil.server.call("getAllEmployees", self.user["UserID"], "UserID")
        self.refreshEmployeeList(self.employees)


    def refreshEmployeeList(self, employeeList, **event_args):
      if self.ddSort.selected_value == "ID":
        sortBy = "UserID"
      elif self.ddSort.selected_value == "Name":
        sortBy = "FullName"
      elif self.ddSort.selected_value == "Group":
        sortBy = "Group"
      elif self.ddSort.selected_value == "Employment Type":
        sortBy = "Employment"
      self.employees = anvil.server.call("getAllEmployees", self.user["UserID"], sortBy)
      self.rpEmployees.items = [{'employee': emp, 'parent': self} for emp in employeeList]
  
    def addUser(self, **event_args):
      self._parent.selectAddNewUser()

    def openProfileTimesheets(self, employeeID, **event_args):
      self._parent.openProfileTimesheets(employeeID)

    def openProfileUserDetails(self, employeeID, **event_args):
      self._parent.openProfileUserDetails(employeeID)

    def editUserDetails(self, employeeID, **event_args):
      self._parent.editUser(employeeID)

    def resortProfiles(self, **event_args):
      if self.ddSort.selected_value == "ID":
        newOrder = Other.QuickSort(self.employees, "UserID")
        self.refreshEmployeeList(newOrder)
      elif self.ddSort.selected_value == "Name":
        newOrder = Other.QuickSort(self.employees, "FullName")
        self.refreshEmployeeList(newOrder)
      elif self.ddSort.selected_value == "Group":
        newOrder = Other.QuickSort(self.employees, "Group")
        self.refreshEmployeeList(newOrder)
      elif self.ddSort.selected_value == "Employment Type":
        newOrder = Other.QuickSort(self.employees, "Employment")
        self.refreshEmployeeList(newOrder)
