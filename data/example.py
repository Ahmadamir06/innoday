# example.py

def get_user_input():
    user_input = input("Enter your name: ")
    print("Hello, " + user_input)

def calculate_area(radius):
    area = 3.14 * radius * radius
    print("Area is: " + str(area))
    return area

get_user_input()
calculate_area(5)