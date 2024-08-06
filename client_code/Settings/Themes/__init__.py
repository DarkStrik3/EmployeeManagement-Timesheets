from ._anvil_designer import ThemesTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Themes(ThemesTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)


  def ThemeLightMode(self, **event_args):
      anvil.server.call('changeSettings', "lightMode")
      get_open_form().applyTheme('lightMode')

  def ThemeDarkMode(self, **event_args):
      anvil.server.call('changeSettings', "darkMode")
      get_open_form().applyTheme('darkMode')

  def ThemeCyanMode(self, **event_args):
      anvil.server.call('changeSettings', "cyanMode")
      get_open_form().applyTheme('cyanMode')
    
  def saveTheme(self, **event_args):
    """This method is called when the button is clicked"""
    # Command to close the form with this button
    self.raise_event("x-close-alert", value=42)

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