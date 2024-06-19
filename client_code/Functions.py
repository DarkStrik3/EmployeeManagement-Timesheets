import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import re
from anvil.tables import app_tables
from datetime import datetime


class Validation:


  def validateString(name): # the user name is validated
    name = name.strip() # remove leading and following spaces
    try: # attempts to test the name
        assert name != "" # makes sure it isn't blank
        if not name: # makes sure it isn't noneType, double-checking
          raise TypeError # error raised if it fails this part
        assert not name.isspace()  # Ensure name is not empty or whitespace
        return True # if it passes all the tests, True is returned
    except: # an error arises throughout the test, 'try' block is ended
        return False # False is returned

  def validateDate(date):  # The inputted date is validated
    dateFormatCode = "%Y-%m-%d"
    try:  # Attempt to validate the date format and contents
        # Ensure the inputted date isn't blank and has the correct length
        assert date != "" and len(date) == 10
        # Attempt to parse the date string to a date object
        date_object = datetime.strptime(date, dateFormatCode)
        # Reformat the date to ensure it matches the required format
        reformatted_date = date_object.strftime(dateFormatCode)
        # Additional check to ensure the day and month are within valid ranges
        year, month, day = map(int, date.split('-'))
        assert 1 <= day <= 31 and 1 <= month <= 12
        return True  # The date is in the correct format and has valid values, True is returned
    except:  # If any error arises throughout the 'try' block
        # If parsing or formatting fails, it's not a valid date
        return False  # False is returned since it doesn't meet the required format
  
  def validateRate(baseRate, extendedRate, pubholrate):
    try:
      baseRate = float(baseRate.strip())
      extendedRate = float(extendedRate.strip())
      pubholrate = float(pubholrate.strip())
      assert baseRate >= 20 # make sure that the base rate is at least minimum wage
      assert extendedRate >= baseRate # make sure that the rate at which an employee earns extra is actually more than or equal to the base rate
      assert pubholrate >= baseRate # make sure that the rate at which an employee earns extra is actually more than or equal to the base rate
      return True # everything is ok with the rates, good to go
    except:
      return False # something went wrong, error message will ensue
  
  def validateEmail(email):
    try:
      email = email.strip()
      assert email != "" # makes sure email isnt a blank value
      assert email.count("@") == 1 # makes sure there is at least 1 @ symbol, but only 1
      name, domain = email.split('@') # splits the email into 2 parts, split at the @ symbol but not including it
      # make sure that they both exist: the @ symbol isnt at begginning or end
      assert name != "" 
      assert domain != ""
      assert len(email) >= 3 # make sure that there is at least 1 character in front and 1 character behind 
      assert re.match(r"[^@]+@[^@]+\.[^@]+", email) # make sure that there arent any symbols in the email that shouldn't be there
      return True # true is returned
    except: # an assertion doesnt work, meaning that the email isnt valid
      return False # false is returned
  
  def validatePhoneNum(phoneNumber):
    try:
      assert len(phoneNumber) >= 10 # Ensure the phone number is at least 10 characters long
      phonePattern = re.compile(r'^(\+?[1-9]\d{7,14}|0\d{9})$') # Sets required phone number pattern
      assert phonePattern.match(phoneNumber) # Ensure the phone number matches the pattern
      return True # Returns true if everything is ok
    except: # something doesn't match the required format/length
      return False # False is returned
  
  def validateTFN(tfn):
    try:
      tfn = tfn.strip()
      assert len(tfn) == 8 or 9
      assert tfn.isdigit()
      return True
    except:
      return False


  def validateUpload(imgFile):
    try:
      assert imgFile is not None
      imgFileName = imgFile.name.lower()
      validExtensions = ['.jpg', '.jpeg', '.png', 'webp']
      assert any(imgFileName.endswith(ext) for ext in validExtensions)
      return True
    except:
      return False

class Other:

  
  def getDate15YearsAgo():
    current_date = datetime.now()
    try:
      date_15_years_ago = current_date.replace(year=current_date.year - 15)
    except ValueError:
      # This handles the case where the original date is Feb 29 and the target year is not a leap year.
      date_15_years_ago = current_date.replace(month=2, day=28, year=current_date.year - 15)
    return date_15_years_ago.date()
    



  