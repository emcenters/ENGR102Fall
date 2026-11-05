# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Emmanuelle Chern
#               Fuman Jiang
# Section:      218
# Assignment:   Midnight Yield L3
# Date:         3 November 2026

# TEST CASES:
# TEST forecast(9500, 0.045, 12) -> 5536.1 (rounded)
# TEST forecast(9500, 0.045, 0) -> 9500.0
# TEST forecast(192453.45, 0.40023, 54) -> 7.9*10^-05 (rounded)
# TEST fit_decline_np(range(0, 10), [1866, 16708, 19695, 6054, 9028, 18794, 11224, 9302, 17903, 15801]) -> 6417.5 (rounded), -0.1124 (rounded)
# TEST read_lease_name("kyle_production.csv") -> Field Unit 1 - Kyle

# BUG: runtime (IndexError) | crashed when making the months list | changed to append to the months list rather than using an index
# BUG: logic | report said 53 months used in fit | changed the conditional to include month 6 by checking if the month is greater than or equal to rather than only greater than
# BUG: logic | the total number of months was 0 | changed the month counter that is used to assign month numbers to increase as another line of data from the csv is read

import math
import numpy as np
import matplotlib.pyplot as plt

def load_production(filename, month_initial = 6, min_rate = 1000):
    '''Reads the file and applies all three data rules:
    1) Month numbers come from line position, and the first line of data (not the header) is month 0
    2) A line whose oil value cannot be converted to a number is skipped and counted, and it still uses it's month number
    3) A month goes into the fit only if it is month 6 or later and its oil value is at least 1,000 bbl'''
    months = []
    rates = []
    skipped_count = 0

    with open(filename) as file:
        split_file = file.readlines()
        split_file = split_file[1:]
        month_counter = 0
        for line in split_file:
            values = line.split(",")
            try:
                val = float(values[2])
                months.append(month_counter)
                rates.append(val)
            except:
                skipped_count += 1
            month_counter += 1
    
    fit_months = []
    fit_rates = []
    for i in range(len(months)):
        if months[i] >= month_initial and rates[i] >= min_rate:
            fit_months.append(months[i])
            fit_rates.append(rates[i])    
    return months, rates, fit_months, fit_rates, skipped_count

def fit_decline_np(months, rates):
    '''Calculates the same fit as fit_decline using NumPy.
    Receives a list of months and rates to be used. Returns the intercept and slope.'''
    log_rates = []
    for i in range(len(rates)):
        log_rates.append(math.log(rates[i]))
    
    D, qi = np.polyfit(months, log_rates, 1)
    return np.exp(qi), -D

def forecast(qi, D, t):
    '''Returns a rate or an array of rates the same length as t.
    Receives the slope, intercept, and months passed.'''
    if type(t) == int:
        return qi * np.exp(-(D*t))
    else:
        forecasts = []
        for time in t:
            forecasts.append(qi * np.exp(-(D*time)))
        return forecasts
   

qi_tolerance = 0.01
D_tolerance = 0.000001
months_list, rates_list, fit_months_list, fit_rates_list, skipped_count = load_production("kyle_production.csv")

py_inter, py_slope = fit_decline_np(fit_months_list, fit_rates_list)

def midnight_month(qi, D, limit = 500, t_max = 240):
    '''Forecasts months 0 through t_max, compares to the limit at once, and finds the first month below it
    Takes in the intercept(qi) and slope(D) of the line of best fit, and limit to compare to else it defaults to 500. 
    Can take a max amount of months else it defaults to 240. Returns the first month under the limit.'''
    forecast_list = forecast(qi, D, range(0, t_max))
    under_limit = np.array(forecast_list) < limit
    if True in under_limit:
        return np.where(under_limit == True)[0][0]
    return None

def remaining_barrels(qi, D, start, end):
    '''Total forecast barrels from month start up to, but not including, month end. Returns the sum of the forecasts from start month to end month.
    Receives the intercept(qi) and slope(D) and the start and ending month that you want the sum to be for. Returns the sum.'''
    forecast_list = forecast(qi, D, range(start, end))
    return sum(forecast_list)

def month_label(m):
    '''Takes in a month number and returns the year and month in the format YYYY-MM.'''
    year = 2021
    month = 1
    for i in range(m):
        month += 1
        if month == 13:
            month %= 12
            year += 1
    return f"{year}-{month:02}"

def write_midnight_report(filename, total_barrels, first_month, qi, D, limit_list):
    '''Writes the report file. Receives the filename, total barrels, first month, qi, D, and list of limits.
    Returns nothing and writes a file.'''
    with open(filename, "w") as report:
        report.write(f"Produced through the last report: {total_barrels:0.0} bbl\n")
        report.write(f"{'Limit':>5}{'Midnight':>10}{'Date':>9}{'Remaining':>11}{'Total':>8}\n")
        for limit in limit_list:
            midnight = midnight_month(qi, D, limit)
            date = month_label(midnight)
            remains = remaining_barrels(qi, D, first_month, midnight)
            total = total_barrels+remains
            if midnight_month == None:
                midnight = "not reached by month 240"
            report.write(f"{limit:>5}{midnight:>10}{date:>9}{remains:>11.0}{total:>8.0}\n")

def plot_midnight(months, rates, qi, D, midnight, limit=500):
    '''Receives lists of months, rates, and qi, D, midnight month, and a limit to plot 
    the oil production up till midnight'''
    plt.scatter(months, rates, color='black', label = 'Data')
    plt.yscale("log")
    plt.axhline(limit, color='red', linestyle='--', label='Limit')
    if midnight == None:
        plt.axvline(len(months)-1, color='red', linestyle='--', label='Midnight Month')
    else:
        plt.axvline(midnight, color='red', linestyle='--', label='Midnight Month')
    forecasted_rates = forecast(qi, D, np.arange(midnight)) 
    if midnight == None:
        plt.plot(range(0, len(months)-1), forecasted_rates, color = 'blue', label= "Forecasted Rate")
    else:
        plt.plot(range(0, midnight), forecasted_rates, color = 'blue', label= "Forecasted Rate")
    plt.xlabel('Months')
    plt.ylabel('Log of Oil Rates (bbl/month)')
    plt.title('Rate of Oil per Month')
    plt.legend()

    plt.suptitle("Production till midnight")
    plt.tight_layout()
    plt.show()

total = sum(forecast(py_inter, py_slope, range(0, len(months_list))))
with open("midnight_report.txt", "w") as report:
    "empty"
write_midnight_report("midnight_report.txt", total, len(months_list), py_inter, py_slope, [1000, 500, 300])
midnight = midnight_month(py_inter, py_slope)
plot_midnight(fit_months_list, fit_rates_list, py_inter, py_slope, midnight)
