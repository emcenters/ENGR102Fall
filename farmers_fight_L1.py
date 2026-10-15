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
# Date:         15 October 2026

# date	The calendar day	text, YYYY-MM-DD
# tmax_f, tmin_f	Daily high and low temperature	°F
# wind_mph	Average wind speed	miles per hour
# et_in	Reference evapotranspiration (ET): the water a well-watered reference crop would lose to the air that day	inches
# humidity_pct	Average relative humidity	percent
# rain_in


def run_season():
    print()


def load_season(filename):
    '''Reads the file from the filename given, and returns the ET and rain values.'''
    et_list = []
    rain_list = []
    with open(filename) as file:
        all_lines = file.readlines()
        for line in all_lines:
            current_line = line.split(',')
            et_list.append(current_line[4])
            rain_list.append(current_line[-1])
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
   '''Takes in depletion at the start of the day, the day's crop water use, the day's rain
   the water pumped, and the stress limit. Returns a tuple with the new depletion and T or F'''
   dep += water_use-rain-water_pumped
   if dep < 0:
        dep = 0
   is_stress_day = False
   if dep > limit:
       is_stress_day = True
   return dep, is_stress_day

def run_season(et_list, rain_list, capacity, hours=18, eff=0.8, stress_lim=3.9):
    Kc_constants = {'initial': 0.35, 'mid': 1.15, 'late': 0.70}
    depletion = 0
    stress_day_counter = 0
    peak_water_use = 0
    lowest_water_no_stess = -1
    for i in range(len(et_list)):
        Kc = Kc_constants(growth_stage(i+1))
        water_used = crop_water_use(et_list[i], Kc)
        peak_water_used = max(water_used, peak_water_use)
        water_pumped = pump_inches_per_day(capacity, hours, eff)
        depletion, is_stress_day = update_balance(depletion, water_used, rain_list[i], water_pumped, stress_lim)
        if is_stress_day:
            stress_day_counter += 1
        else:
            lowest_water_no_stess = min(water_pumped, lowest_water_no_stess)
    return depletion, stress_day_counter, peak_water_used

def print_summary(days_sim, cap, num_stress_days, peak_use, lowest_use):
    print(f'Days simulated: {days_sim}')
    print(f'Pump capacity tested: {cap:0.1f} gpm/acre')
    print(f'Days of crop water stress: {num_stress_days}')
    print(f'Peak daily crop water use: {peak_use:0.2f} in/day')
    print()

if lowest_use == -1:
    print("No tested capacity avoided water stress.")
else:
    print(f"Smallest capacity with no water stress: {} gpm/acre")
