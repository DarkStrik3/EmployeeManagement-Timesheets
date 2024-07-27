import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import re
from anvil.tables import app_tables
from datetime import datetime


class Validation:
    def validateString(name):  # Validate user name
        name = name.strip()  # Remove leading and trailing spaces
        try:
            assert name != ""  # Ensure name is not empty
            assert not name.isspace()  # Ensure name is not whitespace
            return True  # Return True if valid
        except:
            return False  # Return False if invalid

    @staticmethod
    def validateDate(date_str):  # Validate date
        dateFormatCode = "%d/%m/%Y"
        try:
            # Ensure date is not empty and has correct length
            assert date_str != "" and len(date_str) == 10
            # Parse date string to date object
            date_object = datetime.strptime(date_str, dateFormatCode)
            # Extract day, month, and year from date string
            day, month, year = map(int, date_str.split('/'))
            # Ensure day and month are within valid ranges
            assert 1 <= day <= 31 and 1 <= month <= 12
            # Ensure the date string reformatted matches original string
            reformatted_date = date_object.strftime(dateFormatCode)
            assert reformatted_date == date_str
            return True  # Return True if the date is valid
        except:
            return False  # Return False if the date is invalid

    def validateRate(baseRate, extendedRate, pubholrate):  # Validate rates
        try:
            baseRate = float(baseRate.strip())  # Convert base rate to float
            extendedRate = float(extendedRate.strip())  # Convert extended rate to float
            pubholrate = float(pubholrate.strip())  # Convert public holiday rate to float
            assert baseRate >= 20  # Ensure base rate is at least minimum wage
            assert extendedRate >= baseRate  # Ensure extended rate is greater than or equal to base rate
            assert pubholrate >= baseRate  # Ensure public holiday rate is greater than or equal to base rate
            return True  # Return True if rates are valid
        except:
            return False  # Return False if rates are invalid

    def validateEmail(email):  # Validate email
        try:
            email = email.strip()  # Remove leading and trailing spaces
            assert email != ""  # Ensure email is not empty
            assert email.count("@") == 1  # Ensure there is exactly one '@' symbol
            name, domain = email.split('@')  # Split the email into name and domain
            assert name != ""  # Ensure name part is not empty
            assert domain != ""  # Ensure domain part is not empty
            assert len(email) >= 3  # Ensure email has at least 3 characters
            assert re.match(r"[^@]+@[^@]+\.[^@]+", email)  # Ensure email matches the pattern
            return True  # Return True if email is valid
        except:
            return False  # Return False if email is invalid

    def validatePhoneNum(phoneNumber):  # Validate phone number
        try:
            assert len(phoneNumber) >= 10  # Ensure phone number is at least 10 characters long
            phonePattern = re.compile(r'^(\+?[1-9]\d{7,14}|0\d{9})$')  # Set required phone number pattern
            assert phonePattern.match(phoneNumber)  # Ensure phone number matches the pattern
            return True  # Return True if phone number is valid
        except:
            return False  # Return False if phone number is invalid

    def validateTFN(tfn):  # Validate TFN (Tax File Number)
        try:
            tfn = tfn.strip()  # Remove leading and trailing spaces
            assert len(tfn) in (8, 9)  # Ensure TFN length is either 8 or 9
            assert tfn.isdigit()  # Ensure TFN contains only digits
            return True  # Return True if TFN is valid
        except:
            return False  # Return False if TFN is invalid

    def validateUpload(imgFile):  # Validate image file upload
        try:
            assert imgFile is not None  # Ensure an image file is provided
            imgFileName = imgFile.name.lower()  # Get the file name and convert it to lower case
            validExtensions = ['.jpg', '.jpeg', '.png', 'webp']  # Set valid file extensions
            assert any(imgFileName.endswith(ext) for ext in validExtensions)  # Ensure the file has a valid extension
            return True  # Return True if the image file is valid
        except:
            return False  # Return False if the image file is invalid


class Other:
  def getDate15YearsAgo():  # Get the date 15 years ago from today
      current_date = datetime.now()
      try:
          date_15_years_ago = current_date.replace(year=current_date.year - 15)  # Calculate the date 15 years ago
      except ValueError:
          # Handle the case where the original date is Feb 29 and the target year is not a leap year
          date_15_years_ago = current_date.replace(month=2, day=28, year=current_date.year - 15)
      return date_15_years_ago.date()  # Return the date 15 years ago

  def QuickSort(array, key):  # QuickSort algorithm
      if len(array) <= 1:
          return array  # Base case: array with 0 or 1 element is already sorted
      else:
          pivot = array[len(array) // 2]  # Choose the pivot element
          left = [x for x in array if x[key] < pivot[key]]  # Elements less than the pivot
          middle = [x for x in array if x[key] == pivot[key]]  # Elements equal to the pivot
          right = [x for x in array if x[key] > pivot[key]]  # Elements greater than the pivot
          return Other.QuickSort(left, key) + middle + Other.QuickSort(right, key)  # Combine sorted sub-arrays


  def convertFloatToString(hoursFloat):
    # Convert the input hours to an integer number of hours, minutes, and seconds
    totalSeconds = int(hoursFloat * 3600)  # Total seconds
    hours = totalSeconds // 3600  # Calculate hours
    totalSeconds %= 3600  # Remaining seconds after hours are calculated
    minutes = totalSeconds // 60  # Calculate minutes
    seconds = totalSeconds % 60  # Remaining seconds after minutes are calculated
    
    # Return formatted string
    return f"{hours}h {minutes}m {seconds}s"