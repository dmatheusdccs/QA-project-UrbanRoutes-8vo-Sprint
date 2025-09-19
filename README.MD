# QA Urban Routes
---
![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Selenium](https://img.shields.io/badge/Selenium-4.x-orange.svg) ![Chrome](https://img.shields.io/badge/Chrome-Driver-green.svg) ![PyTest](https://img.shields.io/badge/PyTest-v6.2.x-blueviolet.svg)

---
## Project Overview

This project is an automation script built using **Selenium** and **Python** for testing the **Urban Routes** web application. The main goal of this project is to automate the process of making a ride request through the platform, ensuring that all essential steps are correctly validated.

### Project Overview

Urban Routes is a web application that provides a taxi or transport service to the user. It offers three specific travel modes, each with unique request options tied to the transportation type chosen by the user. Additionally, the application includes market-specific amenities, such as the option to have a quiet ride or even receive a delicious ice cream during the trip.

The objective of the test automation is to simulate the following core user journey:

1. Configuring the ride's **from** and **to** addresses.
2. Selecting the **Comfort** ride option.
3. Filling in the user's **phone number**.
4. Adding a **credit card** as the payment method.
5. Writing a **message for the driver**.
6. Requesting a **blanket and tissues**.
7. Ordering **2 ice creams**.
8. Triggering the **taxi request modal**.

### Badges

- **Python:** The primary programming language for the automation script.
- **Selenium:** The framework used for web automation.
- **PyTest:** The testing framework used for running tests and validating the requests.

## Project Structure
urban_routes_project/
├── src/
│ ├── test_urban_routes.py # Contains the test scripts for the Urban Routes app
├── helpers/
│ ├── helpers.py # Helper functions, including phone code retrieval
├── data/
│ ├── data.py # Data file containing test URLs, phone numbers, and other variables
├── requirements.txt # List of required Python packages
└── README.md # This file

- **`src/test_urban_routes.py`:** Contains the main test cases that automate the ride request process using Selenium and Python.
- **`helpers/helpers.py`:** Contains utility functions, including code for retrieving phone confirmation codes.
- **`data/data.py`:** Holds configuration data such as the URL, addresses, and other test values.

## Installation

To get started with this project, follow the steps below:

1. **Clone the repository:**
   ```
   git clone <your-repo-url>
   cd urban_routes_project
`

Install dependencies:
This project uses Python 3. Make sure you have Python installed. Then install the required dependencies:

pip install -r requirements.txt

Running Tests
Run all tests:
To run the entire test suite, use the following command:


pytest -q
Run a specific test file:
If you want to run a specific test file, use:


pytest -q src/test_urban_routes.py

Generate a coverage report:
You can generate a coverage report by using the following command:


pytest --cov=src tests/

Test Cases Overview
The following test cases are implemented to simulate the user journey:

1. test_set_route: Tests the ability to configure the 'from' and 'to' addresses for the ride request.
2. test_set_conf_taxi_request: Validates the selection of the Comfort travel mode.
3. test_add_phone_number: Verifies that the phone number is correctly entered and validated.
4. test_add_payment_method: Tests adding a credit card to the payment method.
5. test_driver_comment: Simulates writing a message for the driver.
6. test_manta_request: Checks if the user can request a blanket and tissues.
7. test_ice_cream_request: Tests the ability to request 2 ice creams.
8. test_wait_for_taxi_modal: Validates the appearance of the modal to search for a taxi after all inputs are made.

Helpers
The project contains helper functions in the helpers/helpers.py file that assist in specific tasks, such as retrieving the phone confirmation code.

Example of Helper Function (helpers/helpers.py):
```
import time
import json
from selenium.common import WebDriverException

def retrieve_phone_code(driver) -> str:
    """This function retrieves the phone confirmation code and returns it as a string."""
    code = None
    for _ in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') 
            if log.get("message") and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No phone confirmation code found. Use this function only after requesting the code in the app.")
        return code
```
Dependencies
This project relies on the following Python packages:

Selenium: For web automation.
PyTest: To run tests and validate the automation.
WebDriver: To use ChromeDriver for Selenium tests.
You can install these dependencies using:

pip install selenium pytest

requirements.txt
###### selenium==4.0.0
###### pytest==6.2.5
---


Conclusion:
This project automates the process of requesting a ride via the Urban Routes application. By leveraging Selenium and Python, we ensure that all essential functionalities, such as ride configuration, phone number validation, and payment method setup, work as expected. Each step is verified with automated tests that ensure reliability and maintainability of the system.
