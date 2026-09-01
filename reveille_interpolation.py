# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:       ADHEETH PRABHANJANA
#              FUMAN JIANG
#              EMMANUELLE CHERN
#              GREY HOUGH
# Section:     218
# Assignment:  MINI PROJECT 1 L1
# Date:        1 SEPT 2026

import math

positions = [0 for _ in range(3)]; time = [0 for _ in range(3)]
r = 6745; C = 2 * math.pi * r

time[0] = 10; time[1] = 55
positions[0] = 2030; positions[1] = 23030

slope = (positions[1] - positions[0]) / (time[1] - time[0])

time[2] = float(input("Enter the query time in minutes: "))
positions[2] = slope * (time[2] - time[0]) + positions[0]
positions[2] = positions[2] % C

print(f"At t = {time[2]:.0f} minutes, the position is {positions[2]:.2f} km")

