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
      self.employees = anvil.server.call("getAllEmployees", self.user["UserID"])
      self.rpEmployees.items = [{'employee': emp, 'parent': self} for emp in self.employees]

    def addUser(self, **event_args):
        self._parent.selectAddNewUser()

    def openProfile(self, employeeID, **event_args):
        self._parent.openSelectedProfile(employeeID)

    def editUserDetails(self, employeeID, **event_args):
        self._parent.editUser(employeeID)
