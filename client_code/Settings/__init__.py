from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Settings(SettingsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    user = anvil.users.get_user()
    self.userID = user['UserID']
    userSettings = anvil.server.call('getUserSettings', self.userID)
    self.cbDark.checked = userSettings['DarkMode']
    apply_dark_mode(get_open_form(), userSettings['DarkMode'])

  def saveChanges(self, **event_args):
    anvil.server.call('changeSettings', self.userID, self.cbDark.checked)
    apply_dark_mode(get_open_form(), self.cbDark.checked)
    alert("Changes were updated.")

  def changePassword(self, **event_args):
    try:
      anvil.users.change_password_with_form(require_old_password=True)
    except:
      alert("Change failed, please try again.")
