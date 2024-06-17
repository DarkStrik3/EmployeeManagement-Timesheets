from ._anvil_designer import AddUserTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Validation import *
from datetime import datetime

class AddUser(AddUserTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.userID = properties["userID"]
    # Any code you write here will run before the form opens.

  def addNewUser(self, **event_args):
    dateFormatCode = "%d/%m/%Y"  # The date format is specified to allow for future changes by changing only 1 variable
    try:
      assert Validation.validateString(self.txtFullName.text) # makes sure that the name is a valid string
      assert Validation.validateString(self.txtTitle.text) # makes sure that the title is a valid string
      assert Validation.validateEmail(self.txtEmail.text) # makes sure that email is valid
      # additional rates are higher than base rate, and base rate is at least minimum wage
      assert Validation.validateRate(float(self.txtBaseRate.text), float(self.txtExtendedRate.text), float(self.txtPubHolRate.text)) 
      assert Validation.validateDate(self.dpDoB.date.strftime(dateFormatCode), dateFormatCode) # date is valid
      assert str(self.ddGender.selected_value) == "Male" or "Female" or "Other" # make sure one of the specified options is selected
      assert str(self.ddEmplType.selected_value) == "Full Time" or "Part Time" # make sure one of the specified options is selected
      assert str(self.ddGroup.selected_value) == "Warehouse" or "Manager" or "Admin" or "Accountant" # make sure one of the specified options is selected

      
      anvil.server.call('addNewuser', )
    except:
      alert("At least one of the entries is either blank or incorrectly filled out. Please try again.")

  def uploadProfile(self, **event_args):
    try:
      imgFile = self.flUpload.file
      assert imgFile is not None
      imgFileName = imgFile.name.lower()
      validExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
      assert any(imgFileName.endswith(ext) for ext in validExtensions)
      self.imgUpload.source = imgFile
    except:
      alert("The file that was uploaded doesn't match the required format. Please upload an image such as PNG or PJG.")
      self.flUpload.clear()
