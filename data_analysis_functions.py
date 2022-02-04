# import libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from firebase_queries import query_cbc_analyte_by_covid, query_cbc_analyte_unit

# This function accepts a matplotlib.figure object that was previously
# closed as a parameter then redisplays that figure 
def redisplay_fig(analyte_plot):
    
    # create new dummy figure and use it to display analyte_plot
    dummy = plt.figure()
    new_manager = dummy.canvas.manager
    new_manager.canvas.figure = analyte_plot
    analyte_plot.set_canvas(new_manager.canvas)
    analyte_plot.set_size_inches(5, 5)
    
    plt.show()
    plt.close()

# This function accepts a dictionary containing statistical data about an
# analyte and displays it.
def display_statistic(stat_dict):
    print(f'\nThe COVID negative sample median is {stat_dict["neg_median"]} {stat_dict["unit"]}.')
    print(f'The COVID positive sample median is {stat_dict["pos_median"]} {stat_dict["unit"]}.')
    print(f'The p-value for a two-tailed Mann-Whitney-Wilcoxon test comparing sample medians is {stat_dict["p_value"]:.2e}')
    
    if (stat_dict['p_value'] < 0.05):
        print('The hypothesis that the two samples have different medians is statistically significant with an alpha of 0.5.')
    else:
        print('The null hypothesis that the two samples have the same median cannot be rejected with an alpha of 0.05.')
    print()

# This function creates a box plot for the analyte parameter 
# by COVID result status. Displays then returns the figure.
def plot_analyte_by_covid(analyte):
    
    plot_data = query_cbc_analyte_by_covid(analyte)
    analyte_unit = query_cbc_analyte_unit(analyte)

    analyte_fig = plt.figure(figsize=(5, 5))
    ax = analyte_fig.add_axes([0.15,0.1,0.75,0.8])
    ax.boxplot(plot_data, showfliers=False, widths=0.4, labels=['COVID Neg', 'COVID Pos'])
    ax.set_title(f'{analyte} by COVID')
    ax.set_ylim(ymin=0)
    ax.set_ylabel(analyte_unit)

    plt.show()
    plt.close()

    return analyte_fig

# This function compares the analyte parameter's median from the
# COVID negative and COVID positive samples. Returns a dictionary
# containing the p-value, medians for both samples, and the units
# of measure
def compare_analyte_by_covid(analyte):
    
    # query analyte data and units from database
    stat_data = query_cbc_analyte_by_covid(analyte)
    analyte_unit = query_cbc_analyte_unit(analyte)

    p_value = stats.mannwhitneyu(stat_data[0], stat_data[1], alternative='two-sided')[1]
    neg_median = np.median(stat_data[0])
    pos_median = np.median(stat_data[1])

    stat_dict = {'p_value': p_value, 'neg_median': neg_median, 'pos_median':pos_median, 'unit': analyte_unit}

    return stat_dict


# This function displays a summary of the dataset
def display_summary(data_summary):

    print(f"\nNumber of entries: {len(data_summary['Age'])}")
    print(f"Percent by Sex: {(data_summary['Sex'].count('F') / len(data_summary['Sex']) * 100):.1f}% Female, {(data_summary['Sex'].count('M') / len(data_summary['Sex']) * 100):.1f}% Male" )
    print(f"Average age: {(sum(data_summary['Age']) / len(data_summary['Age'])):.1f} years (min: {min(data_summary['Age']):.1f}, max: {max(data_summary['Age']):.1f})")
    print(f"Percent COVID Positive: {(data_summary['COVID'].count('Yes') / len(data_summary['COVID']) * 100):.1f}%")
    print()