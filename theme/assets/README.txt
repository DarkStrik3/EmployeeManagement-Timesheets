Kimikim Organics Timesheets: Employee Management System

  Overview
    This Employee Management System is designed to facilitate the management of employee details, timesheets, rates, and other related information. 
    It includes validation methods to ensure the integrity of the data entered.
    For managers, they have the ability to approve work records, make changes to employee details, and view graphs in relation to employee performance.

  How to Test:
    Employee Side:
      - Clock in, and clock out. Final clock out time dislayed initially would NOT be the same as final time recorded in the database due to code processing time. It is a difference of a few seconds give or take.
      - View 4 pending and 4 approved work records on the main page
      - View their profile with all their details displayed, and view their own timesheets in a table format.
      - Edit their profile except for company-sensitive details like their payrate, title and group (user cant promote themselves)
      - Change password in settings page, also change dark mode.
    Manager Side:
      Employee Management:
        - Add a new user with all of their details and a temporary password
        - View all employees in a sorted fashion
        - Resort the employees based on their details
        - Filter the employees based on their details
        - Open an employee Profile
        - Open the employee editing page
        - Archive a user (account becomes disabled, user shown as Not in Employment)
      Timesheets:
        - View all Timesheets, and the user it is associated to (users are cached to reduce server load)
        - Resort the timesheets based on the user details or the record's details itself\
        - Filter the records based on Group, gender, employment type, or date. Filter by employee might come later.
        - Filter by whether it is approved, and/or paid
        - Approve either selected records (extra column) or all records
        - Reject either selected records or all records (on unnapporved and unpaid, deletes the record)
        - Mark selected records or all records as paid
      Analytics & Reporting:
       - Download all User Details (except profile picture) as a CSV file
       - Download all work records or time-filtered work records as a CSV file
       - View Graphs displaying payout/time worked in comparison to either all groups, all employees or the different employment types
        - Pie graph showing breakdown
        - Bar chart with total across the time
        - Bar chart with dates across that time
       - View a table with employees, and you can choose what to view from their User ID, payrate, balance (unpaid work records), etc. 
        - WIP as more options into what to view, especiall to the with balance.
       - View total employees
       - View total payout across all employees (unpaid)
       - View total time worked across all employees (unpaid)
      Settings:
       - Change dark mode
       - Change password
      Home Page:
       - Logo 
      
      

  Requirements:
    Any computer that can run applications within a browser. Not recommended on Mobile due to aspect ratio, but still usable to an extent.
  
  Features
    User Validation: Validates user inputs such as names, dates, rates, emails, phone numbers, and TFNs.
    File Uploads: Ensures that uploaded image files meet specified criteria.
    Graphs: Provides graphs that are reflective of employee work.
    Data display: Displays user details in a repeating format, while also allowing them to be opened in full page.

  Analytics Page:
    The selections panel is responsible for changing the all the graphs and data displayed beneath (total payout, time worked, and employees). The time-restrictive dropdown is also responsible for the filtered work record downloads.
    However, the bottom table is only controlled by the dropdown located above it. Its contents are all relevent records (i.e. all not yet paid records), and the other information is not time sensitive.

  Unincluded Features
    The following features are ones that I was going to include, but was unable to due to time limitation, instead preferring to focus on essential features.
    No-ClockOut Notification:
      Since it requires a check that goes across every row and requires concatination into a single message, while also allowing the manager to see the exact rows highlighted in the Timesheets. Due to the additional Anvil functionality that
      would have to be researched, I preferred to skip it.
    Public Holiday Rate: 
      I didn't end up implementing a public holiday rate check into the clock-out logic that calculated the total payout. This is because I couldn't find a decent API that would give me all the Australian public holidays.
      Furthermore, I didn't want to mess with the logic any further since I didn't want to break anything that was already working in the clock out code.
    Employee Repeating Panel:
      Initially, I was planning to have up to 5 employees per row in the Employee Management dashboard, however after attempting to use just 1 repeating panel for it, I realised that it simply wasn't supported. 
      Instead, I would have to create multiple repeating panels that would be controlled through the logic, rather than by the default settings. I didn't have enough time to make this work,
      so instead I just had 1 repeating panel with 1 employee per row.
    Popups:
      Quite a few of the "pop-ups" I wanted previously are now just their own pages. Not only they are easier to program, but Anvil doesn't support such large popups like the proposed Add User and Edit User forms.
    Sidebar Menu:
      Since I chose to use a Blank HTML, unfortunately I am unable to implement a sidebar menu as the only way to do so is to use a Material Design. Instead there is a popup with buttons to select desired page.
    Themes/Dark Mode:
      I ended up making the default be dark mode. Although you can change dark mode in the settings, applying light mode/removing dark mode is not yet enabled.
    Login:
      The login page features a button that opens up Anvil's login form, meaning that it isn't through textboxes like previously concieved.
    Employee-side work record viewing:
      Employees didn't end up getting the "extend" link at the bottom of the page to extend the amount of work records they see. Instead, they see only 4 in each column.

  Classes and Methods (of Functions module)
  
    Validation Class
      Contains methods to validate various types of input data.
      
      validateString(name): Validates that a string is not empty or whitespace.
      validateDate(date): Validates a date string in the format dd/mm/yyyy.
      validateRate(baseRate, extendedRate, pubholrate): Validates that rates meet the specified conditions.
      validateEmail(email): Validates the format of an email address.
      validatePhoneNum(phoneNumber): Validates the format of a phone number.
      validateTFN(tfn): Validates a Tax File Number (TFN).
      validateUpload(imgFile): Validates an image file upload.
    Other Class
    Provides additional utility methods, such as:
      getDate15YearsAgo(): Returns the date 15 years ago from today (to make sure only people who are at least 15 years old can be added as employees to meet the law).
      QuickSort(array, key): Implements the QuickSort algorithm for sorting an array of dictionaries based on a specified key.


  Manager Login
    Email: manager1@kimikim.com
    Password: 87654321
  Employee Login
    Email: employee1@gmail.com
    Password: 12345678

    
  Usage
    Login: Use the provided manager or employee login details to access the system.
    Data Entry: Enter employee details, rates, and other relevant information.
    Validation: Utilize the validation methods through adding a user or editing user details.
    File Uploads: Upload employee images and ensure they meet the specified criteria.