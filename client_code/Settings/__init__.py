from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Functions import Other
from .Themes import Themes

class Settings(SettingsTemplate):
  def __init__(self, **properties):
    """
    Constructor for the Settings class. Initializes the settings form
    and loads the user settings.
    
    Parameters:
    properties (dict): Properties to initialize the form with.
    """
    self.init_components(**properties)  # Initialize form components with given properties.
    user = anvil.users.get_user()  # Get the currently logged-in user.
    self.userID = user['UserID']  # Store the user's ID for future use.
    userSettings = anvil.server.call('getUserSettings', self.userID)  # Fetch user settings from the server.
    self.cbDark.checked = userSettings['DarkMode']  # Set the dark mode checkbox based on the user's settings.

  def saveChanges(self, **event_args):
    """
    Save changes to the user settings. Updates the dark mode setting on the server.
    
    Parameters:
    event_args (dict): Event arguments passed by the Anvil framework.
    """
    anvil.server.call('changeSettings', self.userID, self.cbDark.checked)  # Call the server to update the dark mode setting.
    alert("Changes were updated.")  # Show a confirmation alert to the user.

  def changePassword(self, **event_args):
    """
    Change the user's password. Opens a form to change the password and handles any errors.
    
    Parameters:
    event_args (dict): Event arguments passed by the Anvil framework.
    """
    try:
      anvil.users.change_password_with_form(require_old_password=True)  # Open a form to change the password, requiring the old password.
    except:
      alert("Change failed, please try again.")  # Show an alert if the password change fails.


  def Themes(self, **event_args):
    """
    Let user select a theme
    """
    alert(content=Themes(), large=True, buttons=[], title="Themes")
      
    # Function to get the user's currently saved theme and apply it at init
  def applyUserTheme(self):
    theme = anvil.server.call('getUserTheme')
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