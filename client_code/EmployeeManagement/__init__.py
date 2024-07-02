from ._anvil_designer import EmployeeManagementTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class EmployeeManagement(EmployeeManagementTemplate):
    def __init__(self, parent=None, **properties):
        self.init_components(**properties)
        self._parent = parent
        self.user = anvil.users.get_user()
        self.refreshEmployeeList()


    def refreshEmployeeList(self):
        self.employees = anvil.server.call("getAllEmployees", self.user["UserID"])
        print(self.employees)  # Debugging: Check the employee data
        self.rpEmployees.items = self.employees

    def addUser(self, **event_args):
        self._parent.selectAddNewUser()

    def openProfile(self, user_id, **event_args):
        self._parent.openSelectedProfile(user_id)

    def editUserDetails(self, user_id, **event_args):
        self._parent.editUser(user_id)
