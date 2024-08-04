# Kimikim Organics Timesheets: Employee Management System

## Overview
This Employee Management System is designed to facilitate the management of employee details, timesheets, rates, and other related information. It includes validation methods to ensure the integrity of the data entered. For managers, they have the ability to approve work records, make changes to employee details, and view graphs in relation to employee performance.

## Requirements
- Any computer that can run applications within a browser. Not recommended on mobile due to aspect ratio, but still usable to an extent.

## Features
- **User Validation**: Validates user inputs such as names, dates, rates, emails, phone numbers, and TFNs.
- **File Uploads**: Ensures that uploaded image files meet specified criteria.
- **Graphs**: Provides graphs that are reflective of employee work.
- **Data display**: Displays user details in a repeating format, while also allowing them to be opened in full page.

## Analytics Page
The selections panel is responsible for changing all the graphs and data displayed beneath (total payout, time worked, and employees). The time-restrictive dropdown is also responsible for the filtered work record downloads. However, the bottom table is only controlled by the dropdown located above it. Its contents are all relevant records (i.e., all not yet paid records), and the other information is not time-sensitive.

## Unincluded Features
The following features were intended to be included but were omitted due to time limitations, prioritizing essential features:

- **No-ClockOut Notification**:  
  Since it requires a check that goes across every row and requires concatenation into a single message, while also allowing the manager to see the exact rows highlighted in the Timesheets. Due to the additional Anvil functionality that would have to be researched, I preferred to skip it.

- **Public Holiday Rate**:  
  I didn't implement a public holiday rate check into the clock-out logic that calculated the total payout because I couldn't find a decent API that would provide all the Australian public holidays. Additionally, I didn't want to complicate the logic further and risk breaking the existing clock-out code.

- **Employee Repeating Panel**:  
  Initially, I planned to have up to 5 employees per row in the Employee Management dashboard. However, after attempting to use just one repeating panel for it, I realized that it wasn't supported. Instead, I would have had to create multiple repeating panels controlled through logic rather than default settings. Due to time constraints, I opted for a single repeating panel with one employee per row.

- **Popups**:  
  Many of the "pop-ups" I initially wanted are now standalone pages. Not only are they easier to program, but Anvil doesn't support large pop-ups like the proposed Add User and Edit User forms.

- **Sidebar Menu**:  
  Since I chose to use a Blank HTML, I couldn't implement a sidebar menu. Instead, a popup with buttons selects the desired page.

- **Themes/Dark Mode**:  
  The default is dark mode. Although you can change dark mode in the settings, applying light mode/removing dark mode is not yet enabled.

- **Login**:  
  The login page features a button that opens up Anvil's login form, meaning it isn't through textboxes as previously conceived.

- **Employee-side Work Record Viewing**:  
  Employees didn't get the "extend" link at the bottom of the page to extend the number of work records they see. Instead, they only see 4 records in each column.

## Classes and Methods (of Functions Module)

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

- **getDate15YearsAgo()**: Returns the date 15 years ago from today (to ensure only individuals who are at least 15 years old can be added as employees, meeting legal requirements).
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
- **Validation**: Utilize the validation methods through adding a user or editing user details.
- **File Uploads**: Upload employee images and ensure they meet the specified criteria.
