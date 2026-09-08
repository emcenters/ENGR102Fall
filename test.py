# Create one line of a conditional statement that: sets flagged equals to if a oz ≥ 9, 
# the difference of past and current oz ≥ 5 and is positive, and false otherwise
oz = [0 for _ in range(4)]
i = 0
flagged = (oz[i] >= 9 or (i >=1 and (abs(oz[i-1] - oz[i]) >= 5 and oz[i] > 0)))
print(flagged)