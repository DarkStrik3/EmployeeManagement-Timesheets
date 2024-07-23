from ._anvil_designer import EditUserTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Functions import Validation
from ..Functions import Other
from datetime import datetime


class EditUser(EditUserTemplate):
  def __init__(self, employeeID, p_parent, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.dpDoB.max_date = Other.getDate15YearsAgo()  # makes sure that the worker is at least 15 years old which is a requirement to work
    self.dpDoB.format = "%d/%m/%Y"
    self.flUpload.file_types = [".jpg", ".jpeg", ".png", "webp"]
    self.employeeId = employeeID
    self._parent = p_parent
    # Sets all pre-existing data into the required inputs
    userRow = anvil.server.call('getUserInfo', employeeID)
    self.imgUpload.source = userRow['Profile']
    self.txtFullName.text = userRow['FullName']
    self.txtEmail.text = userRow['Email']
    self.txtPhoneNumber.text = userRow['PhoneNumber']
    self.dpDoB.date = userRow['DoB']
    self.txtTitle.text = userRow['Title']
    self.txtTFN.text = userRow['TFN']
    self.txtBaseRate.text = str(userRow['BasicRate'])
    self.txtExtendedRate.text = str(userRow['ExtendedRate'])
    self.txtPubHolRate.text = str(userRow['PublHolRate'])
    self.ddEmplType.selected_value = userRow['Employment']
    self.ddGroup.selected_value = userRow['Group']
    self.ddGender.selected_value = userRow['Gender']
    
  def editUser(self, **event_args):
    issues = []
    if not Validation.validateString(self.txtFullName.text):  # makes sure that the name is a valid string
      issues.append("invalid name")
    if not Validation.validateString(self.txtTitle.text):  # makes sure that the title is a valid string
      issues.append("invalid title")
    if not Validation.validateEmail(self.txtEmail.text):  # makes sure that email is valid
      issues.append("invalid email")
    # additional rates are higher than base rate, and base rate is at least minimum wage
    if not Validation.validateRate(self.txtBaseRate.text, self.txtExtendedRate.text, self.txtPubHolRate.text):
      issues.append("invalid rates")
    if not Validation.validateDate(str(self.dpDoB.date)):  # date is valid
      issues.append("invalid date of birth")
    if (self.ddGender.selected_value is None):  # make sure one of the specified options is selected
      issues.append("invalid gender")
    if (self.ddEmplType.selected_value is None):  # make sure one of the specified options is selected
      issues.append("invalid employment type")
    if (self.ddGroup.selected_value is None):  # make sure one of the specified options is selected
      issues.append("invalid group selected")
    if not Validation.validatePhoneNum(self.txtPhoneNumber.text):  # Makes sure that the phone number is valid
      issues.append("invalid phone number")
    if not Validation.validateTFN(self.txtTFN.text):  # Makes sure that TFN is valid
      issues.append("invalid TFN number")
    if not Validation.validateUpload(self.imgUpload.source):
      issues.append("invalid file type uploaded")
    if issues == [] or len(issues) == 0:
      # Call the server code to pass the values and create a new user.
      if confirm(
        "Please confirm that the following details are correct prior to continuing:\n"
        + "Full Name: "
        + self.txtFullName.text
        + "\nEmail: "
        + self.txtEmail.text
        + "\nPhone Number: "
        + self.txtPhoneNumber.text
        + "\nDate of birth: "
        + str(self.dpDoB.date)
        + "\nGender: "
        + str(self.ddGender.selected_value)
        + "\nGroup: "
        + str(self.ddGroup.selected_value)
        + "\nTitle: "
        + self.txtTitle.text
        + "\nBase Rate: "
        + self.txtBaseRate.text
        + "\nExtendedRate: "
        + self.txtExtendedRate.text
        + "\nPublic Holiday Rate: "
        + self.txtPubHolRate.text
        + "\nTFN: "
        + self.txtTFN.text
      ):
        try:
          anvil.server.call(
            "editUser",
            self.employeeId,
            self.txtFullName.text,
            self.txtEmail.text,
            self.txtPhoneNumber.text,
            self.dpDoB.date,
            self.ddGender.selected_value,
            self.ddEmplType.selected_value,
            self.ddGroup.selected_value,
            self.txtTitle.text,
            float(self.txtBaseRate.text),
            float(self.txtExtendedRate.text),
            float(self.txtPubHolRate.text),
            self.txtTFN.text,
            self.flUpload.file,
          )
          self.imgUpload.source = None
          self.flUpload.clear()
          self.txtFullName.text = ""
          self.txtEmail.text = ""
          self.txtPhoneNumber.text = ""
          self.txtBaseRate.text = ""
          self.txtExtendedRate.text = ""
          self.txtPubHolRate.text = ""
          self.txtTitle.text = ""
          self.txtTFN.text = ""
          self.ddEmplType.selected_value = None
          self.ddGender.selected_value = None
          self.ddGroup.selected_value = None
          self.dpDoB.date = None
        except Exception as e:
          alert(f"An error occurred: {str(e)}")
          self.txtEmail.text = ""
        if confirm("Would you like to view this profile?"):
          self._parent.openSelectedProfile(self.employeeId)
    else:
      issueString = ""
      n = 0
      for issue in issues:
        if n == 0:
          issueString = (
            "At least one of the entries is either blank or incorrectly filled out. Please try again. This includes: "
            + issue
          )
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
    except Exception as e:
      alert(
        f"The file that was uploaded doesn't match the required format. Please upload an image such as PNG or PJG. Error: {str(e)}"
      )
      self.flUpload.clear()
