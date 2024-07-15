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
        self.employeeSelected = {emp["UserID"]: False for emp in self.employees}
        self.refreshEmployeeList(self.employees)

    def getUserRow(self, user_id):
        return next((emp for emp in self.employees if emp["UserID"] == user_id), None)

    def changeSelectedStatus(self, userID, status, **event_args):
        self.employeeSelected[userID] = status

    def getAllSelected(self):
        return [userID for userID, selected in self.employeeSelected.items() if selected]

    def refreshEmployeeList(self, employeeList, **event_args):
        self.rpEmployees.items = [{'employee': emp, 'parent': self} for emp in employeeList]

    def sortFilteredEmployees(self, **event_args):
        if self.cbFiltersEnabled.checked:
            filteredEmployees = self.filterEmployees()
            self.resortProfiles(filteredEmployees)
        else:
            self.resortProfiles()

    def resortProfiles(self, employees=None, **event_args):
        employees = employees if employees is not None else self.employees
        sortBy = self.ddSort.selected_value

        if sortBy == "ID":
            newOrder = Other.QuickSort(employees, "UserID")
        elif sortBy == "Name":
            newOrder = Other.QuickSort(employees, "FullName")
        elif sortBy == "Group":
            newOrder = Other.QuickSort(employees, "Group")
        elif sortBy == "Employment Type":
            newOrder = Other.QuickSort(employees, "Employment")

        self.refreshEmployeeList(newOrder)

    def filterEmployees(self, **event_args):
        if self.cbFiltersEnabled.checked:
            newFilter = []

            for employee in self.employees:
                add = True

                if self.ddGender.selected_value and str(self.ddGender.selected_value) != "All" and employee['Gender'] != str(self.ddGender.selected_value):
                    add = False

                if self.ddGroup.selected_value and str(self.ddGroup.selected_value) != "All" and employee['Group'] != str(self.ddGroup.selected_value):
                    add = False

                if self.ddEmploymentType.selected_value and str(self.ddEmploymentType.selected_value) != "All" and employee['Employment'] != str(self.ddEmploymentType.selected_value):
                    add = False

                if add:
                    newFilter.append(employee)

            self.refreshEmployeeList(newFilter)
            self.resortProfiles(newFilter)
            return newFilter
        else:
            self.refreshEmployeeList(self.employees)
            self.resortProfiles()

    def addUser(self, **event_args):
        self._parent.selectAddNewUser()

    def openProfileTimesheets(self, employeeID, **event_args):
        self._parent.openProfileTimesheets(employeeID)

    def openProfileUserDetails(self, employeeID, **event_args):
        self._parent.openProfileUserDetails(employeeID)

    def editUserDetails(self, employeeID, **event_args):
        self._parent.editUser(employeeID)
