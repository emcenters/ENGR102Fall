# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Rama Patwardhan
#               Emmanuelle Chern
# Section:      218
# Assignment:   Taming the Hullabaloo - L3
# Date:         10 September 2026

# Test Cases: [1.0, 2.0, 3.0], [25.0, 23.0, 22.0, 4.0, 5.0], [25.0, 23.0, 22.0, 4.0, 5.0, 27.0]
# Expected Results: no streak, one streak, two streaks

# We changed where the loop would evaluate whether the current streak is greater than the previous
# longest streak to account for when a streak stops at the end of the list.

readings = [6.0, 22.0, 25.0, 8.0, 21.0, 30.0, 33.0, 34.0, 7.0]
wind_speed = float(input("Enter today's forecasted wind speed (mph): "))
tier_tally = [0, 0, 0, 0]
count = 0
time_elapsed = len(readings) * 0.1


for reading in readings:
    count += 1
    if reading >= 35:
        tier_tally[3] += 1
        print(f"Reading {count} ({reading}): Critical -- suppression system would engage")
    elif wind_speed >= 39 and reading >= 20:
        tier_tally[3] += 1
        print(f"Reading {count} ({reading}): Critical -- escalated due to today's Gale-force wind forecast")
    elif reading >= 20:
        tier_tally[2] += 1  
        print(f"Reading {count} ({reading}): Warning")
    elif reading >= 10:
        tier_tally[1] += 1
    else:
        tier_tally[0] += 1

print("")
print("Tier summary: Normal=" + str(tier_tally[0]), "Elevated=" + str(tier_tally[1]), "Warning=" + str(tier_tally[2]), "Critical=" + str(tier_tally[3]), sep=", ") 
print("Elapsed monitoring time:", round(time_elapsed, 1), "hours", sep = " ")

if tier_tally[3] >= 1:
    print("Bridge status: SUPPRESSION TRIGGERED during this log.")
else:
    print("Bridge status: Suppression system did not engage during this log.")
        

longest_streak = 0
current_streak = 0

for reading in readings:
    if reading >= 20:
        current_streak += 1
    else:
        current_streak = 0
    longest_streak = max(longest_streak, current_streak)

print(f"The longest streak in this list of readings is {longest_streak}")