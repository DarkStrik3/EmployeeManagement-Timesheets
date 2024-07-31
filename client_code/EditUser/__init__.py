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
    def __init__(self, employeeID, p_parent, isManager, **properties):
        """
        Purpose: Initialize the EditUser form with default properties.
        Input: employeeID (str) - the ID of the employee to edit.
               p_parent (Form) - parent form.
               **properties (dict) - additional properties.
        Process: Sets form components, binds data, and retrieves initial data from the server.
        Output: None
        """
        self.init_components(**properties)  # Initialize form components with properties
        self.dpDoB.max_date = Other.getDate15YearsAgo()  # Ensure the worker is at least 15 years old
        self.dpDoB.format = "%d/%m/%Y"
        self.flUpload.file_types = [".jpg", ".jpeg", ".png", "webp"]  # Set allowed file types for upload
        self.employeeId = employeeID
        self._parent = p_parent
        # Sets all pre-existing data into the required inputs
        userRow = anvil.server.call('getUserInfo', employeeID)
        if not isManager:
            self.txtBaseRate.enabled = False
            self.txtExtendedRate.enabled = False
            self.txtPubHolRate.enabled = False
            self.ddEmplType.enabled = False
            self.ddGroup.enabled = False
            self.txtTitle.enabled = False
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
        """
        Purpose: Validate and edit user details.
        Input: **event_args (dict) - event arguments.
        Process: Validates user inputs, confirms changes with the user, and updates user details on the server.
        Output: None
        """
        issues = []
        if not Validation.validateString(self.txtFullName.text):  # Validate full name
            issues.append("invalid name")
        if not Validation.validateString(self.txtTitle.text):  # Validate title
            issues.append("invalid title")
        if not Validation.validateEmail(self.txtEmail.text):  # Validate email
            issues.append("invalid email")
        # Validate rates
        if not Validation.validateRate(self.txtBaseRate.text, self.txtExtendedRate.text, self.txtPubHolRate.text):
            issues.append("invalid rates")
        # Validate date of birth
        if not Validation.validateDate(self.dpDoB.date.strftime("%d/%m/%Y")):
            issues.append("invalid date of birth")
        # Validate gender selection
        if self.ddGender.selected_value is None:
            issues.append("invalid gender")
        # Validate employment type selection
        if self.ddEmplType.selected_value is None:
            issues.append("invalid employment type")
        # Validate group selection
        if self.ddGroup.selected_value is None:
            issues.append("invalid group selected")
        # Validate phone number
        if not Validation.validatePhoneNum(self.txtPhoneNumber.text):
            issues.append("invalid phone number")
        # Validate TFN
        if not Validation.validateTFN(self.txtTFN.text):
            issues.append("invalid TFN number")
        # Validate file upload
        if not Validation.validateUpload(self.imgUpload.source):
            issues.append("invalid file type uploaded")

        if issues == [] or len(issues) == 0:
            # Confirm details with the user
            if confirm(
                "Please confirm that the following details are correct prior to continuing:\n"
                + "Full Name: " + self.txtFullName.text
                + "\nEmail: " + self.txtEmail.text
                + "\nPhone Number: " + self.txtPhoneNumber.text
                + "\nDate of birth: " + str(self.dpDoB.date)
                + "\nGender: " + str(self.ddGender.selected_value)
                + "\nGroup: " + str(self.ddGroup.selected_value)
                + "\nTitle: " + self.txtTitle.text
                + "\nBase Rate: " + self.txtBaseRate.text
                + "\nExtendedRate: " + self.txtExtendedRate.text
                + "\nPublic Holiday Rate: " + self.txtPubHolRate.text
                + "\nTFN: " + self.txtTFN.text
            ):
                try:
                    # Check if a new file is uploaded, otherwise use the existing image
                    if self.flUpload.file is None:
                        image = self.imgUpload.source
                    else:
                        image = self.flUpload.file

                    # Call the server to edit user details
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
                        image
                    )

                    # Reset form fields
                    self.imgUpload.source = None
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
                    self.flUpload.clear()
                except Exception as e:
                    alert(f"An error occurred: {str(e)}")
                    self.txtEmail.text = ""
                
                # Confirm if user wants to view the profile
                if confirm("Would you like to view this profile?"):
                    self._parent.openProfileUserDetails(self.employeeId)
        else:
            # Concatenate issues into a single string for alert
            issueString = "At least one of the entries is either blank or incorrectly filled out. Please try again. This includes: "
            issueString += ", ".join(issues[:-1]) + ", and " + issues[-1] + "." if len(issues) > 1 else issues[0] + "."
            alert(issueString)

    def uploadProfile(self, **event_args):
        """
        Purpose: Upload a profile image.
        Input: **event_args (dict) - event arguments.
        Process: Validates and sets the uploaded image as the profile image.
        Output: None
        """
        try:
            imgFile = self.flUpload.file
            assert Validation.validateUpload(imgFile)  # Validate the uploaded file
            self.imgUpload.source = imgFile  # Set the profile image source
        except Exception as e:
            alert(f"The file that was uploaded doesn't match the required format. Please upload an image such as PNG or JPG. Error: {str(e)}")
            self.flUpload.clear()  # Clear the file upload input
