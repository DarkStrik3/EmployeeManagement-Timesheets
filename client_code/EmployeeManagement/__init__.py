from ._anvil_designer import EmployeeManagementTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class EmployeeManagement(EmployeeManagementTemplate):
    def __init__(self, p_parent, **properties):
        self.init_components(**properties)
        self._parent = p_parent
        self.user = anvil.users.get_user()
        self.refreshEmployeeList()


    def refreshEmployeeList(self, **event_args):
      if self.ddSort.selected_value == "ID":
        sortBy = "UserID"
      elif self.ddSort.selected_value == "Name":
        sortBy = "FullName"
      elif self.ddSort.selected_value == "Group":
        sortBy = "Group"
      elif self.ddSort.selected_value == "Employment Type":
        sortBy = "Employment"
      self.employees = anvil.server.call("getAllEmployees", self.user["UserID"], sortBy)
      self.rpEmployees.items = [{'employee': emp, 'parent': self} for emp in self.employees]

    def addUser(self, **event_args):
      self._parent.selectAddNewUser()

    def openProfileTimesheets(self, employeeID, **event_args):
      self._parent.openProfileTimesheets(employeeID)

    def openProfileUserDetails(self, employeeID, **event_args):
      self._parent.openProfileUserDetails(employeeID)

    def editUserDetails(self, employeeID, **event_args):
      self._parent.editUser(employeeID)
