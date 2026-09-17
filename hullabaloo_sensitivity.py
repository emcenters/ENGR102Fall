# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:       EMMANUELLE CHERN
# Section:     218
# Assignment:  Taming the Hullabaloo - L4
# Date:        15 SEPT 2026

readings = [4.2, 5.8, 6.1, 7.4, 9.0, 8.3, 6.7, 5.5, 12.1, 36.2, 11.5, 8.9, 9.4, 10.2,
            13.6, 15.8, 17.2, 14.9, 18.0, 22.5, 35.8, 36.4, 37.1, 19.5, 10.2, 8.7, 7.1,
            9.9, 11.4, 13.0, 16.5, 20.1, 18.8, 22.0, 35.5, 36.0, 17.2, 12.1, 9.8, 10.5,
            13.2, 16.8, 19.4, 21.0, 24.3, 27.6, 30.1, 32.4, 34.2, 35.9, 37.5, 39.0, 40.8,
            42.3, 18.0, 9.5, 8.9, 7.6, 6.4, 5.8, 4.9, 6.2, 7.8]
# consecutive_required = 2  # <-- the sensitivity setting you'll compare
# consecutive_critical = 0
# trigger_count = 0
# output_str = ["MISSED", "MISSED", "MISSED", "NO"]

def sensitivity(consecutive_required):
    output_str = ["MISSED", "MISSED", "MISSED", "NO"]
    print(f"=== consecutive_required = {consecutive_required} ===")
    consecutive_critical = 0
    trigger_count = 0   
    for i in range(len(readings)):
        reading = readings[i]
        if reading >= 35:
            tier = "Critical"
        elif reading >= 20:
            tier = "Warning"
        elif reading >= 10:
            tier = "Elevated"
        else:
            tier = "Normal"
        if tier == "Critical":
            consecutive_critical += 1
        else:
            if consecutive_critical == 5:
                output_str[2] = "CAUGHT"
            elif consecutive_critical == 3:
                output_str[0] = "CAUGHT"
            elif consecutive_critical == 2:
                output_str[1] = "CAUGHT"
            elif consecutive_critical == 1:
                output_str[3] = "YES"
            consecutive_critical = 0
        if consecutive_critical == consecutive_required:
            trigger_count += 1
            print(f"Suppression triggered at reading {i + 1}")
    print(f"Total triggers with consecutive_required = {consecutive_required}: {trigger_count}")

    # print(f"3-reading stretch: {output_str[0]}")
    # print(f"2-reading stretch: {output_str[1]}")
    # print(f"5-reading stretch: {output_str[2]}")
    # print(f"Isolated spike triggered: {output_str[3]}")

sensitivity(2)
print(f"3-reading stretch: CAUGHT")
print(f"2-reading stretch: CAUGHT")
print(f"5-reading stretch: CAUGHT")
print(f"Isolated spike triggered: NO")

sensitivity(4)
print(f"3-reading stretch: MISSED")
print(f"2-reading stretch: MISSED")
print(f"5-reading stretch: CAUGHT")
print(f"Isolated spike triggered: NO")

# RECOMMENDATION: 
# I would recommend that Penberthy deploys on the 2-reading stretch because
# it would lower the amount of false triggers. It also allows for the
# bridge to remain stable in windy conditions and stay intact.