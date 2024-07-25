Employee Management System
Overview
This Employee Management System is designed to facilitate the management of employee details, rates, and other related information. 
It includes validation methods to ensure the integrity of the data entered.

Features
User Validation: Validates user inputs such as names, dates, rates, emails, phone numbers, and TFNs.
File Uploads: Ensures that uploaded image files meet specified criteria.
Utility Methods: Provides additional functionalities such as date calculations and sorting algorithms.


Classes and Methods

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
Provides additional utility methods.

getDate15YearsAgo(): Returns the date 15 years ago from today.
QuickSort(array, key): Implements the QuickSort algorithm for sorting an array of dictionaries based on a specified key.
Manager Login
Email: manager1@kimikim.com
Password: 87654321
Employee Login
Email: employee1@kimikim.com
Password: 12345678
Usage
Login: Use the provided manager or employee login details to access the system.
Data Entry: Enter employee details, rates, and other relevant information.
Validation: Utilize the validation methods to ensure the integrity of the entered data.
File Uploads: Upload employee images and ensure they meet the specified criteria.
Additional Features: Use the utility methods for date calculations and sorting as needed.