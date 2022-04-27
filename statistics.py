import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import levene, ttest_ind
import matplotlib.patches as mpatches

boxes_locations = [[1, 2], [4, 5], [7, 8], [10, 11]] # Horizontal locations of boxes in the figure
colors = plt.cm.Pastel2(np.linspace(0, 1, 8))[[2,4]] # # Array for the 2 chosen colors of the boxes in the figure
statuses = ['nesting','migration_to_africa','wintering','migration_to_europe']
fig = plt.figure()

all_levene_pvalues = [] # List for all saved Levene pvalues
all_ttest_pvalues = [] # List for all saved t-test pvalues
all_ttest_statistic = [] # List for all saved t-test statistic
all_freedom_degrees = [] # List for all saved freedom degree

for status, position in zip(statuses, boxes_locations):
    # Reading the adults and juveniles 40 behaviour percentages
    adult = pd.read_csv('40Percentages/Adults/'+status+'.csv').values[:,1]
    juvenile = pd.read_csv('40Percentages/Juveniles/' + status + '.csv').values[:,1]

    # Removing nan values
    adult = adult[~np.isnan(adult)]
    juvenile = juvenile[~np.isnan(juvenile)]

    # Making Levene test and saving only pvalues
    _, levene_pvalue = levene(adult, juvenile)

    # Making t-test and saving statistic and pvalue
    ttest_statistic, ttest_eq_var_pvalue = ttest_ind(adult, juvenile, equal_var=True)

    # Calculating degree of freedom
    all_freedom_degrees.append(len(adult) + len(juvenile) - 2)

    # Saving results
    all_levene_pvalues.append(levene_pvalue)
    all_ttest_pvalues.append(ttest_eq_var_pvalue)
    all_ttest_statistic.append(ttest_statistic)

    # Plotting boxes
    bplot = plt.boxplot([adult, juvenile], positions=position, widths=0.75,
                        showmeans=True, patch_artist=True, showfliers=False)

    # Annotating significance
    if ttest_eq_var_pvalue < 0.05:
        plt.text(np.mean(position), 17,'*',
                 ha='center', color='k', fontsize=14)
    else:
        plt.text(np.mean(position), 17,'NS',
                 ha='center', color='k', fontsize=10)

    # Boxes colors
    for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)

    # Median colors
    for median in bplot['medians']:
        median.set_color('black')

    # Mean colors
    for means in bplot['means']:
        means.set_markerfacecolor('black')
        means.set_markeredgecolor('black')

# Adding x axis tick labels
xlabels = ['Nesting','Fall Migration','Wintering','Spring Migration']
plt.xticks(labels=xlabels, ticks=np.mean([[1,2],[4,5],[7,8],[10,11]], axis=1))

# Adding legend manually
handles = []
for color, label in zip(colors, ['Adults', 'Juveniles']):
    handles.append(mpatches.Patch(fc=color,ec='k', label=label))
fig.legend(handles=handles)

# y label
plt.ylabel('Pecking Relative Duration [%]')

# Adding seperating dashed lines between statuses
for x in [3,6,9]:
    plt.vlines(x,0,20,ls='--', alpha=0.15, colors='k')

# Limits
plt.xlim(0,12)
plt.ylim(0,20)

# All pvalues of Levene and t-test in one DataFrame
all_pvalues = pd.DataFrame(np.r_[all_levene_pvalues, all_ttest_pvalues].reshape(2, -1), columns=statuses)
all_pvalues.index = ['Levene', 'ttest']

# All t-test statistics in one DataFrame
all_ttest_statistic = pd.DataFrame(np.array(all_ttest_statistic).reshape(1, -1), columns=statuses)

# All freedom degrees in one DataFrame
all_freedom_degrees = pd.DataFrame(np.array(all_freedom_degrees).reshape(1, -1), columns=statuses)

# Saving all 3 DataFrames
all_pvalues.to_csv('StatisticResults/pvalues.csv')
all_ttest_statistic.to_csv('StatisticResults/statistics.csv')
all_freedom_degrees.to_csv('StatisticResults/freedom_degree.csv')