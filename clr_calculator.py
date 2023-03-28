import mysql.connector
from mysql.connector import Error

def main():
    print_welcome_message()
    gender = get_gender()
    weight = get_weight()
    height = get_height()
    age = get_age()
    rest_bmr = calculate_bmr(gender, weight, height, age)
    bmi = calculate_bmi(weight, height)
    print(f"Your BMI is {bmi}.")
    calorie_needs, target_calories = total_calories_needed(rest_bmr)
    save_daily_calorie_needs(rest_bmr, calorie_needs, target_calories)
    update_the_daily_calories_data(rest_bmr)
    suggest_healthy_meals(calorie_needs)


def save_daily_calorie_needs(rest_bmr, calorie_needs, target_calories):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="",
            password="",
            database="daily_calories"
        )
        if conn.is_connected():
            cursor = conn.cursor()
            # Insert the data into the table
            query = "INSERT INTO calories_needs (rest_bmr, sedentary, light, moderate, active, target) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (rest_bmr, calorie_needs["sedentary"], calorie_needs["light"], calorie_needs["moderate"], calorie_needs["active"], target_calories)
            cursor.execute(query, data)
            conn.commit()
            print("Calorie needs saved successfully!")
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def suggest_healthy_meals(calorie_needs):
    if calorie_needs < 1200:
        print("Your daily calorie needs are very low. Please consult a nutritionist to create a personalized meal plan.")
    elif calorie_needs < 1500:
        print("Here are some healthy meal options for you:")
        print("- Grilled chicken with mixed vegetables")
        print("- Quinoa salad with roasted sweet potato and avocado")
        print("- Broiled salmon with roasted asparagus")
    elif calorie_needs < 1800:
        print("Here are some healthy meal options for you:")
        print("- Baked salmon with quinoa and sautéed spinach")
        print("- Chicken fajita bowl with brown rice and black beans")
        print("- Lentil soup with mixed greens salad")
    else:
        print("Here are some healthy meal options for you:")
        print("- Grilled sirloin steak with roasted Brussels sprouts and sweet potato")
        print("- Chickpea and vegetable stir-fry with brown rice")
        print("- Roasted vegetable and tofu bowl with brown rice and tahini dressing")
        
def get_calorie_needs_from_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="",
            password="",
            database="daily_calories"
        )
        if conn.is_connected():
            cursor = conn.cursor()
            # Retrieve the data from the table
            query = "SELECT * FROM calories_needs"
            cursor.execute(query)
            records = cursor.fetchall()
            for record in records:
                print(record)
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def update_the_daily_calories_data(updated_data):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="",
            password="",
            database="daily_calories"
        )
        if conn.is_connected():
            cursor = conn.cursor()
            # Update the data in the table
            query = "UPDATE calories_needs SET rest_bmr = %s WHERE id = %s"
            data = (updated_data, 1)  # assuming there is only one record in the table
            cursor.execute(query, data)
            conn.commit()
            print("Data updated successfully!")
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def print_welcome_message():
    print("Welcome to your calories python calculator!")
    print("Find out how many calories you should eat daily based on your BMR and activity level.")
    print("We will also calculate your body mass index (BMI) to give you an idea of your overall health.\n")

def get_gender():
    genders = ["male", "female"]
    while True:
        gender = input("Do you identify as male or female? ").lower()
        if gender not in genders:
            print("Invalid input. Please enter either 'male' or 'female'")
        else:
            return gender

def get_weight():
    while True:
        weight_unit = input("Would you like to enter your weight in kilograms or pounds? ").lower()
        if weight_unit == "kilograms":
            weight_kg = float(input("Enter your weight in kilograms: "))
            if weight_kg <= 0:
                print("Invalid input. Please enter your weight in kilograms: ")
            else:
                return weight_kg
        elif weight_unit == "pounds":
            weight_lb = float(input("Enter your weight in pounds: "))
            if weight_lb <= 0:
                print("Invalid input. Please enter your weight in pounds: ")
            else:
                weight_kg = weight_lb * 0.45359237
                return weight_kg
        else:
            print("Invalid input. Please enter either 'kilograms' or 'pounds'")

def get_height():
    while True:
        height_unit = input("Would you like to enter your height in centimeters or feet/inches? ").lower()
        if height_unit == "centimeters":
            height_cm = float(input("Enter your height in centimeters: "))
            if height_cm <= 0:
                print("Invalid input. Please enter your height in centimeters: ")
            else:
                return height_cm
        elif height_unit == "feet/inches":
            height_ft = int(input("Enter your height in feet: "))
            height_in = int(input("Enter your height in inches: "))
            if height_ft <= 0 or height_in < 0 or height_in >= 12:
                print("Invalid input. Please enter your height in feet/inches: ")
            else:
                height_cm = (height_ft * 12 + height_in) * 2.54
                return height_cm
        else:
            print("Invalid input. Please enter either 'centimeters' or 'feet/inches'")

def get_age():
    while True:
        age_yrs = int(input("Enter your age in years: "))
        if age_yrs <= 0:
            print("Invalid input. Please enter your age in years: ")
        else:
            return age_yrs

def calculate_bmi(weight, height):
    height_m = height / 100  # Convert height from cm to m
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def calculate_bmr(gender, weight, height, age):
    if gender == "female":
        bmr = (weight * 10) + (height * 6.25) - (age * 5) - 161
    else:
        bmr = (weight * 10) + (height * 6.25) - (age * 5) + 5
    return int(bmr)

def total_calories_needed(rest_bmr):
    activity_level = get_user_activity_level()
    goal = get_user_goal()
    calorie_needs = {
        "sedentary": get_sedentary_calories(rest_bmr),
        "light": get_light_activity_calories(rest_bmr),
        "moderate": get_moderate_activity_calories(rest_bmr),
        "active": get_very_active_calories(rest_bmr)
    }
    target_calories = calculate_target_calories(calorie_needs[activity_level], goal)
    print(f"You need to eat {calorie_needs[activity_level]} calories a day to maintain your current weight")
    if goal == "lose":
        print(f"To lose weight, you should eat {target_calories} calories a day.")
    elif goal == "gain":
        print(f"To gain weight, you should eat {target_calories} calories a day.")
    else:
        print("Invalid goal. Please try again.")

    # Save the calorie needs to the database
    save_daily_calorie_needs(rest_bmr, calorie_needs, target_calories)

def get_user_goal():
    while True:
        goal = input("Do you want to lose weight, maintain weight, or gain weight? ").lower()
        if goal not in ["lose", "maintain", "gain"]:
            print("Invalid input. Please enter: 'lose', 'maintain', or 'gain'")
        else:
            return goal

def calculate_target_calories(base_calories, goal):
    if goal == "lose":
        return int(base_calories * 0.8)
    elif goal == "gain":
        return int(base_calories * 1.2)
    else:
        return None

def get_user_activity_level():
    while True:
        print("\nWhat is your activity level?")
        print("Sedentary is little to no exercise.")
        print("Lightly active is light exercise/sports 1 - 3 days/week.")
        print("Moderately active is moderate exercise/sports 3 - 5 days/week.")
        print("Very active is hard exercise every day, or 2 xs/day 6 - 7 days/week.")
        activity_level = input("Please enter: 'sedentary', 'light', 'moderate', or 'active' ").lower()
        if activity_level not in ["sedentary", "light", "moderate", "active"]:
            print("Invalid input. Please enter: 'sedentary', 'light', 'moderate', or 'active'")
        else:
            return activity_level

def get_sedentary_calories(rest_bmr):
    return int(rest_bmr * 1.25)

def get_light_activity_calories(rest_bmr):
    return int(rest_bmr * 1.375)

def get_moderate_activity_calories(rest_bmr):
    return int(rest_bmr * 1.550)

def get_very_active_calories(rest_bmr):
    return int(rest_bmr * 1.725)

if __name__ == "__main__":
    main()
