from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Functions import Other

class Settings(SettingsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    user = anvil.users.get_user()
    self.userID = user['UserID']
    self.add_class('anvil-role-light-mode')
    userSettings = anvil.server.call('getUserSettings', self.userID)
    Other.apply_mode(userSettings['DarkMode'], self)  # Apply mode using helper function

  def apply_dark_mode(self, enabled):
    form = get_open_form()
    if enabled:
      form.remove_class('anvil-role-light-mode')
      form.add_class('anvil-role-dark-mode')
    else:
      form.remove_class('anvil-role-dark-mode')
      form.add_class('anvil-role-light-mode')

  def saveChanges(self, **event_args):
    anvil.server.call('changeSettings', self.userID, self.cbDark.checked)
    self.apply_dark_mode(self.cbDark.checked)
    alert("Changes were updated.")

  def changePassword(self, **event_args):
    try:
      anvil.users.change_password_with_form(require_old_password=True)
    except:
      alert("Change failed, please try again.")
