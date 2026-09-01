# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:       FUMAN JIANG
#              EMMANUELLE CHERN
# Section:     218
# Assignment:  MINI PROJECT 1 L3
# Date:        1 SEPT 2026

import math

rev_position = [0 for _ in range(3)]; rev_time = [0 for _ in range(3)]
gig_position = [0 for _ in range(3)]; gig_time = [0 for _ in range(3)]

r = 6745; C = 2 * math.pi * r

rev_time[0] = 10; rev_time[1] = 55
rev_position[0] = 2030; rev_position[1] = 23030

gig_time[0] = 10; gig_time[1] = 55
gig_position[0] = 17030; gig_position[1] = 38030

rev_speed = (rev_position[1] - rev_position[0]) / (rev_time[1] - rev_time[0])
gig_speed = rev_speed
gig_time[2] = rev_time[2] = float(input("Enter the query time in minutes: "))

rev_position[2] = (rev_speed * (rev_time[2] - rev_time[0]) + rev_position[0])
gig_position[2] = (gig_speed * (gig_time[2] - gig_time[0]) + gig_position[0])
rev_position[2] = rev_position[2] % C
gig_position[2] = gig_position[2] % C
separation = abs(rev_position[2]-gig_position[2])


print(f"Reveille: {rev_position[2]:.2f} km")
print(f"GigEm: {gig_position[2]:.2f} km")
print(f"Separation: {separation:.2f} km")