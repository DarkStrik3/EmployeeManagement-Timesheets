from ._anvil_designer import AddUserTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Functions import Validation
from ..Functions import Other
from datetime import datetime

class AddUser(AddUserTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)  # Initialize form components with properties
        # Any code you write here will run before the form opens.
        self.dpDoB.max_date = Other.getDate15YearsAgo()  # Set max date to ensure the user is at least 15 years old
        self.dpDoB.format = "%d/%m/%Y"  # Set date format
        self.flUpload.file_types = ['.jpg', '.jpeg', '.png', 'webp']  # Restrict file types for upload

    def addNewUser(self, **event_args):
        """
        Purpose: Validate user input and add a new user if all validations pass.
        Input: **event_args (dict) - event arguments.
        Process: Validate each input field and accumulate any issues.
        Output: None directly, calls a server function to add a user if validations pass.
        """
        issues = []  # Initialize issues list
        if not Validation.validateString(self.txtFullName.text):  # Validate full name
            issues.append("Invalid name")
        if not Validation.validateString(self.txtTitle.text):  # Validate title
            issues.append("Invalid title")
        if not Validation.validateEmail(self.txtEmail.text):  # Validate email
            issues.append("Invalid email")
        # Validate rates: additional rates > base rate, and base rate >= minimum wage
        if not Validation.validateRate(self.txtBaseRate.text, self.txtExtendedRate.text, self.txtPubHolRate.text):
            issues.append("Invalid rates")
        try:
          if not Validation.validateDate(self.dpDoB.date.strftime("%d/%m/%Y")) and not None:  # Validate date of birth
            issues.append("Invalid date of birth")
        except:
          issues.append("Invalid date of birth")
        if self.ddGender.selected_value is None:  # Validate gender selection
            issues.append("Invalid gender")
        if self.ddEmplType.selected_value is None:  # Validate employment type selection
            issues.append("Invalid employment type")
        if self.ddGroup.selected_value is None:  # Validate group selection
            issues.append("Invalid group selected")
        if not Validation.validatePhoneNum(self.txtPhoneNumber.text):  # Validate phone number
            issues.append("Invalid phone number")
        if not Validation.validateTFN(self.txtTFN.text):  # Validate TFN number
            issues.append("Invalid TFN number")
        if not Validation.validateUpload(self.flUpload.file):  # Validate file upload
            issues.append("Invalid file type uploaded")
        if len(self.txtTempPassword.text) < 8:  # Validate temporary password length
            issues.append("Invalid temporary password")
        if issues == [] or len(issues) == 0:  # Check if there are no validation issues
            # Confirm user details before proceeding
            if confirm("Please confirm that the following details are correct prior to continuing:\n" +
                       "Full Name: " + self.txtFullName.text + "\nEmail: " + self.txtEmail.text +
                       "\nPhone Number: " + self.txtPhoneNumber.text + "\nDate of birth: " + str(self.dpDoB.date) +
                       "\nGender: " + str(self.ddGender.selected_value) + "\nGroup: " + str(self.ddGroup.selected_value) +
                       "\nTitle: " + self.txtTitle.text + "\nBase Rate: " + self.txtBaseRate.text +
                       "\nExtended Rate: " + self.txtExtendedRate.text + "\nPublic Holiday Rate: " + self.txtPubHolRate.text +
                       "\nTFN: " + self.txtTFN.text):
                try:
                    # Call server function to add a new user
                    anvil.server.call('addNewuser', self.txtFullName.text, self.txtEmail.text, self.txtTempPassword.text,
                                      self.txtPhoneNumber.text, self.dpDoB.date, self.ddGender.selected_value,
                                      self.ddEmplType.selected_value, self.ddGroup.selected_value, self.txtTitle.text,
                                      float(self.txtBaseRate.text), float(self.txtExtendedRate.text), float(self.txtPubHolRate.text),
                                      self.txtTFN.text, self.flUpload.file)
                    self.imgUpload.source = None  # Clear image source
                    self.flUpload.clear()  # Clear file upload
                    self.txtTempPassword.text = ""  # Clear temporary password field
                    self.txtFullName.text = ""  # Clear full name field
                    self.txtEmail.text = ""  # Clear email field
                    self.txtPhoneNumber.text = ""  # Clear phone number field
                    self.txtBaseRate.text = ""  # Clear base rate field
                    self.txtExtendedRate.text = ""  # Clear extended rate field
                    self.txtPubHolRate.text = ""  # Clear public holiday rate field
                    self.txtTitle.text = ""  # Clear title field
                    self.txtTFN.text = ""  # Clear TFN field
                    self.ddEmplType.selected_value = None  # Clear employment type selection
                    self.ddGender.selected_value = None  # Clear gender selection
                    self.ddGroup.selected_value = None  # Clear group selection
                    self.dpDoB.date = None  # Clear date of birth field
                except Exception as e:
                    alert(f"An error occurred: {str(e)}")  # Alert user if an error occurs
                    self.txtEmail.text = ""  # Clear email field
        else:
            issueString = ""  # Initialize issue string
            n = 0  # Initialize issue count
            for issue in issues:  # Iterate over issues
                if n == 0:
                    issueString = "At least one of the entries is either blank or incorrectly filled out. Please try again. This includes: " + issue
                    n += 1
                else:
                    n += 1
                    if len(issues) == n:
                        issueString = issueString + ", and " + issue + "."
                    else:
                        issueString = issueString + ", " + issue
            alert(str(issueString))  # Alert user of issues

    def uploadProfile(self, **event_args):
        """
        Purpose: Upload a profile image and validate its format.
        Input: **event_args (dict) - event arguments.
        Process: Validate the uploaded file and display it if valid.
        Output: None
        """
        try:
            imgFile = self.flUpload.file  # Get uploaded file
            assert Validation.validateUpload(imgFile)  # Validate file format
            self.imgUpload.source = imgFile  # Set image source to the uploaded file
        except Exception as e:
            alert(f"The file that was uploaded doesn't match the required format. Please upload an image such as PNG or JPG. Error: {str(e)}")
            self.flUpload.clear()  # Clear file upload field if invalid
