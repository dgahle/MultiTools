from pandas import read_csv
from numpy import convolve, isnan, where, diff, round
from scipy.signal import fftconvolve
from multitools import dot_convolve, date_str_to_date_int, date_int_to_date_str
from matplotlib.pyplot import subplots
from time import time

# get example data to plot
covid_incidence_link = "https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=newCasesByPublishDate&format=csv"
df_incidence = read_csv(covid_incidence_link)
# make chronological
df_incidence = df_incidence[::-1].reset_index(drop=True)
# add date_int to df for plotting
pandas_date_format = "%Y-%m-%d"
df_incidence["date_int"] = date_str_to_date_int(df_incidence.date, df_incidence.date.min(), pandas_date_format)

# smooth data
run_reps = 50
days = 7
window_function = [1/days for i in range(days)]
runtimes = [time()]
for _ in range(run_reps):
    incidence_numpy = convolve(df_incidence.newCasesByPublishDate, window_function, mode='same')
runtimes.append(time())
for _ in range(run_reps):
    incidence_scipy = fftconvolve(df_incidence.newCasesByPublishDate, window_function, mode='same')
runtimes.append(time())
for _ in range(run_reps):
    incidence_pandas = df_incidence.newCasesByPublishDate.rolling(days, center=True).mean()
runtimes.append(time())
for _ in range(run_reps):
    incidence_omnitools = dot_convolve(df_incidence.newCasesByPublishDate, window_function)
runtimes.append(time())

runtimes_ms = round(1e3 * diff(runtimes)/run_reps, 1)
keys = ["numpy", "scipy", "pandas", "multitools"]
runtime_pre_dict = [(k, r) for k, r in zip(keys, runtimes_ms)]
runtime_dict = dict(runtime_pre_dict)
for key in runtime_dict:
    print(key, runtime_dict[key])

incidences = [incidence_numpy, incidence_scipy, incidence_pandas, incidence_omnitools]
for name, incidence in zip(keys, incidences):
    error = (incidence.sum() - df_incidence.newCasesByPublishDate.sum()) / df_incidence.newCasesByPublishDate.sum()
    print(name, 100 * abs(error))


# plot data
non_nan = [not check for check in isnan(incidence_pandas)]
non_nan_indicies = where(non_nan)[0]
rolling_x = [df_incidence.date_int, df_incidence.date_int, df_incidence.date_int, df_incidence.date_int[non_nan_indicies]]
rolling_y = [incidence_omnitools, incidence_numpy, incidence_scipy, incidence_pandas[non_nan_indicies]]
rolling_label = ["multitools.dot_convolve", "numpy.convolve", "scipy.signal.fftconvolve", "pandas.DataFrame.rolling"]
rolling_offset = [0 * offest for offest in range(len(rolling_y))]

rolling_linestyle = '--'
linewidth = 3

fig, ax = subplots()

ax_start = fig.add_axes([0.235, 0.42, 0.2, 0.25])
ax_end = fig.add_axes([0.65, 0.6, 0.2, 0.25])

for a in [ax, ax_start, ax_end]:
    a.plot(df_incidence.date_int, df_incidence.newCasesByPublishDate, linewidth=linewidth)

    for x, y, label, offset, rtime in zip(rolling_x, rolling_y, rolling_label, rolling_offset, runtimes_ms):
        a.plot(x, y + offset, linestyle=rolling_linestyle, label=label, linewidth=linewidth)

ax.set_title("Covid-19 Incidence - A Comparison of Rolling Averages")
ax.set_ylabel("Covid-19 Incidence")
ax.set_xlabel("Date")
ax.set_ylim(bottom=0)
ax.set_xlim(0, df_incidence.date_int.max())

ticks = [60 * tick for tick in range(13)]
tick_labels = date_int_to_date_str(ticks, df_incidence.date.min(), pandas_date_format)
ax.set_xticks(ticks, tick_labels, rotation=90)

ax.legend(title=f"{days}-day rolling average")

mini_days = 7
ax_start.set_xlim(0, mini_days)
ax_start.set_ylim(0, 2)
ax_end.set_xlim(df_incidence.date_int.max() - mini_days, df_incidence.date_int.max())
ax_end.set_ylim(0, 120e3)

for a in [ax_start, ax_end]:
    low, high = a.get_xlim()
    ticks = [low, high]
    tick_labels = date_int_to_date_str(ticks, df_incidence.date.min(), pandas_date_format)
    a.set_xticks(ticks, tick_labels, rotation=0)

fig.tight_layout()

fig.show()
