# Kimikim Organics Timesheets: Employee Management System

## Overview
This Employee Management System is designed to facilitate the management of employee details, timesheets, rates, and other related information. It includes validation methods to ensure the integrity of the data entered. For managers, they have the ability to approve work records, make changes to employee details, and view graphs in relation to employee performance.

## How to Test

### Employee Side
- Clock in, and clock out. The final clock-out time displayed initially may not be the same as the final time recorded in the database due to code processing time, with a difference of a few seconds, give or take.
- View 4 pending and 4 approved work records on the main page.
- View their profile with all their details displayed and view their own timesheets in a table format.
- Edit their profile except for company-sensitive details like their pay rate, title, and group (users can't promote themselves).
- Change the password in the settings page, also change dark mode.

### Manager Side

#### Employee Management
- Menu with buttons to all pages as a popup.
- Add a new user with all of their details and a temporary password.
- View all employees in a sorted fashion.
- Resort the employees based on their details.
- Filter the employees based on their details.
- Open an employee profile.
- Open the employee editing page.
- Archive a user (account becomes disabled, user shown as Not in Employment).

#### Timesheets
- View all timesheets and the user it is associated with (users are cached to reduce server load).
- Resort the timesheets based on the user details or the record's details.
- Filter the records based on group, gender, employment type, or date. Filtering by employee may come later.
- Filter by whether it is approved and/or paid.
- Approve either selected records (extra column) or all records.
- Reject either selected records or all records (for unapproved and unpaid, deletes the record).
- Mark selected records or all records as paid.

#### Analytics & Reporting
- Download all user details (except profile pictures) as a CSV file.
- Download all work records or time-filtered work records as a CSV file.
- View graphs displaying payout/time worked in comparison to either all groups, all employees, or the different employment types.
  - Pie graph showing breakdown.
  - Bar chart with total across the time.
  - Bar chart with dates across that time.
- View a table with employees, and choose what to view from their User ID, pay rate, balance (unpaid work records), etc.
  - WIP as more options are added to what to view, especially with balance.
- View total employees.
- View total payout across all employees (unpaid).
- View total time worked across all employees (unpaid).

#### Settings
- Change dark mode.
- Change password.

#### Home Page
- The logo returns to the first dashboard (employee management).
- The profile picture opens the manager's own profile.
- Sign out to return to the login page.

## Requirements
Any computer that can run applications within a browser. Not recommended on mobile due to aspect ratio, but still usable to an extent.

## Features
- **User Validation**: Validates user inputs such as names, dates, rates, emails, phone numbers, and TFNs.
- **File Uploads**: Ensures that uploaded image files meet specified criteria.
- **Graphs**: Provides graphs that reflect employee work.
- **Data display**: Displays user details in a repeating format while also allowing them to be opened in full-page.

## Analytics Page
The selections panel is responsible for changing all the graphs and data displayed beneath (total payout, time worked, and employees). The time-restrictive dropdown is also responsible for the filtered work record downloads. However, the bottom table is only controlled by the dropdown located above it. Its contents are all relevant records (i.e., all not yet paid records), and the other information is not time-sensitive.

## Unincluded Features
The following features were planned but not implemented due to time constraints, as the focus was on essential features:

- **No-ClockOut Notification**:  
  Requires a check across every row and concatenation into a single message while allowing the manager to see the exact rows highlighted in the Timesheets. Due to the additional Anvil functionality required, this feature was skipped.

- **Public Holiday Rate**:  
  A public holiday rate check in the clock-out logic was not implemented due to the unavailability of a reliable API for all Australian public holidays. Additionally, modifying the existing logic further risked breaking the functioning clock-out code.

- **Employee Repeating Panel**:  
  Initially intended to display up to 5 employees per row in the Employee Management dashboard. However, a single repeating panel was not supported. Implementing multiple repeating panels controlled through logic was time-consuming, so the implementation used a single repeating panel with one employee per row.

- **Popups**:  
  Many intended pop-ups are now standalone pages, as they are easier to program, and Anvil doesn't support large pop-ups like the proposed Add User and Edit User forms.

- **Sidebar Menu**:  
  Due to the use of Blank HTML, implementing a sidebar menu was not feasible. Instead, a popup with buttons is used to select the desired page.

- **Themes/Dark Mode**:  
  The default is dark mode. Although dark mode can be toggled in settings, switching to light mode is not yet enabled.

- **Login**:  
  The login page includes a button that opens Anvil's login form, as opposed to using textboxes as initially conceived.

- **Employee-side Work Record Viewing**:  
  Employees do not have an "extend" link at the bottom of the page to view more work records. Instead, they see only 4 records in each column.

## Classes and Methods (Functions Module)

### Validation Class
Contains methods to validate various types of input data.

- **validateString(name)**: Validates that a string is not empty or whitespace.
- **validateDate(date)**: Validates a date string in the format dd/mm/yyyy.
- **validateRate(baseRate, extendedRate, pubholrate)**: Validates that rates meet the specified conditions.
- **validateEmail(email)**: Validates the format of an email address.
- **validatePhoneNum(phoneNumber)**: Validates the format of a phone number.
- **validateTFN(tfn)**: Validates a Tax File Number (TFN).
- **validateUpload(imgFile)**: Validates an image file upload.

### Other Class
Provides additional utility methods, such as:

- **getDate15YearsAgo()**: Returns the date 15 years ago from today (to ensure only individuals who are at least 15 years old can be added as employees, in compliance with the law).
- **QuickSort(array, key)**: Implements the QuickSort algorithm for sorting an array of dictionaries based on a specified key.

## Manager Login
- **Email**: manager1@kimikim.com
- **Password**: 87654321

## Employee Login
- **Email**: employee1@gmail.com
- **Password**: 12345678

## Usage
- **Login**: Use the provided manager or employee login details to access the system.
- **Data Entry**: Enter employee details, rates, and other relevant information.
- **Validation**: Utilize the validation methods when adding or editing user details.
- **File Uploads**: Upload employee images and ensure they meet the specified criteria.
