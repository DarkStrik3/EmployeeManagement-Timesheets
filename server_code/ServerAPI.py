import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

#
@anvil.server.callable
def Authenticate(inputEmail, password):
  try:
    existingRow = app_tables.tblauthentication.get(Email=inputEmail)
    if existingRow['Password'] == password:
      return existingRow['AuthenticationID']
  except:
    return "404"

@anvil.server.callable
def getRefresh(userIdentification):
  db = app_tables.tbltimesheets.search(UserID=userIdentification)
  return db

@anvil.server.callable
def getUserID(name):
  row = app_tables.tblusers.get(Username=name)
  return row[0]

@anvil.server.callable
def getLoginExists(username, pwd):
  return True