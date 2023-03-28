import mysql.connector
from mysql.connector import Error
import sys
import requests

# Define constants
HOST = ""
USER = ""
PASSWORD = ""
DATABASE = ""
APP_ID = ""
APP_KEY = ""
KG_TO_LB = 0.45359237
INCH_TO_CM = 2.54
ACTIVITY_LEVELS = {
    "sedentary": 1.25,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
}
DIETARY_RESTRICTIONS_DICT = {
    "vegetarian": 200,
    "vegan": 300,
    "gluten-free": 100
}

DIETARY_RESTRICTIONS_LIST = [
    "vegetarian",
    "vegan",
    "gluten-free"
]


def print_welcome_message():
    """
    Print a welcome message to the user.

    The function will print a message to welcome the user to the calories python calculator. 
    It will also provide some information about what the calculator does and what it will calculate.
    """
    print("Welcome to your calories python calculator!")
    print("Find out how many calories you should eat daily based on your BMR and activity level.")
    print("We will also calculate your body mass index (BMI) to give you an idea of your overall health.\n")


def get_gender():
    """
    Ask the user for their gender and return it.

    The function will prompt the user to enter their gender (male or female) and will return the value entered.
    If the user enters an invalid input, they will be prompted to try again until a valid input is provided.
    """
    while True:
        gender = input("Do you identify as male or female? ").lower()
        if gender in ["male", "female"]:
            return gender
        print("Invalid input. Please enter either 'male' or 'female'")


def get_weight():
    """
    Ask the user for their weight and return it in kilograms.

    The function will prompt the user to enter their weight in either kilograms or pounds.
    If kilograms is selected, the user will be prompted to enter their weight in kilograms and the value will be returned.
    If pounds is selected, the user will be prompted to enter their weight in pounds and the value will be converted to kilograms and returned.
    If an invalid input is entered, the user will be prompted to try again until a valid input is provided.
    """
    while True:
        weight_unit = input(
            "Would you like to enter your weight in kilograms or pounds? ").lower()
        if weight_unit == "kilograms":
            weight_kg = float(input("Enter your weight in kilograms: "))
            if weight_kg > 0:
                return weight_kg
        elif weight_unit == "pounds":
            weight_lb = float(input("Enter your weight in pounds: "))
            if weight_lb > 0:
                return weight_lb * KG_TO_LB
        print("Invalid input. Please enter either 'kilograms' or 'pounds'")


def get_height():
    """
    Ask the user for their height and return it in centimeters.

    The function will prompt the user to enter their height in either centimeters or feet/inches.
    If centimeters is selected, the user will be prompted to enter their height in centimeters and the value will be returned.
    If feet/inches is selected, the user will be prompted to enter their height in feet and inches and the value will be converted to centimeters and returned.
    If an invalid input is entered, the user will be prompted to try again until a valid input is provided.
    """
    while True:
        height_unit = input(
            "Would you like to enter your height in centimeters or feet/inches? ").lower()
        if height_unit == "centimeters":
            height_cm = float(input("Enter your height in centimeters: "))
            if height_cm > 0:
                return height_cm
        elif height_unit == "feet/inches":
            height_ft = int(input("Enter your height in feet: "))
            height_in = int(input("Enter your height in inches: "))
            if 0 < height_ft and 0 <= height_in < 12:
                return (height_ft * 12 + height_in) * INCH_TO_CM
        print("Invalid input. Please enter either 'centimeters' or 'feet/inches'")


def get_age():
    """
    Asks the user to input their age in years, validates the input and returns the age.

    Returns:
    int: The age of the user in years.
    """
    while True:
        age_yrs = int(input("Enter your age in years: "))
        if age_yrs > 0:
            return age_yrs
        print("Invalid input. Please enter your age in years: ")


def get_dietary_restrictions():
    """
    Asks the user to input any dietary restrictions or preferences they have. Validates the input
    and returns a list of dietary restrictions.

    Returns:
    list: A list of dietary restrictions entered by the user.
    """
    restrictions = []
    while True:
        restriction = input(
            "Do you have any dietary restrictions or preferences? (type 'done' when finished) ").lower()
        if restriction == 'done':
            return restrictions
        elif restriction in DIETARY_RESTRICTIONS_LIST:
            restrictions.append(restriction)
        else:
            print(
                "Invalid input. Please enter either 'vegetarian', 'vegan', 'gluten-free', or 'done'")
        return restrictions


def calculate_bmi(weight, height):
    """
    Calculates the BMI (Body Mass Index) based on the user's weight and height.

    Args:
    weight (float): The weight of the user in kilograms.
    height (float): The height of the user in centimeters.

    Returns:
    float: The BMI of the user rounded to one decimal place.
    """
    height_m = height / 100  # Convert height from cm to m
    return round(weight / (height_m ** 2), 1)


def get_weight_status(bmi):
    """
    Determines the weight status of the user based on their BMI and returns a message.

    Args:
    bmi (float): The BMI of the user.

    Returns:
    str: A message describing the weight status of the user based on their BMI.
    """
    if bmi < 18.5:
        message = """
Based on your daily calorie requirement, age, gender, and height, 
it appears that you are currently underweight in comparison to the average. 
This suggests that you may need to adjust your diet or exercise routine 
to achieve a healthier weight for your body type and overall well-being."""
    elif 18.5 <= bmi < 25:
        message = """
Based on your daily calorie requirement, age, gender, and height, 
it appears that you are currently at a healthy weight for your body type. 
It's important to maintain this weight through a balanced diet 
and regular physical activity to improve your overall well-being."""
    elif 25 <= bmi < 30:
        message = """
Based on your daily calorie needs, age, gender, and height, 
it appears that you are currently classified as overweight according to the average range. 
Being overweight can increase your risk of various health issues such as heart disease, 
diabetes, and certain types of cancer. It is important to maintain a healthy 
weight through a balanced diet and regular physical activity to reduce 
your risk of these health problems and improve your overall well-being."""
    else:
        message = """
Based on your daily calorie needs, age, gender, and height, 
it appears that you are currently classified as obese according to the average range. 
Obesity can increase your risk of various health issues such as heart disease, 
diabetes, and certain types of cancer. It is important to maintain a healthy 
weight through a balanced diet and regular physical activity to reduce 
your risk of these health problems and improve your overall well-being."""

    return message


def calculate_bmr(gender, weight, height, age):
    """
    Calculates the BMR (Basal Metabolic Rate) of the user based on their gender, weight, height and age.

    Args:
    gender (str): The gender of the user. Must be 'male' or 'female'.
    weight (float): The weight of the user in kilograms.
    height (float): The height of the user in centimeters.
    age (int): The age of the user in years.

    Returns:
    int: The BMR of the user in calories per day.
    """
    if gender == "female":
        return int(weight * 10 + height * 6.25 - age * 5 - 161)
    return int(weight * 10 + height * 6.25 - age * 5 + 5)


def get_user_goal():
    """
    Asks the user to input their goal for weight management (lose weight, maintain weight, or gain weight),
    validates the input and returns the goal.

    Returns:
    str: The user's goal for weight management.
    """
    while True:
        goal = input(
            "Do you want to lose weight, maintain weight, or gain weight? ").lower()
        if goal not in ["lose", "maintain", "gain"]:
            print("Invalid input. Please enter: 'lose', 'maintain', or 'gain'")
        else:
            return goal


def get_user_activity_level():
    """
    Asks the user to input their activity level, validates the input and returns the activity level.

    Returns:
    str: The user's activity level.
    """
    activity_levels = ACTIVITY_LEVELS
    while True:
        print("\nWhat is your activity level?")
        for level, value in activity_levels.items():
            print(f"{level.capitalize()} is {value}x BMR.")
        activity_level = input(
            "Please enter: 'sedentary', 'light', 'moderate', or 'active' ").lower()
        if activity_level not in activity_levels:
            print(
                "Invalid input. Please enter: 'sedentary', 'light', 'moderate', or 'active'")
        else:
            return activity_level


def total_calories_needed(rest_bmr):
    """
    Calculates and prints the total number of calories needed by a person based on their activity level and goal.

    Parameters:
    rest_bmr (int): The number of calories a person burns at rest.

    Returns:
    None
    """
    activity_level = get_user_activity_level()
    goal = get_user_goal()

    # Check for dietary restrictions
    restrictions = get_dietary_restrictions()
    calorie_adjustments = DIETARY_RESTRICTIONS_DICT
    total_adjustment = 0
    if any(r in DIETARY_RESTRICTIONS_LIST for r in restrictions):
        total_adjustment = sum([calorie_adjustments[r]
                               for r in restrictions if r in calorie_adjustments])

    # Calculate calorie needs and target calories
    calorie_needs = {
        "sedentary": get_calories(rest_bmr, 1.25),
        "light": get_calories(rest_bmr, 1.375),
        "moderate": get_calories(rest_bmr, 1.55),
        "active": get_calories(rest_bmr, 1.725),
    }
    target_calories = calculate_target_calories(
        calorie_needs[activity_level], goal)

    # Subtract calorie adjustments from the total
    total_calories = calorie_needs[activity_level] - total_adjustment
    if goal == 'maintain':
        print("To maintain weight, you should eat",
              total_calories, "calories a day.")
    else:
        print(
            f"You need to eat {calorie_needs[activity_level]} calories a day to maintain your current weight")
        if target_calories:
            print(
                f"To {goal} weight, you should eat {target_calories} calories a day.")
        else:
            print("Invalid goal. Please try again.")

    # Suggest healthy meals based on the goal
    if goal == "lose":
        suggest_healthy_meals("lose weight")
    elif goal == "gain":
        suggest_healthy_meals("gain weight")

    save_daily_calorie_needs(rest_bmr, calorie_needs, target_calories)
    compare_calories_to_average(target_calories)


def calculate_target_calories(base_calories, goal):
    """
    Calculates the target number of calories for a user based on their goal.

    Parameters:
    base_calories (int): The number of calories a person burns based on their activity level.
    goal (str): The goal of the user, either 'lose' or 'gain'.

    Returns:
    int: The target number of calories for the user.
    """
    goals = {"lose": 0.8, "gain": 1.2}
    return int(base_calories * goals.get(goal, 0))


def get_calories(rest_bmr, activity_level_factor):
    """
    Calculates the number of calories a person burns based on their BMR and activity level.

    Parameters:
    rest_bmr (int): The number of calories a person burns at rest.
    activity_level_factor (float): The activity level factor for a person based on their activity level.

    Returns:
    int: The number of calories a person burns based on their BMR and activity level.
    """
    return int(rest_bmr * activity_level_factor)


def suggest_healthy_meals(goal):
    """
    Suggests healthy meals to the user based on their goal.

    Parameters:
    goal (str): The goal of the user, either 'lose' or 'gain'.

    Returns:
    None
    """
    app_id = APP_ID
    app_key = APP_KEY
    if goal == "lose weight":
        query = "low-calorie"
    elif goal == "gain weight":
        query = "high-calorie"
    else:
        return
    url = f"https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={app_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        hits = data.get("hits")
        if hits:
            print("Here are some healthy meal suggestions:")
            for hit in hits[:5]:
                recipe = hit.get("recipe")
                print(recipe.get("label"))
                print(recipe.get("url"))
                print()
        else:
            print("No meal suggestions found.")
    else:
        print("Error retrieving meal suggestions.")


def save_daily_calorie_needs(rest_bmr, calorie_needs, target_calories, host, user, password, database):
    """
    Saves the user's daily calorie needs to the database.

    Args:
        rest_bmr (float): The user's resting metabolic rate.
        calorie_needs (dict): A dictionary containing the number of calories needed for different activity levels.
        target_calories (float): The user's target number of calories.
        host (str): The hostname of the MySQL server.
        user (str): The username to use to connect to the MySQL server.
        password (str): The password to use to connect to the MySQL server.
        database (str): The name of the MySQL database to use.

    Returns:
        None

    Raises:
        mysql.connector.Error: If there is an error when connecting to the MySQL server or executing the query.
    """
    query = "INSERT INTO calories_needs (rest_bmr, sedentary, light, moderate, active, target) VALUES (%s, %s, %s, %s, %s, %s)"
    data = (rest_bmr, calorie_needs["sedentary"], calorie_needs["light"],
            calorie_needs["moderate"], calorie_needs["active"], target_calories)

    try:
        with mysql.connector.connect(host=HOST, user=USER,
                                     password=PASSWORD,
                                     database=DATABASE) as conn, conn.cursor() as cursor:
            cursor.execute(query, data)
            conn.commit()
            print("Calorie needs saved successfully!")
    except mysql.connector.Error as e:
        print(e)


def get_calorie_needs_from_database(host, user, password, database):
    """
    Retrieves the user's daily calorie needs from the database.

    Args:
        host (str): The hostname of the MySQL server.
        user (str): The username to use to connect to the MySQL server.
        password (str): The password to use to connect to the MySQL server.
        database (str): The name of the MySQL database to use.

    Returns:
        None

    Raises:
        mysql.connector.Error: If there is an error when connecting to the MySQL server or executing the query.
    """
    query = "SELECT * FROM calories_needs"

    try:
        with mysql.connector.connect(host=HOST, user=USER,
                                     password=PASSWORD,
                                     database=DATABASE) as conn, conn.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            for record in records:
                print(record)
    except mysql.connector.Error as e:
        print(e)


def update_daily_calories_data(updated_data, host, user, password, database):
    """
    Updates the user's daily calorie needs in the database.

    Args:
        updated_data (float): The user's updated resting metabolic rate.
        host (str): The hostname of the MySQL server.
        user (str): The username to use to connect to the MySQL server.
        password (str): The password to use to connect to the MySQL server.
        database (str): The name of the MySQL database to use.

    Returns:
        None

    Raises:
        mysql.connector.Error: If there is an error when connecting to the MySQL server or executing the query.
    """
    query = "UPDATE calories_needs SET rest_bmr = %s WHERE id = %s"
    data = (updated_data, 1)  # assuming there is only one record in the table

    try:
        with mysql.connector.connect(host=HOST, user=USER,
                                     password=PASSWORD,
                                     database=DATABASE) as conn, conn.cursor() as cursor:
            cursor.execute(query, data)
            conn.commit()
            print("Data updated successfully!")
    except mysql.connector.Error as e:
        print(e)


def compare_calories_to_average(gender, height, age, daily_calories, host, user, password, database):
    """
    Compares the user's daily calorie needs to the average for their gender, height, and age.

    Args:
        gender (str): The user's gender.
        height (float): The user's height in meters.
        age (int): The user's age in years.
        daily_calories (float): The user's daily calorie needs.
        host (str): The hostname of the MySQL server.
        user (str): The username to use to connect to the MySQL server.
        password (str): The password to use to connect to the MySQL server.
        database (str): The name of the MySQL database to use.

    Returns:
        None

    Raises:
        mysql.connector.Error: If there is an error when connecting to the MySQL server.
    """
    try:
        with mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        ) as conn:
            if conn.is_connected():
                print('Connected to MySQL database')
                # do the rest of your work here
                update_daily_calories_data(
                    daily_calories, host, user, password, database)
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")


def main():
    """
    Runs the main program.

    Args:
        None

    Returns:
        None
    """
    print_welcome_message()
    gender = get_gender()
    weight = get_weight()
    height = get_height()
    age = get_age()
    rest_bmr = calculate_bmr(gender, weight, height, age)
    bmi = calculate_bmi(weight, height)
    print(f"Your BMI is {bmi}.")
    bmi_status = get_weight_status(bmi)
    print(bmi_status)
    calorie_needs, target_calories = total_calories_needed(rest_bmr)
    compare_calories_to_average(
        gender, age, height, total_calories_needed(rest_bmr))
    save_daily_calorie_needs(rest_bmr, calorie_needs, target_calories)
    update_daily_calories_data(rest_bmr)
    suggest_healthy_meals(calorie_needs)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)




