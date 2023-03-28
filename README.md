# Calories Calculator
This is a Python program that calculates how many calories an individual should consume daily based on their BMR (basal metabolic rate) and activity level. It also calculates the individual's body mass index (BMI) and provides advice on how to maintain a healthy weight.

## Requirements
- Python 3.x
- MySQL
- The `mysql-connector-python` and `requests` libraries for Python.

## Installation and Setup
- Clone this repository to your local machine.
- Install Python 3.x on your machine if it is not already installed.
- Install MySQL on your machine if it is not already installed.
- Install the `mysql-connector-python` and `requests` libraries by running the following command in your terminal:
``` python
pip install mysql-connector-python requests
```
- Create a MySQL database and set the `HOST`, `USER`, `PASSWORD`, and `DATABASE` variables in the code to match your database settings.
- Obtain an `APP_ID` and `APP_KEY` from the [Nutritionix API](https://developer.nutritionix.com/) and set the `APP_ID` and `APP_KEY` variables in the code to your own API credentials.

## Usage
- To run the program, navigate to the directory where the program is saved in your terminal and run the following command:
``` python
python calories_calculator.py
```
- Follow the prompts to enter your gender, weight, height, age, activity level, and dietary restrictions. The program will then calculate your daily calorie requirements and BMI, and provide advice on maintaining a healthy weight.

## Contributing
This project is open to contributions. If you would like to contribute, please follow these steps:

- Fork the repository and clone it to your local machine.
- Create a new branch for your feature or bug fix.
- Write your code and commit your changes.
- Push your changes to your forked repository.
- Create a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the [LICENSE]() file for details...
