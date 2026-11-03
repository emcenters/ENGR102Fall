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
    with open(filename) as file:
        split_file = file.readlines()
        split_file = split_file[1:]
        month_counter = 0
        for line in split_file:
            values = line.split(",")
            months.append(month_counter)
            rates.append(values[2])
            month_counter += 1
    
    fit_months = []
    fit_rates = []
    skipped_count = 0
    for i in range(len(months)):
        try:
            rate_num = int(rates[i])
            if i >= month_initial and rate_num >= min_rate:
                fit_rates.append(rate_num)
                fit_months.append(months[i])
                print(months[i], rate_num)
        except:
            skipped_count += 1
    return months, rates, fit_months, fit_rates, skipped_count

def fit_decline_np(months, rates):
    '''Calculates the same fit as fit_decline using NumPy.
    Receives a list of months and rates to be used. Returns the intercept and slope.'''
    log_rates = []
    for i in range(len(rates)):
        log_rates.append(math.log(rates[i]))
    D, qi = np.polyfit(x=months, y=log_rates, deg=1)
    return qi, -D

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
        report.write(f"Forecast at month 84: {month_84_pred:0.1f} bbl/month")

def plot_forecast(months, rates, qi, D, t_end = 84):
    '''plot two charts side by side, with titile, axis label with units, legend
    1) rates v months as points, with forecast from month0 to t_end as a smooth line
    2) uses a log scale on the y axis(plt.yscale("log"))'''
    plt.subplot(1, 2, 1)
    plt.scatter(months, rates, color='black', label = 'data')
    forecast_rate = forecast(qi, D, months) 
    slope, intercept = np.polyfit(months, forecast_rate, 1)
    trendline = np.poly1d([slope, intercept])
    plt.plot(months, trendline(months), color = 'blue', label= "forecast rate")
    plt.xlabel('months')
    plt.ylabel('rates (bbl/month)')
    plt.title('Rate of oil per month')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.scatter(months, rates, color='black', label = 'data')
    plt.yscale("log")
    qiLog, dLog = fit_decline_np(months, rates)
    forecast_rate = forecast(qiLog, dLog, range(t_end)) 
    slope, intercept = np.polyfit(range(t_end), forecast_rate, 1)
    trendline = np.poly1d([slope, intercept])
    plt.plot(months, trendline(months), color = 'blue', label= "logged forecast rate")
    plt.xlabel('months')
    plt.ylabel('logged rates (bbl/month)')
    plt.title('Rate of oil per month')
    plt.legend()
    plt.show()


### ------------------- MAIN CODE ------------------- ###
qi_tolerance = 0.01
D_tolerance = 0.000001
months_list, rates_list, fit_months_list, fit_rates_list, skipped_count = load_production("kyle_production.csv")

loop_inter, loop_slope = fit_decline(fit_months_list, fit_rates_list)
print(loop_slope, loop_inter)
py_inter, py_slope = fit_decline_np(fit_months_list, fit_rates_list)
print(py_slope, py_inter)

fits_agree = abs(loop_slope-(-py_slope)) <= qi_tolerance and abs(loop_inter-py_inter) <= D_tolerance
print(f"Loop and NumPy fits agree: {fits_agree}")
write_report("kyle_report.txt", read_lease_name("kyle_production.csv"), len(months_list), skipped_count, len(fit_months_list), py_inter, py_slope)
plot_forecast(fit_months_list, fit_rates_list, py_inter, py_slope)
    
    
    