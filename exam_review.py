import math
def problem_one():
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    user_inputs = ["December 12", "January 15", "April 12", "April 25", "April 1"]
    # for i in range(5):
    #     user_inputs.append(str(input(f"User {i+1} please enter a birthday: ")))

    for i in range(len(user_inputs)):
        current = user_inputs[i]
        j = i-1
        
        while j >= 0 and month_names.index(current.title()[:-2].strip()) < month_names.index(user_inputs[j].title()[:-2].strip()):
            temp = user_inputs[j+1]
            user_inputs[j+1] = user_inputs[j]
            user_inputs[j] = temp

            j -= 1
        while j >= 0 and month_names.index(current.title()[:-2].strip()) == month_names.index(user_inputs[j].title()[:-2].strip()) and int(current.title()[-2:]) < int(user_inputs[j].title()[-2:]):
                temp = user_inputs[j+1]
                user_inputs[j+1] = user_inputs[j]
                user_inputs[j] = temp
                j -= 1
        user_inputs[j+1] = current

    print(user_inputs)

def problem_two():
    word = str(input("Enter the secret word: "))
    while len(word) < 6:
        word = str(input("Enter the secret word: "))
    guessed_letter = str(input("Guess a letter: "))
    count = 0
    while guessed_letter in word:
        guessed_letter = str(input("Guess another letter: "))
        count += 1
    print(f"The secret word is: \"{word}\". You took {count} guesses!")

def problem_three():
    roster = [["123004567", ["Joe", "Aggie", "ENGE", 3.50]],
        ["123004568", ["Jake", "Green", "OCEN", 3.75]],
        ["123004569", ["Jill", "Apple", "ENGR", 3.25]]]
    uin = int(input("Enter a UIN: "))
    index = 0
    for information_list in roster:
        if uin == int(information_list[0]):
            break
        index += 1
    print(f"{roster[index][1][0]} {roster[index][1][1]}: {roster[index][1][2]}, {roster[index][1][3]}")

def problem_four():
    total = 0
    for i in range(0, 201, 2):
        total += i
    print(total)

def problem_five():
    alphabet = "abcdefghjiklmnopqrstuvwxyz"
    for i in range(5):
        print(alphabet[i]*(i+1))

    subtract = 2
    for i in range(5, 0, -1):
        print(">"*(3-abs(subtract)))
        subtract -= 1
    subtract = 2
    for i in range(5):
        print("*"*(1+abs(subtract)))
        subtract -= 1
    
    for i in range(5):
        print(" "*i+"o"*(5-i))

    for i in range(5):
        print("x"*(4-i)+"o"*i)
    
def problem_six():
    ages = [int(input("Enter an age: "))]
    while ages[-1] != -1:
        ages.append(int(input("Enter another age: ")))
    ages.pop()
    print(f"{"Number of people":<20}{"Minimum age":<20}{"Maximum age":<20}")
    minimum = ages[0]
    maximum = ages[0]
    for age in ages:
        if age < minimum:
            minimum = age
        elif age > maximum:
            maximum = age
    print(f"{len(ages):<20}{minimum:<20}{maximum:<20}")

def problem_seven():
    letter_phone = str(input("Enter a phone number in this format XXX-XXXXXXX: "))
    letter_phone = letter_phone.replace("-", "")
    numbers = "0123456789"
    alphabet = "abcdefghijklmnopqrstuvwxyz".split(" ")
    phone_number = ""
    digit = 1
    for letter in letter_phone:
        if digit == 4 or digit == 7:
            phone_number += "-"
        if letter in numbers:
            phone_number += letter
        elif letter in "ABC":
            phone_number += "2"
        elif letter in "DEF":
            phone_number += "3"
        elif letter in "GHI":
            phone_number += "4"
        elif letter in "JKL":
            phone_number += "5"
        elif letter in "MNO":
            phone_number += "6"
        elif letter in "PQRS":
            phone_number += "7"
        elif letter in "TUV":
            phone_number += "8"
        elif letter in "WXYZ":
            phone_number += "9"
        digit += 1
    print(phone_number)

def problem_32():
    lock_wheels = [range(10) for _ in range(4)]
    combination = str(input("Enter a 4-digit combination: "))
    test_combo_list = [0 for _ in range(4)]
    count = 0
    for wheel4 in lock_wheels:
        for pin4 in wheel4:
            test_combo_list[0] = pin4
            for wheel3 in lock_wheels:
                for pin3 in wheel3:
                    test_combo_list[1] = pin3
                    for wheel2 in lock_wheels:
                        for pin2 in wheel2:
                            test_combo_list[2] = pin2
                            for wheel1 in lock_wheels:
                                for pin1 in range(len(wheel1)):
                                    test_combo_list[3] = pin1
                                    test_combo = "".join(str(num) for num in test_combo_list)
                                    if test_combo == combination:
                                        print(f"Combination found: {test_combo}")
                                        print(f"Number of computations: {count}")
                                        return
                                    count += 1

def problem_33():
    radius = float(input("Enter the radius: "))
    area = math.pi*radius**2
    perimeter = 2*math.pi*radius
    square_length_eq_area = math.sqrt(area)
    square_length_eq_perimeter = perimeter/4
    print(f"The circle has area {area:0.2f} and perimeter {perimeter:0.2f}")
    print(f"A square with equal area has side length {square_length_eq_area:0.2f}")
    print(f"A square with equal perimeter has side length {square_length_eq_perimeter:0.2f}")
problem_33()