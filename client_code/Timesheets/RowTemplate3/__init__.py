from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    userRow = anvil.server.call('getUserInfo', self.item['UserID'])
    # Any code you write here will run before the form opens.
    self.lblName = userRow['FullName']
    self.lblDate = self.item['Date']
    self.lblPayout = self.item['Payout']
    self.lblRate = self.item['PayRate']
    self.lblTimeWorked = self.item['HoursWorked']
