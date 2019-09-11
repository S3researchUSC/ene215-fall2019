import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# set seaborn settings
sns.set_style("whitegrid")
plt.rcParams["font.family"] = "Arial Narrow"

# inputs
main_dir = '/Users/MEAS/GitHub/ene215-fall2019/01/python'
data_file = 'Primary Energy Consumption_from 1635.csv'

# set directory
os.chdir(main_dir)

# read in data
df_data = pd.read_csv(main_dir+'/data/'+data_file, skiprows=2)
df_data = df_data.rename(columns={df_data.columns[0]: "Year"})
df_data = df_data.fillna(0)
df_data['Other Renewables'] = df_data['Solar'] + df_data['Wind']

# create long version of dataframe
df_long = pd.melt(df_data,
					id_vars = 'Year',
					value_vars = ['Coal', 'Natural Gas', 'Petroleum', 'Nuclear',
					'Hydropower', 'Wood/biomass', 'Solar', 'Wind',
					'Other Renewables', 'Total Fossil', 'Total Renewable Energy'],
					var_name = 'Fuel', value_name = 'Value')

# remove totals, solar, and wind
df_fuels = df_long[~df_long.Fuel.isin(['Total Fossil', 'Total Renewable Energy', 'Solar', 'Wind'])]

# LINE PLOT ------------------------------------

# create new figure, with dimensions of width = 8.2 inches and height = 4.4 inches
fig, ax = plt.subplots(figsize = (8.2,4.4))

# create line plot with specified line colors
p = sns.lineplot(data = df_fuels, x = "Year", y = "Value", hue = "Fuel",
                 palette = {"Petroleum": "orange",
                            "Natural Gas": "red",
                            "Coal": "black",
                            "Nuclear": "seagreen",
                            "Hydropower": "steelblue",
                            "Wood/biomass": "brown",
                            "Other Renewables": "skyblue"});
ax.set_xlim([1635,2017])
ax.set_ylim([0,45])
ax.set_title('US Primary Energy Consumption by Source (1635 – 2017)', y=1.1, fontsize=20, fontweight='bold', loc='left')
ax.set_xlabel('')
ax.set_ylabel('')
ax.text(ax.get_xlim()[0], ax.get_ylim()[1]*1.05, 'Quadrillion British Thermal Units', horizontalalignment='left', fontsize=15)
ax.xaxis.grid(which="major", color='r', linestyle='-', linewidth=0)
ax.yaxis.grid(which="major", color='grey', linestyle='-', linewidth=0.3)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
plt.figtext(0.9, 0, 'Plot created by Kelly Sanders on September 9, 2019', horizontalalignment='right', fontstyle='italic')

fig.savefig("Figure_Fuel-Consumption-by-Source_KTSanders.png", dpi=600, bbox_inches='tight')

# -------------------------------------------------------------------------------------------------------------------

# analyze data from 1845-1905
years = np.arange(1845,1906,10)
df_rev = df_fuels[df_fuels.Year.isin(years)]
df_rev['span'] = (df_rev['Year']-10).map(str) + '-' + (df_rev['Year']).map(str)
df_rev['diff'] = df_rev.groupby(['Fuel'])['Value'].transform(lambda x: x.diff())
df_rev['perc_diff'] = df_rev.groupby(['Fuel'])['Value'].transform(lambda x: x.pct_change())
df_rev = df_rev.dropna()

# BAR PLOT (absolute) -------------------------------------------------------
fig, ax = plt.subplots(figsize = (10,5.6))
p = sns.barplot(data = df_rev, x = "span", y = "diff", hue = "Fuel",
                 palette = {"Petroleum": "orange",
                            "Natural Gas": "red",
                            "Coal": "black",
                            "Nuclear": "seagreen",
                            "Hydropower": "steelblue",
                            "Wood/biomass": "brown",
                            "Other Renewables": "skyblue"});
ax.set_title('Change in US Fuel Consumption by Source (1845-1905)', y = 1.04, fontsize = 20, fontweight='bold', loc='left');
ax.set_xlabel('');
ax.set_ylabel('');
ax.text(ax.get_xlim()[0], ax.get_ylim()[1], 'Quadrillion British Thermal Units', horizontalalignment='left', fontsize = 15);
ax.xaxis.grid(which="major", color='r', linestyle='-', linewidth=0);
ax.yaxis.grid(which="major", color='grey', linestyle='-', linewidth=0.3);
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False);
plt.figtext(0.9, 0, 'Plot created by Kelly Sanders on September 9, 2019', horizontalalignment='right', fontstyle='italic');

fig.savefig("Figure_Absolute-Change-in-Fuel-Consumption_KTSanders.png", dpi=600, bbox_inches='tight')

# BAR PLOT (percent) -----------------------------------------------

fig, ax = plt.subplots(figsize = (10,5.6))
p = sns.barplot(data = df_rev, x = "span", y = "perc_diff", hue = "Fuel",
                 palette = {"Petroleum": "orange",
                            "Natural Gas": "red",
                            "Coal": "black",
                            "Nuclear": "seagreen",
                            "Hydropower": "steelblue",
                            "Wood/biomass": "brown",
                            "Other Renewables": "skyblue"});
ax.set_title('Percent Change in US Fuel Consumption by Source (1845-1905)', y=1, fontsize=20, fontweight='bold', loc='left');
ax.set_xlabel('');
ax.set_ylabel('');
vals = ax.get_yticks()
ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])
ax.xaxis.grid(which="major", color='r', linestyle='-', linewidth=0);
ax.yaxis.grid(which="major", color='grey', linestyle='-', linewidth=0.3);
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False);
plt.figtext(0.9, 0, 'Plot created by Kelly Sanders on September 9, 2019', horizontalalignment='right', fontstyle='italic');

fig.savefig("Figure_Rate-of-Change-in-Fuel-Consumption_KTSanders.png", dpi = 600, bbox_inches='tight')
