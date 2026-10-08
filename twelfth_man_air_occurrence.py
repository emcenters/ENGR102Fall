# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Emmanuelle Chern
# Section:      218
# Assignment:   Mini Project 3 L4
# Date:         3 October 2026

# Given data: the 8 causes, how often each occurred, and the Severity/
# Detection ratings, same for both Occurrence methods below.
causes = ["W", "C", "M", "G", "D", "P", "B", "S"]
counts = [732, 332, 251, 151, 136, 92, 85, 22]

severity  = [6, 7, 8, 5, 4, 3, 5, 10]
detection = [2, 4, 3, 2, 2, 3, 5, 9]

# Needed for the normalized method below: this log's smallest and largest counts.
lowest = min(counts)
highest = max(counts)

string = 'word'
string.indexOf
fixed_rpn = []
normalized_rpn = []
for i in range(len(causes)):
    count = counts[i]

    # Method 1: fixed bands -- same count-to-rating cutoffs every time,
    # regardless of what this particular log's numbers look like.
    if count <= 5:
        fixed_occurrence = 2
    elif count <= 15:
        fixed_occurrence = 5
    elif count <= 30:
        fixed_occurrence = 7
    else:
        fixed_occurrence = 9

    # Method 2: normalized to this log -- the highest count here always
    # becomes a 10, the lowest always becomes a 1, everything else scaled
    # in between.
    fraction = (count - lowest) / (highest - lowest)
    normalized_occurrence = 1 + round(fraction * 9)

    # Same RPN formula both times, just fed a different Occurrence rating.
    fixed_rpn.append(severity[i] * fixed_occurrence * detection[i])
    normalized_rpn.append(severity[i] * normalized_occurrence * detection[i])

def sort_list(given_list):
    indexes_list = list(range(len(given_list)))
    for i in range(1, len(given_list)):
        current = given_list[i]
        current_index = indexes_list[i]
        j = i-1

        while j >= 0 and current > given_list[j]:
            temp = given_list[j+1]
            given_list[j+1] = given_list[j]
            given_list[j] = temp
            temp = indexes_list[j+1]
            indexes_list[j+1] = indexes_list[j]
            indexes_list[j] = temp
            j -= 1

        given_list[j+1] = current
        indexes_list[j+1] = current_index
    return indexes_list

def give_cause_name(index_list, cause_list, full_list):
    cause_name_list = ["" for _ in range(len(cause_list))]
    already_in_list = [0 for _ in range(8)]
    for i in index_list:
        match cause_list[i]:
            case "W": cause_name_list[i] = "Weather (W)"
            case "C": cause_name_list[i] = "Crew Timeout (C)"
            case "M": cause_name_list[i] = "Mechanical (M)"
            case "G": cause_name_list[i] = "Ground Stop (G)"
            case "D": cause_name_list[i] = "Deicing (D)"
            case "P": cause_name_list[i] = "Gate Conflict (P)"
            case "B": cause_name_list[i] = "Connecting-Flight Backup (B)"
            case "S": cause_name_list[i] = "Software/Scheduling System (S)"
        already_in_list[i] = 1
    
    weather_types = ["Weather (W)", "Crew Timeout (C)", "Mechanical (M)", "Ground Stop (G)", "Deicing (D)", "Gate Conflict (P)", "Connecting-Flight Backup (B)", "Software/Scheduling System (S)"]
    if full_list:
        for i in range(len(already_in_list)):
            if already_in_list[i] == 0:
                cause_name_list.append(weather_types[i])
    else:
        cause_name_list = [item for item in cause_name_list if item != ""]
    return cause_name_list

sorted_fixed_rpn_indexes = sort_list(fixed_rpn[:])
sorted_normalized_rpn_indexes = sort_list(normalized_rpn[:])

print("=== Fixed Occurrence Bands ===")
ranking_index = 1
sort_cause_list = give_cause_name(sorted_fixed_rpn_indexes, causes, True)
for i in sorted_fixed_rpn_indexes:
    print(f"{ranking_index}. {sort_cause_list[i]}: RPN {fixed_rpn[i]}")
    ranking_index += 1

print("=== Normalized Occurrence Bands ===")
ranking_index = 1
sort_cause_list = give_cause_name(sorted_normalized_rpn_indexes, causes, True)
for i in sorted_normalized_rpn_indexes:
    print(f"{ranking_index}. {sort_cause_list[i]}: RPN {normalized_rpn[i]}")
    ranking_index += 1
T3_fixed_indexes = sorted_fixed_rpn_indexes[:3]
T3_normalized_indexes = sorted_normalized_rpn_indexes[:3]
for cause in T3_fixed_indexes:
    if cause in T3_normalized_indexes:
        T3_normalized_indexes.remove(cause)
        T3_fixed_indexes.remove(cause)
if len(T3_fixed_indexes) == 0:
    T3_fixed_indexes.append("none")
if len(T3_normalized_indexes) == 0:
    T3_normalized_indexes.append("none")

print(f"Top cause, fixed bands: {give_cause_name([sorted_fixed_rpn_indexes[0]], causes, False)[0]}")
print(f"Top cause, normalized bands: {give_cause_name([sorted_normalized_rpn_indexes[0]], causes, False)[0]}")
print(f"Top cause changed: {'NO' if sorted_fixed_rpn_indexes[0] == sorted_normalized_rpn_indexes[0] else 'YES'}")
print(f"Top 3, fixed only: {', '.join(causes[i] for i in T3_fixed_indexes)}")
print(f"Top 3, normalized only: {', '.join(causes[i] for i in T3_normalized_indexes)}")


# RECOMMENDATION:
# I think that it would be more important to use the normalized RPN list because then the airline knows what is
# the most pressing issue to fix in comparsion to others. My answer would change to use the fixed RPN list six 
# months later though because there wouldn't be a crisis happening where you need to prioritize the most reccuring issue.