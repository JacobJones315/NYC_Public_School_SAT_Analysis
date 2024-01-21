import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# import csv file
schools = pd.read_csv("schools.csv")

# Preview the data
schools.head()

#filtering out avg math scores below 80% and keeping only the school name and avg_math columns 
best_math_schools = schools.loc[schools['average_math'] >= 0.8 * 800, ['school_name', 'average_math']].sort_values('average_math', ascending=False)

schools['total_SAT'] = schools['average_math'] + schools['average_reading'] + schools['average_writing']


#creates a df showing top 10 schools, only including school_name and total avg SAT score
top_10_schools = schools.nlargest(10, 'total_SAT') [['school_name', 'total_SAT']] 



# Calculate mean and standard deviation for each borough
boroughs  = schools.groupby('borough')['total_SAT'].agg(['count', 'mean', 'std']).round(2)

# Rename columns for clarity
boroughs.columns = ['num_schools', 'average_SAT', 'std_SAT']


boroughs3 = schools[['borough','school_name', 'total_SAT']]

#creating a multi-level index and sorting
boroughs4  = boroughs3.set_index(['borough','school_name']).sort_index()

# shows the top 3 schools by each borough, keeping index as borough/school name
top_3_schools = boroughs4.sort_values(['borough', 'total_SAT'], ascending=[True, False]).groupby('borough').head(3)
print(top_3_schools)

pivot_df = top_3_schools.pivot_table(values='total_SAT', index='school_name', columns='borough')

# creating heatmap, fmt makes it so the values in the hatmap are integers and not decimals

plt.figure(figsize=(12, 8))
sns.heatmap(pivot_df, cmap='YlGnBu', annot=True, fmt='.0f', cbar_kws={'label': 'Average SAT Score'})
plt.xlabel('Borough')
plt.ylabel('School Name')
plt.title('Average SAT Scores for the Top 3 Schools in Each Borough')


# Filter for max std and reset index so borough is a column
largest_std_dev = boroughs[boroughs["std_SAT"] == boroughs["std_SAT"].max()]


# Rename columns for clarity
largest_std_dev.columns = ['num_schools', 'average_SAT', 'std_SAT']


fig, ax =plt.subplots(dpi =100)
ax= sns.barplot(data = boroughs, x = boroughs.index, y ='average_SAT', yerr = boroughs['std_SAT'], alpha = 0.7)
ax.set_xlabel('Borough')
ax.set_ylabel("Average SAT Score")
ax.set_title("Average SAT Scores by NYC Borough")
ax2 = ax.twinx()
sns.lineplot(data=boroughs, x='borough', y='num_schools', ci=None, color='black', marker ='o', markersize = 8, ax=ax2)
ax2.set_ylabel('Number of Schools per Borough')


fig, bz =plt.subplots(dpi =100)
bz= sns.barplot(data = top_10_schools, x = 'total_SAT', y ='school_name')
bz.set_xlabel('Average SAT Score"')
bz.set_ylabel("School")
bz.set_title("Top 10 Public Schools in NYC")
