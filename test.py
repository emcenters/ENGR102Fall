# Create one line of a conditional statement that: sets flagged equals to if a oz ≥ 9, 
# the difference of past and current oz ≥ 5 and is positive, and false otherwise
oz = [0 for _ in range(4)]
i = 0
flagged = (oz[i] >= 9 or (i >=1 and (abs(oz[i-1] - oz[i]) >= 5 and oz[i] > 0)))
print(flagged)

counter = lambda oz, x: x+1 if oz > 0 else x

counter = counter(0, oz[i])

readings = [0 for _ in range(8)]
suppression_flag = False
tiers = [0 for _ in range(8)]
wind_speed = 0
wind_category = ""

if wind_speed >= 74:
    wind_category = "Hurricane"

for amplitude in readings:
    if(not(suppression_flag) and (amplitude >= 20 and wind_speed >= 39)):
        suppression_flag = True

    if(amplitude >= 35):
        tiers[3] += 1
    elif(amplitude >= 20):
        tiers[2] += 1
    elif(amplitude >= 10):
        tiers[1] += 1
    else:
        tiers[0] += 1

