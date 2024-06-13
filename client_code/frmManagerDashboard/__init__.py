from ._anvil_designer import frmManagerDashboardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..EmployeeManagement import EmployeeManagement
from ..AnalyticsReporting import AnalyticsReporting
from ..Settings import Settings
from ..Timesheets import Timesheets
from ..AddUser import AddUser


class frmManagerDashboard(frmManagerDashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #self.userID = properties["userID"]
    # Any code you write here will run before the form opens.
    self.cpDashboards.add_component(Settings())


  def signOut(self, **event_args):
    open_form('frmLogin')
  
  def selectEmployeeManagement(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(EmployeeManagement())
    self.btnEmplManage.background = "#6e6e6e"
    self.btnAnalyticReport.background = ""
    self.btnTimesheets.background = ""
    self.btnSettings.background = ""

  def selectAnalyticsReport(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(AnalyticsReporting())
    self.btnEmplManage.background = ""
    self.btnAnalyticReport.background = "#6e6e6e"
    self.btnTimesheets.background = ""
    self.btnSettings.background = ""

  def selectTimesheets(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(Timesheets())
    self.btnEmplManage.background = ""
    self.btnAnalyticReport.background = ""
    self.btnTimesheets.background = "#6e6e6e"
    self.btnSettings.background = ""

  def selectSettings(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(Settings())
    self.btnEmplManage.background = ""
    self.btnAnalyticReport.background = ""
    self.btnTimesheets.background = ""
    self.btnSettings.background = "#6e6e6e"

  def selectAddNewuser(self, **event_args):
    self.cpDashboards.clear()
    self.cpDashboards.add_component(AddUser())
    self.btnEmplManage.background = ""
    self.btnAnalyticReport.background = ""
    self.btnTimesheets.background = ""
    self.btnSettings.background = ""
    




