from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Settings(SettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    userSettings = anvil.server.call('getUserSettings', userID)
    self.cbDark.checked = userSettings['DarkMode']



  def changeDarkMode(self, **event_args):
    anvil.server.call('changeSettings', userID, self.cbDark.checked)
