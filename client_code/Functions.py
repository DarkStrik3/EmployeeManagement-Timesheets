import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import re
from anvil.tables import app_tables
from datetime import datetime
from anvil import get_open_form

class Validation:
    @staticmethod
    def validateString(name):  
        """
        Purpose: Validate the user name to ensure it's not empty or just whitespace.
        Input: 
            name (str) - The name to validate.
        Process: 
            - Strips leading and trailing spaces.
            - Checks that the name is not empty and not None.
        Output: 
            True if the name is valid, otherwise False.
        """
        name = name.strip()  # Remove leading and trailing spaces
        try:  
            assert name != ""  # Ensure name is not empty or whitespace
            if not name:  
                raise TypeError  # Raise error if the name is None or invalid
            return True  
        except:  
            return False  

    @staticmethod
    def validateDate(date_str):  
        """
        Purpose: Validate the date string format and content.
        Input: 
            date_str (str) - The date string in 'dd/mm/yyyy' format.
        Process: 
            - Ensures the date string is not empty and is of the correct length.
            - Parses the date string to a date object.
            - Checks day and month are within valid ranges and reformats the date to verify correctness.
        Output: 
            True if the date is valid, otherwise False.
        """
        dateFormatCode = "%d/%m/%Y"
        try:
            assert date_str != "" and len(date_str) == 10  # Ensure date is of correct length
            date_object = datetime.strptime(date_str, dateFormatCode)  # Parse date string
            day, month, year = map(int, date_str.split('/'))  # Extract day, month, year
            assert 1 <= day <= 31 and 1 <= month <= 12  # Validate day and month ranges
            reformatted_date = date_object.strftime(dateFormatCode)  # Reformat date to verify
            assert reformatted_date == date_str
            return True  
        except:
            return False  

    @staticmethod
    def validateRate(baseRate, extendedRate, pubholrate):  
        """
        Purpose: Validate wage rates to ensure they meet minimum and logical conditions.
        Input: 
            baseRate (str) - Base wage rate.
            extendedRate (str) - Extended wage rate.
            pubholrate (str) - Public holiday wage rate.
        Process: 
            - Converts rates to float.
            - Ensures base rate is at least the minimum wage.
            - Checks that extended and public holiday rates are not less than the base rate.
        Output: 
            True if all rates are valid, otherwise False.
        """
        try:
            baseRate = float(baseRate.strip())
            extendedRate = float(extendedRate.strip())
            pubholrate = float(pubholrate.strip())
            assert baseRate >= 20  # Minimum wage check
            assert extendedRate >= baseRate  # Extended rate check
            assert pubholrate >= baseRate  # Public holiday rate check
            return True  
        except:
            return False  

    @staticmethod
    def validateEmail(email):  
        """
        Purpose: Validate the email format.
        Input: 
            email (str) - The email address to validate.
        Process: 
            - Strips leading and trailing spaces.
            - Ensures the email has exactly one '@' symbol.
            - Validates the format using a regular expression.
        Output: 
            True if the email is valid, otherwise False.
        """
        try:
            email = email.strip()
            assert email != ""  
            assert email.count("@") == 1  # Ensure there is exactly one '@'
            name, domain = email.split('@')  
            assert name != ""  
            assert domain != ""  
            assert len(email) >= 3  # Email length check
            assert re.match(r"[^@]+@[^@]+\.[^@]+", email)  # Regex for valid email format
            return True  
        except:  
            return False  

    @staticmethod
    def validatePhoneNum(phoneNumber):  
        """
        Purpose: Validate the phone number format.
        Input: 
            phoneNumber (str) - The phone number to validate.
        Process: 
            - Ensures the phone number is at least 10 characters long.
            - Validates the number against a regular expression pattern.
        Output: 
            True if the phone number is valid, otherwise False.
        """
        try:
            assert len(phoneNumber) >= 10  # Length check
            phonePattern = re.compile(r'^(\+?[1-9]\d{7,14}|0\d{9})$')  # Phone number pattern
            assert phonePattern.match(phoneNumber)  # Validate phone number format
            return True  
        except:  
            return False  

    @staticmethod
    def validateTFN(tfn):  
        """
        Purpose: Validate the Tax File Number (TFN).
        Input: 
            tfn (str) - The TFN to validate.
        Process: 
            - Strips leading and trailing spaces.
            - Ensures TFN length is 8 or 9 and contains only digits.
        Output: 
            True if the TFN is valid, otherwise False.
        """
        try:
            tfn = tfn.strip()
            assert len(tfn) == 8 or len(tfn) == 9  # Length check
            assert tfn.isdigit()  # Ensure TFN is numeric
            return True  
        except:  
            return False  

    @staticmethod
    def validateUpload(imgFile):  
        """
        Purpose: Validate the image file upload.
        Input: 
            imgFile (object) - The image file to validate.
        Process: 
            - Ensures the image file is not None.
            - Validates the file extension.
        Output: 
            True if the file is valid, otherwise False.
        """
        try:
            assert imgFile is not None  
            imgFileName = imgFile.name.lower()  
            validExtensions = ['.jpg', '.jpeg', '.png', '.webp']  
            assert any(imgFileName.endswith(ext) for ext in validExtensions)  
            return True  
        except:  
            return False  

class Other:
    @staticmethod
    def getDate15YearsAgo():  
        """
        Purpose: Get the date that was 15 years ago from today.
        Input: None
        Process: 
            - Calculates the date 15 years ago.
            - Handles leap year issues by setting to Feb 28 if necessary.
        Output: 
            The date 15 years ago.
        """
        current_date = datetime.now()
        try:
            date_15_years_ago = current_date.replace(year=current_date.year - 15)
        except ValueError:
            # Handle leap year issue
            date_15_years_ago = current_date.replace(month=2, day=28, year=current_date.year - 15)
        return date_15_years_ago.date()

    @staticmethod
    def QuickSort(array, key):  
        """
        Purpose: Perform a quick sort on a list of dictionaries based on a specified key.
        Input: 
            array (list) - List of dictionaries to sort.
            key (str) - The key to sort by.
        Process: 
            - Recursive sorting by pivot element.
        Output: 
            Sorted list of dictionaries.
        """
        if len(array) <= 1:
            return array
        else:
            pivot = array[len(array) // 2]
            left = [x for x in array if x[key] < pivot[key]]
            middle = [x for x in array if x[key] == pivot[key]]
            right = [x for x in array if x[key] > pivot[key]]
            return Other.QuickSort(left, key) + middle + Other.QuickSort(right, key)

    @staticmethod
    def convertFloatToString(hours_float):
        """
        Purpose: Convert a float representing hours into a formatted string of hours, minutes, and seconds.
        Input: 
            hours_float (float) - The number of hours as a float.
        Process: 
            - Converts float to total seconds.
            - Calculates hours, minutes, and seconds.
            - Formats and returns the result.
        Output: 
            Formatted string showing hours, minutes, and seconds.
        """
        total_seconds = int(hours_float * 3600)  # Convert hours to total seconds
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        result = f"{hours}h {minutes}m {seconds}s"
        return result
