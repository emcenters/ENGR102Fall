# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Rama Patwardhan
#               Christian Hough
#               Sanjay Gopi
#               Emmanuelle Chern
# Section:      218
# Assignment:   Taming the Hullabaloo - L1
# Date:         10 September 2026

# Test Cases (Amplitude, Wind Speed): (5, 4), (10, 14), (20, 14), (35, 14), (22, 41), (33, 20)
# Expected Tier: Normal, Elevated, Warning, Critical, Critical, Warning

# We changed the wind_speed to accept a float instead of an integer, and we added a statement 
# for when the suppression is not triggered based off of the feedback from the Study Partner.
# We also changed our print statement from using printf to use sep parameter instead.

readings = [4.2, 5.8, 6.1, 7.4, 9.0, 8.3, 6.7, 5.5, 12.1, 36.2, 11.5, 8.9, 9.4, 10.2,
            13.6, 15.8, 17.2, 14.9, 18.0, 22.5, 35.8, 36.4, 37.1, 19.5, 10.2, 8.7, 7.1,
            9.9, 11.4, 13.0, 16.5, 20.1, 18.8, 22.0, 35.5, 36.0, 17.2, 12.1, 9.8, 10.5,
            13.2, 16.8, 19.4, 21.0, 24.3, 27.6, 30.1, 32.4, 34.2, 35.9, 37.5, 39.0, 40.8,
            42.3, 18.0, 9.5, 8.9, 7.6, 6.4, 5.8, 4.9, 6.2, 7.8]

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
    print("Bridge status: SUPPRESSION NOT TRIGGERED during this log.")
        
        