import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def Authenticate(username, password):
  try:
    existingUsername = app

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