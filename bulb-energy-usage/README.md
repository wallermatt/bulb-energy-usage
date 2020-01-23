Matthew Waller 

Installation
============

pip install -r requirements.txt

(I installed one extra module - python-dateutil)


Changes
=======
I modified the call for calculate_bill so that as per the instructions the only
optional argument is account, and it is the right-most argument. Because of 
this I also had to change the call for this function in calculate_and_print_bill.


Further work
============

If I had more time I would:

1. Create custom exceptions where exceptions are raised by my code.
2. Explicitly reference these custom exceptions in the tests.
3. Write tests for gas as well as electricity.
4. Write tests for more edge cases.
5. Store readings in a dictionary with reading_date as the key
   (rather than the list they're stored in at the moment)







Original Instructions
=====================

For this challenge you CANNOT edit the following files which are provided to you.

readings.json
You can add files to your submission, but if you edit any of the provided files, other than those specified, your changes will be IGNORED.

Please read these instructions carefully before starting to code:
When you assemble your code challenge solution for submission please create it as a ZIP file.
Please do NOT include generated files in your submitted solution.
Your ZIP upload will be cleaned to remove ignored (e.g. generated) files.
Files will be removed and ignored based on standard gitignore files as specified in this GitHub project: github/gitignore.
When you upload your code, you will be shown which files are accepted for code review and which will be ignored.
The ignored files will NOT be provided to the reviewer.
Create your solution WITHIN the structure of the starting ZIP file that you have downloaded.
When you are ready to upload your code, you can re-ZIP from the starting top-level directory and upload the entire ZIP by clicking the UPLOAD SOLUTION button below.

Overview
Thank you for interviewing at Bulb and taking the time to complete this coding exercise.

We expect the challenge to take around 3-4 hours, however feel free to take as long as you need. If you run out of time, that’s fine, just send us a README with the details of what you planned to include in your implementation.

Please approach this as you would a production problem with respect to quality and consider that we will ask you to extend your work in a pairing exercise as part of the technical interview.

The instructions are duplicated in the README.md file in the starting code ZIP file that should download.

In this challenge, we’d like you to write a small program which, given a set of meter readings, computes a member’s monthly energy bill. To do this, we have stubbed out the following files for you:

bill_member.py, which contains functions to compute the customer bill and print it to screen.
You should implement calculate_bill. This is the entry point to your solution.
calculate_bill is currently hardcoded to give the correct answer for August 2017.
There’s no need to change calculate_and_print_bill.
test_bill_member.py, a test module for bill_member.
main.py, the entry point for the program, there’s no need to make changes to this module.
tariff.py, prices by kWh for all energy
load_readings.py, provides a function for loading the readings from the given json.
readings.json, contains a set of monthly meter readings for a given year, member and fuel
We’d like you to:

Implement the calculate_bill function, so that given a member_id, optional account argument and billing date, we can compute the bill for the customer.
We do not want you to spend time on:

Making this backwards compatible with python <= 3.
You can assume:

All times are UTC.
We’re only dealing with £ denominated billing.
You only need to handle electricity and gas billing.
Energy is consumed linearly.
The billing date is the last day of the month.
Readings are always taken at midnight.
There is only one meter reading per billing period.
The JSON file structure will remain the same in any follow on exercise.