# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Rama Patwardhan
#               Christian Hough
#               Sanjay Gopi
#               Emmanuelle Chern
# Section:      218
# Assignment:   Farmers Fight L1
# Date:         20 October 2026


# TEST growth_stage(45) -> initial
# TEST crop_water_use(0.30, 1.15) -> 0.345
# TEST pump_inches_per_day(3) -> 0.095
# TEST update_balance(0.9, 3, 0, 0.095, 3.9) -> 3.9, False
# TEST crop_water_use(0.9, 0.7) -> 0.63

import matplotlib.pyplot as plt

def load_season(filename):
    '''Reads the file from the filename given, and returns the ET and rain values.'''
    et_list = []
    rain_list = []
    with open(filename) as file:
        all_lines = file.readlines()
        all_lines = all_lines[1:]
        for line in all_lines:
            current_line = line.split(',')
            et_list.append(float(current_line[4]))
            rain_list.append(float(current_line[-1]))
    return et_list, rain_list

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

et_list, rain_list = load_season("cotton_season.csv")
lowest_cap_no_stress = -1
for cap in range(2, 9):
    depletion_list, stress_day_count, peak_water_use = run_season(et_list, rain_list, cap)
    print_summary(len(depletion_list), cap, stress_day_count, peak_water_use)
    if stress_day_count == 0:
        if lowest_cap_no_stress == -1:
            lowest_cap_no_stress = cap
        else:
            lowest_cap_no_stress = min(lowest_cap_no_stress, cap)
    
    plot_season(depletion_list)

if lowest_cap_no_stress != -1:
    print(f"Smallest capacity with no water stress: {lowest_cap_no_stress:0.1f} gpm/acre")
else:
    print("No tested capacity avoided water stress.")