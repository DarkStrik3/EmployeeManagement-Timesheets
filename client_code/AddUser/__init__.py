from ._anvil_designer import AddUserTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Functions import Validation
from datetime import datetime

class AddUser(AddUserTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.userID = properties["userID"]
    # Any code you write here will run before the form opens.

  def addNewUser(self, **event_args):
    dateFormatCode = "%d/%m/%Y"  # The date format is specified to allow for future changes by changing only 1 variable
    issues = []
    if not Validation.validateString(self.txtFullName.text): # makes sure that the name is a valid string
      issues.append("invalid name")
    if not Validation.validateString(self.txtTitle.text): # makes sure that the title is a valid string
      issues.append("invalid title")
    if not Validation.validateEmail(self.txtEmail.text): # makes sure that email is valid
      issues.append("invalid email")
    # additional rates are higher than base rate, and base rate is at least minimum wage
    if not Validation.validateRate(self.txtBaseRate.text, self.txtExtendedRate.text, self.txtPubHolRate.text):
      issues.append("invalid rates")
    if not Validation.validateDate(self.dpDoB.date, dateFormatCode): # date is valid
      issues.append("invalid date of birth")
    if str(self.ddGender.selected_value) != "Male" or "Female" or "Other": # make sure one of the specified options is selected
      issues.append("invalid gender")
    if str(self.ddEmplType.selected_value) != "Full Time" or "Part Time": # make sure one of the specified options is selected
      issues.append("invalid employment type")
    if str(self.ddGroup.selected_value) != "Warehouse" or "Manager" or "Admin" or "Accountant": # make sure one of the specified options is selected
      issues.append("invalid group selected")
    if not Validation.validatePhoneNum(self.txtPhoneNumber.text): # Makes sure that the phone number is valid
      issues.append("invalid phone number")
    if not Validation.validateTFN(self.txtTFN.text): # Makes sure that TFN is valid
      issues.append("invalid TFN number")
    if not Validation.validateUpload(self.flUpload.file)
      issues.append("")
    if issues == "":
    # Call the server code to pass the values and create a new user.
      anvil.server.call('addNewuser', self.txtFullName.text, self.txtEmail.text, self.txtTempPassword.text, self.txtPhoneNumber.text, self.dpDoB.date, self.ddGender.selected_value, self.ddEmplType.selected_value, self.ddGroup.selected_value, self.txtTitle.text, float(self.txtBaseRate.text), float(self.txtExtendedRate.text), float(self.txtPubHolRate.text), self.txtTFN.text, self.flUpload.file)
      self.imgUpload.clear()
      self.flUpload.clear()
      self.txtFullName.clear()
      self.txtEmail.clear()
      self.txtPhoneNumber.clear()
      self.txtBaseRate.clear()
      self.txtExtendedRate.clear()
      self.txtPubHolRate.clear()
      self.txtTFN.clear()
      self.ddEmplType.clear()
      self.ddGender.clear()
      self.ddGroup.clear()
      self.dpDoB.clear()
    else:
      issueString = ""
      n = 0
      for issue in issues:
        if n == 0:
          issueString = "At least one of the entries is either blank or incorrectly filled out. Please try again. This includes: " + issue
          n += 1
        else:
          n += 1
          if len(issues) == n:
            issueString = issueString + ", and " + issue + "."
          else:
            issueString = issueString + ", " + issue
      alert(str(issueString))

  def uploadProfile(self, **event_args):
    try:
      imgFile = self.flUpload.file
      assert Validation.validateUpload(imgFile)
      self.imgUpload.source = imgFile
    except:
      alert("The file that was uploaded doesn't match the required format. Please upload an image such as PNG or PJG.")
      self.flUpload.clear()
