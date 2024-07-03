from ._anvil_designer import EmployeeManagementTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class EmployeeManagement(EmployeeManagementTemplate):
    def __init__(self, p_parent):
        self.init_components()
        self._parent = p_parent
        self.user = anvil.users.get_user()
        self.refreshEmployeeList()
        self.rpEmployees.set_event_handler('x-edit-user', self.editUserDetails(user_id=item["UserID"]))
        self.rpEmployees.set_event_handler('x-open-user', self.openProfile(user_id))
        self.rpEmployees.set_event_handler('x-refresh', self.refreshEmployeeList(user_id))


    def refreshEmployeeList(self):
        self.employees = anvil.server.call("getAllEmployees", self.user["UserID"])
        self.rpEmployees.items = self.employees

    def addUser(self, **event_args):
        self._parent.selectAddNewUser()

    def openProfile(self, user_id, **event_args):
        self._parent.openSelectedProfile(user_id)

    def editUserDetails(self, user_id, **event_args):
        self._parent.editUser(user_id)
