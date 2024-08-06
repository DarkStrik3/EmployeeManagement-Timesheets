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
      
