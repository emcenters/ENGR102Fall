# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Emmanuelle Chern
#               Sophia Holt
#               Fuman Jiang
#               Maya Mather
# Section:      218
# Assignment:   Midnight Yield L1
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

def fit_decline(months, rates):
    """Fit an exponential decline, q = qi * e^(-D * t), to production data.

    months: list of month numbers (0 = first month in the file)
    rates:  list of oil rates in bbl/month, same length; every rate must be > 0
    Returns the tuple (qi, D): initial rate in bbl/month, decline rate per month.
    """
    n = len(months)
    logs = []
    for q in rates:
        logs.append(math.log(q))
    sum_t = 0
    sum_y = 0
    sum_tt = 0
    sum_ty = 0
    for i in range(n):
        sum_t += months[i]
        sum_y += logs[i]
        sum_tt += months[i] ** 2
        sum_ty += months[i] * logs[i]
    slope = (n * sum_ty - sum_t * sum_y) / (n * sum_tt - sum_t ** 2)
    intercept = (sum_y - slope * sum_t) / n
    return math.exp(intercept), -slope

def read_lease_name(filename):
    '''Reads the lease name from the first data line. 
    Receives a string and returns the lease name.'''
    with open(filename) as file:
        lease_index = file.readline().split(",").index("lease")
        lease_name = file.readline().split(",")[lease_index].strip().strip("\n")
    return lease_name

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
   
def write_report(report_filename, lease_name, file_length, skipped_count, months_used, qi, D, t_end = 84):
    '''Writes the report in kyle_report.txt. Receives the filename.'''
    with open(report_filename, "w") as report:
        report.write(f"Lease: {lease_name}\n")
        report.write(f"Months in file: {file_length}\n")
        report.write(f"Lines skipped: {skipped_count}\n")
        report.write(f"Months used in fit: {months_used}\n")
        report.write(f"Model: q(t) = {qi:0.1f} * e^(-{D:0.4f}*t)\n")
        report.write(f"Initial rate qi: {qi:0.1f} bbl/month\n")
        report.write(f"Decline rate D: {D:0.4f} per month\n")
        month_84_pred = forecast(qi, D, t_end)
        report.write(f"Forecast at month {t_end}: {month_84_pred:0.1f} bbl/month\n")

def plot_forecast(months, rates, qi, D, t_end = 84):
    '''Plots two charts side by side, with a title, axis label with units, and a legend.
    1) Rates v months as points, with forecast from month 0 to t_end as a smooth line
    2) Uses a log scale on the y axis(plt.yscale("log"))'''
    plt.subplot(1, 2, 1)
    plt.scatter(months, rates, color='black', label = 'Data')
    forecasted_rates = forecast(qi, D, np.arange(t_end)) 
    plt.plot(range(t_end), forecasted_rates, color = 'blue', label= "Forecast Oil Rate")
    plt.xlabel('Months')
    plt.ylabel('Oil Rates (bbl/month)')
    plt.title('Rate of Oil per Month')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.scatter(months, rates, color='black', label = 'Data')
    plt.yscale("log")
    forecasted_rates = forecast(qi, D, np.arange(t_end)) 
    plt.plot(range(t_end), forecasted_rates, color = 'blue', label= "Log of Forecast Oil Rate")
    plt.xlabel('Months')
    plt.ylabel('Log of Oil Rates (bbl/month)')
    plt.title('Rate of Oil per Month')
    plt.legend()

    plt.suptitle("Oils Rates v. Month")
    plt.tight_layout()
    plt.show()


### ------------------- MAIN CODE ------------------- ###
qi_tolerance = 0.01
D_tolerance = 0.000001
months_list, rates_list, fit_months_list, fit_rates_list, skipped_count = load_production("kyle_production.csv")

loop_inter, loop_slope = fit_decline(fit_months_list, fit_rates_list)
py_inter, py_slope = fit_decline_np(fit_months_list, fit_rates_list)

fits_agree = abs(loop_slope-py_slope) <= D_tolerance and abs(loop_inter-py_inter) <= qi_tolerance
print(f"Loop and NumPy fits agree: {fits_agree}")
write_report("kyle_report.txt", read_lease_name("kyle_production.csv"), len(months_list)+skipped_count, skipped_count, len(fit_months_list), py_inter, py_slope)
plot_forecast(fit_months_list, fit_rates_list, py_inter, py_slope)

