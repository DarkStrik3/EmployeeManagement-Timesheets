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


    def btnColourThemePlainish_click(self, **event_args):
        anvil.server.call('set_user_theme', 'plainish-theme')
        get_open_form().apply_theme('cyanMode')

    def btnColourThemeDefault_click(self, **event_args):
        anvil.server.call('set_user_theme', 'default-theme')
        get_open_form().apply_theme('lightMode')

    def btnColourThemeDark_click(self, **event_args):
        anvil.server.call('set_user_theme', 'dark-theme')
        get_open_form().apply_theme('darkMode')
      
    def saveTheme(self, **event_args):
      """This method is called when the button is clicked"""
      # Command to close the form with this button
      self.raise_event("x-close-alert", value=42)