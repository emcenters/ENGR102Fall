# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Sanjay Gopi
#               Emmanuelle Chern
# Section:      218
# Assignment:   Farmers Fight L3
# Date:         20 October 2026

import matplotlib.pyplot as plt

def load_season(season_list):
    '''Reads the list given from a string of a season, and returns the ET and rain values.'''
    et_list = []
    rain_list = []
    for season in season_list:
        et_list.append(float(season[-2].strip()))
        rain_list.append(float(season[-1].strip()))
    return et_list, rain_list

def load_all_seasons(filename):
    '''Reads the file from the filename given, and returns the ET and rain values.'''
    year_file_data = dict()
    with open(filename) as file:
        all_lines = file.readlines()
        all_lines = all_lines[1:]
        for line in all_lines:
            current_line = line.split(",")
            if int(current_line[0]) in year_file_data:
                year_file_data[int(current_line[0])] += [current_line[1:]]
            else:
                year_file_data[int(current_line[0])] = [current_line[1:]]

    year_data = dict()
    for year in year_file_data:
        year_data[year] = load_season(year_file_data[year])
    return year_data

def growth_stage(day):
    '''Receives the day number and returns the growth stage'''
    if day > 125:
        return "late"
    elif day > 45:
        return "mid"
    else:
        return "initial"

def crop_water_use(ET, kc):
    '''Receives the ET and Kc and returns the crop's water use per day.'''
    used = ET*kc
    return used

def pump_inches_per_day(capacity, hours = 18, eff = 0.8):
    '''The pump conversion, takes in capacity, hours, and efficiency, and returns the inches'''
    pumped = (capacity * 60 * hours * 231 * eff)/(144 * 43560)
    return pumped

def update_balance(dep, water_use, rain, water_pumped, limit):
   '''Updates the level of water depleteion. Takes in depletion at the start of the day, the day's crop water use, 
   the day's rain, the water pumped, and the stress limit. Returns a tuple with the new depletion and T or F'''
   dep += water_use - rain - water_pumped
   is_stress_day = False
   if dep < 0:
        dep = 0
   if dep > limit:
       is_stress_day = True
   return dep, is_stress_day

def smallest_safe_capacity(et_list, rain_list, cap_list, hours=18, eff=0.8, stress_lim=3.9):
    '''Tries the capacities in the order given and finds the first capacity with zero stress days. 
    Takes in the ET and rain list, the list of pump capacities, the hours and efficiency the pump runs at, 
    and the stress limit. Return the capacity that fulfills this condition.'''
    for cap in cap_list:
        stress_count = run_season(et_list, rain_list, cap, hours, eff, stress_lim)[1]
        if stress_count == 0:
            return cap
    return None

def design_capacity(needs, coverage = 0.9):
    '''Finds the smallest capacity that is enough for at least the coverage fraction of the seasons.
    Given: The needs dictionary, then the coverage. Default for coverage. Returns: A capacity (one of the values in the dictionary)'''
    cap_count = dict()
    for key in needs:
        if needs[key] in cap_count:
            cap_count[needs[key]] += 1
        else:
            cap_count[needs[key]] = 1
    num_seasons_need = len(needs)*coverage
    add_previous = 0
    cap_count = dict(sorted(cap_count.items()))
    for cap in cap_count:
        if cap!= None and add_previous+cap_count[cap] >= num_seasons_need:
            return cap
        else:
            add_previous += cap_count[cap]
    return 0

def seasons_covered(needs, capacity):
    '''Counts the seasons covered against the given capacity. Given a dictionary of the capacity needs and a capacity. Returns a count of
    capacities in the dictionary less than or equal to the given one.'''
    count = 0
    for key in needs:
        if needs[key] != None and (needs[key] <= capacity):
            count += 1
    return count

def plot_needs(needs, design_capacity):
    '''Plots the capacity needed for each year and a horizontal line for the design capacity. Given a dictionary of
    the capacities needed for each year and the design capacity.'''
    plt.bar(needs.keys(), needs.values(), label = "Design Capacity")
    plt.plot([list(needs.keys())[0], list(needs.keys())[-1]], [design_capacity, design_capacity], color = 'red', label = "Capacity Needed")
    plt.xlabel("Years")
    plt.ylabel("Capacity needed (gpm/acre)")
    plt.legend(loc = "upper right")
    plt.title("Capacities needed")
    plt.show()

def run_season(et_list, rain_list, capacity, hours=18, eff=0.8, stress_lim=3.9):
    '''Takes in the ET, rain, capacity, hours running, efficiency, and stress limit of the pump to calculate
    if the day qualifies as a stress day based on the depletion for each day. Returns depletion, total number of
    stress days, and the peak water used through the season.'''
    Kc_constants = {'initial': 0.35, 'mid': 1.15, 'late': 0.70}
    depletion = [0]
    peak_water_used = 0
    stress_day_counter = 0
    for i in range(len(et_list)):
        Kc = Kc_constants[growth_stage(i+1)]
        water_used = crop_water_use(et_list[i], Kc)
        peak_water_used = max(water_used, peak_water_used)
        water_pumped = 0
        if depletion[i] >= 1:
            water_pumped = pump_inches_per_day(capacity, hours, eff)
        depletion_val, is_stress_day = update_balance(depletion[i], water_used, rain_list[i], water_pumped, stress_lim)
        depletion.append(depletion_val)
        if is_stress_day:
            stress_day_counter += 1
    depletion = depletion[1:]
    return depletion, stress_day_counter, peak_water_used

def print_summary(days_sim, cap, num_stress_days, peak_use):
    '''Takes in total days simulated, pump capacity, total number of stress days, and the peak water use to 
    print out a summary of for every pump. Doesn't return a value but prints the summary lines.'''
    print(f'Days simulated: {days_sim}')
    print(f'Pump capacity tested: {cap:0.1f} gpm/acre')
    print(f'Days of crop water stress: {num_stress_days}')
    print(f'Peak daily crop water use: {peak_use:0.2f} in/day')
    print()
    
def plot_season(depletion_list, stress_lim=3.9):
    '''Takes in the depletion values and the stress limit and creates a plot with the values against 
    the horizontal limit line.'''
    plt.plot(range(1, len(depletion_list)+1), depletion_list)
    plt.plot([1, len(depletion_list)+1], [stress_lim, stress_lim], color = 'red')
    plt.title("Seasonal depletion against stress limit")
    plt.xlabel("Day Number")
    plt.ylabel("Depletion (in)")
    plt.show()

years_data = load_all_seasons("seasons_2015_2024.csv")
cap_list = []
needs = dict()
for i in range(23):
    cap_list += [1+0.5*i]
for year in years_data:
    needs[year] = smallest_safe_capacity(years_data[year][0], years_data[year][1], cap_list)
design_cap = design_capacity(needs)
num_season_covered = seasons_covered(needs, design_cap)

cap_2019 = -1
for cap in range(2, 9):
    depletion_list, stress_day_count, peak_water_use = run_season(years_data[2019][0], years_data[2019][1], cap)
    if stress_day_count == 0:
        if cap_2019 == -1:
            cap_2019 = cap
        else:
            cap_2019 = min(cap_2019, cap)
num_2019_covered = seasons_covered(needs, cap_2019)

for year in needs:
    print(f"{year}: {needs[year]:0.1f} gpm/acre")
print(f"Design capacity covering at least 90% of seasons: {design_cap:0.1f} gpm/acre")
print(f"Seasons with no stress at {design_cap:0.1f} gpm/acre: {num_season_covered} of {len(needs)}")
print(f"Seasons with no stress at {cap_2019:0.1f} gpm/acre (the L1 answer): {num_2019_covered} of {len(needs)}")
plot_needs(needs, design_cap)