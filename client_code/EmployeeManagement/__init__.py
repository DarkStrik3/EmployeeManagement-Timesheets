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
        """
        Purpose: Initialize the EmployeeManagement form with default properties.
        Input: 
            p_parent (object) - Parent form or container.
            **properties (dict) - Additional properties.
        Process: Sets form components, initializes user and employee data, and refreshes the employee list.
        Output: None
        """
        self.init_components(**properties)
        self._parent = p_parent
        self.user = anvil.users.get_user()
        self.employees = anvil.server.call("getAllEmployees", self.user["UserID"], "UserID", False)
        self.employeeSelected = {emp["UserID"]: False for emp in self.employees}
        self.refreshEmployeeList(self.employees)

    def getUserRow(self, user_id):
        """
        Purpose: Retrieve the employee data row based on user_id.
        Input: 
            user_id (int) - Unique identifier for the user.
        Process: Searches the employees list for the matching user_id.
        Output: (dict) - Employee data row.
        """
        return next((emp for emp in self.employees if emp["UserID"] == user_id), None)

    def refreshEmployeeList(self, employeeList, **event_args):
        """
        Purpose: Refresh the displayed employee list.
        Input: 
            employeeList (list) - List of employee data.
            **event_args (dict) - Additional event arguments.
        Process: Updates the repeating panel with the new employee list.
        Output: None
        """
        self.rpEmployees.items = [{'employee': emp, 'parent': self} for emp in employeeList]

    def sortFilteredEmployees(self, **event_args):
        """
        Purpose: Sort and filter the employee list based on user-selected criteria.
        Input: **event_args (dict) - Additional event arguments.
        Process: Filters and sorts employees if filters are enabled; otherwise, sorts the full list.
        Output: None
        """
        if self.cbFiltersEnabled.checked:
            self.filterEmployees()
        else:
            self.resortProfiles(self.employees)

    def resortProfiles(self, employees, **event_args):
        """
        Purpose: Sort the employee profiles based on selected criteria.
        Input: 
            employees (list) - List of employee data.
            **event_args (dict) - Additional event arguments.
        Process: Sorts the employees based on the selected sort option.
        Output: None
        """
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
        """
        Purpose: Filter the employee list based on user-selected criteria.
        Input: **event_args (dict) - Additional event arguments.
        Process: Filters the employees based on gender, group, and employment type.
        Output: (list) - Filtered list of employees.
        """
        if self.cbFiltersEnabled.checked:
          self.filterEmployeesDropdown() # This is done to save duplicating the code
        else:
          # If the filters get disabled, everything is reset to the original view without any filters enabled.
            self.resortProfiles(self.employees)


    def filterEmployeesDropdown(self, **event_args):
      """
      Purpose: Filter the employee list based on user-selected criteria.
      Input: **event_args (dict) - Additional event arguments.
      Process: Filters the employees based on gender, group, and employment type.
      Output: (list) - Filtered list of employees.
      """
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
          return newFilter 

    def addUser(self, **event_args):
        """
        Purpose: Trigger the addition of a new user.
        Input: **event_args (dict) - Additional event arguments.
        Process: Calls the parent form's selectAddNewUser method.
        Output: None
        """
        self._parent.selectAddNewUser()

    def openProfileTimesheets(self, employeeID, **event_args):
        """
        Purpose: Open the timesheet profile for the selected employee.
        Input: 
            employeeID (int) - Unique identifier for the employee.
            **event_args (dict) - Additional event arguments.
        Process: Calls the parent form's openProfileTimesheets method.
        Output: None
        """
        self._parent.openProfileTimesheets(employeeID)

    def openProfileUserDetails(self, employeeID, **event_args):
        """
        Purpose: Open the user details profile for the selected employee.
        Input: 
            employeeID (int) - Unique identifier for the employee.
            **event_args (dict) - Additional event arguments.
        Process: Calls the parent form's openProfileUserDetails method.
        Output: None
        """
        self._parent.openProfileUserDetails(employeeID)

    def editUserDetails(self, employeeID, **event_args):
        """
        Purpose: Trigger the editing of user details for the selected employee.
        Input: 
            employeeID (int) - Unique identifier for the employee.
            **event_args (dict) - Additional event arguments.
        Process: Calls the parent form's editUser method.
        Output: None
        """
        self._parent.editUser(employeeID)

    # Function to get the user's currently saved theme and apply it at init
    def applyUserTheme(self):
      theme = anvil.server.call('getUserSettings')['Theme']
      self.apply_theme(theme)
  
      # Function to change CSS class which is active to select theme
    def applyTheme(self, theme_name):
      js_code = f"""
      document.body.className = '';
      document.body.classList.add('{theme_name}');
      """
      self.callJS(js_code)
  
    def callJS(self, js_code):
      """
      Add JS
      """
      anvil.js.window.eval(js_code)