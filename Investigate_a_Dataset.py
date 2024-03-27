#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Influence of Demographic Variables on Gun Background Checks
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# The United States has long struggled with high levels of gun violence in comparison to other world powers like Great Britian, or France. In fact the United States has the highest level of gun deaths among xx (cite). Research on this topic has been difficult until the last twenty/thirty years as there existed a ban on gun research under the xx. This changed with passage of the Brady Act during the Clinton Administration. In 1994  the National Instant Criminal Background Check System (NICS) was created to record background checks for the U.S. and its territories. Licensed firearm retailers in 37 states submitted their background checks directly to the FBI, while the remainder submitted to either state goverened reporters or xx (). Data for the NICS database spans from 1998 and continues until today. While the NICS database provides a wide reaching set of data points regarding background checks, and the types of guns purchased, however this does not include information on the subject of the background check, which makes it difficult to uncover demographic influences on the rate/preponderance of background checks. Thankfully, the United States conducts a decennial Census which provides the necessary background information. We are limited in the depth of demographic trends we can indentify as the NICS dataset only divides background checks by states, and not any other finer geographic region. In this analysis we aim to identify demographic factors/variables that correlate to significant changes in the rate of background checks. 
# 
# ### Question(s) for Analysis
# We hope to investigate the relationship between certain demographic factors like employment status, highest level of education, __ , and gun permit checks. We will also investigate whether there is geographic component to the levels of background checks. Research conducted by the Nationhood Lab suggests there is are significant geographic and regional trends to gun violence in the United States which stem from the cultures/peoples that colonized/immigrated to that area. 
# 
# 
# >**Tip**: Clearly state one or more questions that you plan on exploring over the course of the report. You will address these questions in the **data analysis** and **conclusion** sections. Try to build your report around the analysis of at least one dependent variable and three independent variables. If you're not sure what questions to ask, then make sure you familiarize yourself with the dataset, its variables and the dataset context for ideas of what to explore.

# In[1]:


# Importing pandas, numpy, and pyplot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


# Import HTML to Left-Align Markdown Tables

from IPython.core.display import HTML
table_css = 'table {align:left;display:block} '
HTML('<style>{}</style>'.format(table_css))


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# ### General Properties
# > **Tip**: You should _not_ perform too many operations in each cell. Create cells freely to explore your data. One option that you can take with this project is to do a lot of explorations initially. This does not have to be organized, but make sure you use enough comments to understand the purpose of each code cell. Then, after you're done with your analysis, trim the excess and organize your steps so that you have a flowing, cohesive report.

# ## Load National Instant Criminal Background Check System (NICS) Data Set
# 
# First we will read in the NICS dataset, and make some initial observations based on the shape of the data.

# In[3]:


# Read in NICS Gun Data and get a sense of the dataset
df_nics = pd.read_csv('Database_Ncis_and_Census_data/gun_data.csv')
df_nics.head()


# **Data Time Period**
# 
# 
# The NICS data set ends in September of 2017, which means that there is only partial data for that calendar year. As a result, it is possible that for uniformity we will exclude part or all of 2017 depending on whether or not the data set begins in September or another month. 
# 
# Additionally, all of the columns contain data in the first 5 rows, however it is possible that this is not the case throughout the entire data set. We will check the earliest part of the data set to see if all variables were collected initially.

# In[4]:


# Inspect the tail of the NICS dataset to observe the timespan of the data
#By viewing the tail we can observe that there are numerous null values in the earliest part of the data (1998)
df_nics.tail(10)


# **Data Time Period**
# 
# 
# The NICS data set begins in November of 1998, which means 10 months of data is missing for the 1998 calendar year. If the data set began in September of 1998, we would have 19 complete calendar years of data. As we do not, we may choose to exclude the 1998 data to maintain uniformity. 
# 
# **Null Data**
# 
# 
# By inspecting the earliest entries of the NICs dataset we can observe that there are numerous null values in this section of the data. When data collection began NICS only distinguished what type of gun the check was being performed for. The database does not seem to have initially collected data points relating whether the firearm was acquired as a result of pawning, private sale, or rental. Over time, the database expanded to collect these variables among others. 
# 
# Since there is less data for pawned, private sale, and rental columns, we would need to either remove the null data, or replace them with a relevant statistic like the median or mean for that column.
# 
# We will now explore the extent of the null data across the data set to better understand where else it might be required handle missing data.

# In[5]:


# Exploring the data features, and identifying missing data
df_nics.info()


# **Null Data**
# 
# 
# Based on the information provided by `.info()` a majority of the columns contain missing data. We can further see this by inspecting where the null values are using `.isnull()`
# 
# **Data Types**
# 
# 
# We would hope that the columns other than month and state are of a numerical data type as they contain numerical daya. Using `.info()` we can observe this to be true. We should note that the `multiple` and `totals` columns are of the integer data type while all other columns containing numerical data are of the float data type. This is not problematic as if we choose to mathematically combine `multiple` or `totals` with a float data type column the resulting value will be of the float data type. However, if we wanted the resulting value to be an integer, we would have to convert it to an integer.

# In[6]:


#Identify null values, sort in descending order
df_nics.isnull().sum().sort_values(ascending = False)


# **Null Data**
# 
# 
# `.isnull()` supports our inital observation that missing data exists in the rentals, and private sale columns. Interestingly, permit_recheck, returned_handgun, returned_long_gun, returned_other contain the most null data. Each row in the NICS dataset is an aggregation of the different instances in which all federal firearm licensee from a state might request a background check. As mentioned earlier, the data could be missing because these types of background checks were not initially performed. It is also possible that these checks were not included in the mandate of the database and were included later on. We do not have the information to make that determination.
# 
# The aim of this analysis is to investigate trends in gun permit checks. As a result, it would be useful to replace missing data with the mean values of that column. <--

# Ideas for exploration
# - monthly/seasonal changes in background checks
# - yearly changes in background checks
# - background checks based on gun type
# - What states have had the highest increase in permit checks, how does this correspond to changes in their populations? (poverty percentage, median household income, education level)
# - What type of guns are most often checked for permits (handgun, long-gun, etc.) 
# - what states have had the most guns returned to sellers
# 
# - Compare income/poverty levels to percentage with bachelors degree vs. high school diploma, what is association with gun permits over time (median income vs. per capita income)
# What data is needed?
# 
# NICS Database
# - Types of permit checks per state and total checks 2010-2016
# - Percent Change in population / population in 2010 and 2016
# - 

# **Duplicated Data**
# 
# Now that we have identified where data is missing, we will explore if there is duplicated data using `.duplicated`. 

# In[7]:


# Identify duplicate values
df_nics.duplicated().sum()


# We now know that we only need to address the null values. We will do so by replacing the null values with the mean of each column.

# In[8]:


# Replace missing values with mean for each column. Make sure to only calculate mean for columns with numeric values
df_nics.fillna(df_nics.mean(numeric_only = True), axis=0, inplace= True)


# In[9]:


# Check if any null values remain
df_nics.isnull().sum()


# All null values have been removed. Let's get a different sense of the data by inspecting the number of unique values.

# In[10]:


# Identify unique values
df_nics.nunique().sort_values(ascending = False)


# **Columns with Little Variability**
# 
# 
# 
# Column Name | Number of Unique Values | Number of Null Values
# ------------------| --------------------- | ------------------
# prepawn_handgun                  | 90     |  1943
# state                            | 55     |     0
# redemption_other                 | 47     |  7370
# private_sale_other               | 43     |  9735
# returned_other                   | 34     | 10670
# return_to_seller_handgun         | 17     | 10010
# return_to_seller_long_gun        | 17     |  9735
# prepawn_other                    | 16     |  7370
# rentals_handgun                   | 9     | 11495
# rentals_long_gun                  | 8     | 11660
# return_to_seller_other            | 5     | 10230
# 
# *Note: The null values presented here are those we found before replacing them with the mean of each column. We could have either dropped the columns first, in light of the amount of null data present, or we could have replaced all the null values before dropping the columns. We opted for the latter because it allowed us to first analyze the variability of the data in these columns, which provided further support for their removal.*
# 
# More than 10 of the NICS columns have less than 90 unique variables indicating there is little variability in these data points. We see that the variables with the least variability tend to have the most null values, as expected. This suggests that while we could use these variables in our analysis, it would be harder to determine the significance of our correlations as the sample sizes are comparatively small. As a result, we will drop all of these columns except for the `state` column.
# 
# **Too Many States**
# 
# If we look closely at the number of unique values we notice that are 55 `states` listed, when there are only 50 states in the U.S.. We will determine what geographic areas are included in the NICS database to discover the additional areas included in the data set. It is possible that the data set includes areas like the District of Columbia and Puerto Rico which are not states, but districts and territories, respectively, in the United States. 
# 
# Once we have identified the non-state geographic areas we can remove them from the data set.

# In[11]:


#Check what states/territories are listed
print('Number of Geographic areas:', df_nics['state'].nunique())
df_nics['state'].unique()


# The 5 non-state geographic areas are:
# - District of Columbia
# - Guam
# - Mariana Islands
# - Puerto Rico
# - Virgin Islands
# 
# Now that we have identified the no-state areas, we will remove them from the data set along with the aforementioned columns. 

# In[12]:


# Create a list of non-state territories
non_us_states = ['District of Columbia','Guam', 'Mariana Islands', 'Puerto Rico', 'Virgin Islands']


# In[13]:


# Remove non-state territories from the NICS dataset, and verify they have been removed
df_nics = df_nics.query('state not in @non_us_states')
print('Number of geographic areas:', df_nics['state'].nunique())


# Now that there are no missing values in the dataset, we will create two new columns for the month and year of each row. By creating two columns we can eventually get yearly permit totals for each row, and perhaps identify seasonal patterns.

# In[14]:


df_nics['month'] = pd.to_datetime(df_nics['month'])
df_nics['year'] = df_nics['month'].dt.year
df_nics['year'] = pd.to_datetime(df_nics['year'], format='%Y')
df_nics.head()


# We will convert all the state names to lower case to make them easier to query later on in our exploratory data analysis.

# In[15]:


#Convert all state names to lowercase
df_nics['state'] = df_nics['state'].str.lower()
df_nics.head()


# Now the NICS dataset has been cleaned, we can rename it to `nics_clean`.

# In[16]:


nics_clean = df_nics


# In summary we have loaded the NICS data set and cleaned the data of null values, replacing them with the mean for each column. We have also created seperate month and year columns to efficiently stratefy the data based on date. 

# ## Loading and Cleaning Census Data Set

# We will now load the Census data set and make some initial obeservations on the shape of the data and its timeframe. 

# In[17]:


# import census data, and viewing the first few rows
df_census = pd.read_csv('Database_Ncis_and_Census_data/US_Census_Data.csv')
df_census.head()


# The Census data set has 52 columns spanning all 50 states, however the `Fact Note` column already contains null values. Both 2010 and 2016 are included in the dataset, which is interesting as the Census is decennial. Notably the Census uses 2016 as a comparative year for the data collected in the 2010 Census. 
# 
# Since the states are represented as columns, all of the demographic data is contained in the rows and not easily visible. Let's list out the demographic variables.

# In[18]:


# List all demographic variables contained in the Census data set
for index, row in df_census.iterrows():
  print(index, row['Fact'])


# **Observations on Demographic Variables**
# 
# More than 20 rows in the `Fact` column contain irrelevant/extraneous data that will need to be removed from the cleaned data set. The Census data set provides information regarding the age, race, gender, and employment status of Americans in 2010, as well as population data. Most of this information is also provided for 2016 enabling us to compare the two years. 
# 
# We will now make observations regarding the columns in the data set.

# In[19]:


# get column names and summary info about the census dataset
df_census.info()


# All of the datatypes in the dataset are objects. Eventualy we will need to convert them to integers or floats to merge with the NICS dataset. 
# 
# **Questions about Data Consistency**
# 
# On first glance there is consistently 65 values per state column. Based on this, there don't appear to be any null values in the state columns. However, there are descrepancies between the number of values in the state columns (65) and those in the Fact (80) and Fact Note (28) columns. It is possible there is additional data in these columns, or there are null values. We will explore this further by searching for null values specifically. 

# **Identify Duplicates**
# 
# 
# We will check for duplicates using `.duplicated()` instead. 

# In[20]:


# Identify duplicates in the data
df_census.duplicated().sum()


# There are three duplicates present in the Census data set which need to be removed.

# In[21]:


# Remove duplicated data
df_census.drop_duplicates(inplace = True)
df_census.duplicated().sum()


# Duplicated data has been removed from the dataset. Let's check for missing values.

# In[22]:


df_census.isnull().sum().sort_values(ascending = False)


# **Identifying and Removing Null Values**
# 
# As suspected, the `Fact Note` column contains the most null values. Upon inspection it doesn't seem to contain any useful information, and so we will remove it. Contrary to our earlier theory, there are many missing values among the state columns. Strangely enough, each state column is missing 17 data points. We will drop the `Fact Note` column.

# In[23]:


# Remove Fact Note column, it contains the most null values and does not have any useful information
df_census.drop('Fact Note', axis=1, inplace = True)


# Since we plan on focusing on population, unemployment, highest level of education, and xx. We will remove the rows not containing this information. We want to keep the row containing land area as we can evaluate employment levels through employment density.

# In[24]:


# Drop rows that won't be used in the analysis by creating and concatenating data frame slices, 
# then reassign to df_census


df_census = pd.concat(
    [df_census.head(3), 
     df_census.iloc[34:36], 
     df_census.iloc[38:40],
     df_census.iloc[47:51], 
     df_census.iloc[62:64]]
)


# In[25]:


# Display the data frame and verify correct rows are present
df_census


# Now that all of the uneeded rows have been removed, we will work on the style and shape of the data to make it easier to merge with the NICS data set. First we will convert all of the state names to lowercase to match the NICS data set. 

# In[26]:


# Convert all column names to lower case to match the NICS database
df_census.columns = df_census.columns.str.lower()
df_census.head()


# We need to reset the index as there are gaps in the indexes where some rows have been removed. 

# In[27]:


# Reset the Index to account for non-continous indexes
df_census.reset_index(inplace = True)
df_census.head(25)


# In[28]:


# Drop the old non-continuous index
df_census.drop('index', axis = 1, inplace = True)
df_census.head()


# Now that the index has been corrected, we can now convert the object data types to floats to match the NICS data set. 

# In[29]:


#Get info on datatypes
df_census.info()


# All of the numerical data in the state columns are represented as objects and need to be converted to floats as mentioned before. However, each data point also contains non-numerical characters that will need to be removed first.  We will list each state in an numpy array to iteratively remove the non-numerical characters from the data.

# In[30]:


# Defining states for conversion to float
states = ['alabama', 'alaska', 'arizona', 'arkansas', 'california',
          'colorado', 'connecticut', 'delaware', 'florida', 'georgia',  
          'hawaii', 'idaho', 'illinois','indiana', 'iowa', 'kansas', 
          'kentucky', 'louisiana', 'maine','maryland', 'massachusetts', 
          'michigan','minnesota', 'mississippi', 'missouri', 'montana', 'nebraska',
          'nevada', 'new hampshire', 'new jersey', 'new mexico', 'new york',
          'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon','pennsylvania', 
          'rhode island', 'south carolina','south dakota', 'tennessee', 'texas', 'utah', 
          'vermont','virginia', 'washington', 'west virginia','wisconsin', 'wyoming']


# I originally tried to remove all non-digit characters from the strings like '.', ',', '$', and '\%', but this removed the context of which percents were 50.0\% versus 5.0\% or .05\%. Instead I will remove the characters individually

# In[31]:


# Removing non-digit characters, then converting to floats
for state in states:
    df_census[state].replace(',','', regex=True, inplace=True)
    df_census[state].replace('%','', regex=True, inplace=True)
    df_census[state].replace('\$','', regex=True, inplace=True)
    df_census[state] = pd.to_numeric(df_census[state], downcast='float', errors='ignore')


# In[32]:


# verify that non-digit character have been removed, and all objects containing numbers have been converted to floats
df_census


# As mentioned previously, the Census data set will need to be transposed to match the NICS data set. Currently, the demographic variables are contained in the data set rows rather than the columns. 

# In[33]:


# set fact as index
df_census.set_index('fact', inplace = True)
df_census.head()


# In[34]:


# Transpose census data and remove index on 'Fact'
census_transpose = df_census.T.reset_index()


# In[35]:


# Verify the data set has been transposed properly and the index has been removed from 'Fact'
census_transpose.head()


# In[36]:


# Rename the column name from index to state to match the column names in gun data
census_transpose.rename(columns={'index': 'state'}, inplace=True)
#census_transpose.dropna(axis=1, inplace=True)


# In[37]:


# Verify 'state' is now the index
census_transpose.head()


# The Census data has been transposed succesfully. We will improve the style of the data set by removing spaces and other unuseful characters from each column header. Spaces and commas will be replaced with underscores so the columns become easier to query. 

# In[38]:


# Convert column names to lowercase, replace commas and spaces to make them easier to list for removal
census_transpose.columns = census_transpose.columns.str.lower()
census_transpose.rename(columns=lambda x: x.strip().replace(" ", "_"), inplace=True)
census_transpose.rename(columns=lambda x: x.strip().replace(",", "_"), inplace=True)


# In[39]:


# Verify changes to column names
census_transpose.columns


# Now that the data has been properly reorganized, we can make the column labels less wordy and easier to work with.

# In[40]:


# Rename columns to so they are easier to work with, and more self-explanatory
census_transpose.columns = [
    'state',
    'population_2016',
    'population_2010',
    'percent_change_population',
    'hs_diploma_percentage',
    'bachelors_degree_percentage',
    'total_employment_percentage',
    'female_employment_percentage',
    'median_income',
    'income_per_capita',
    'poverty_percentage',
    'number_of_employers',
    'population_density',
    'land_area'    
]
census_transpose.head()


# At this point it appears our Census data is in order, however upon further inspection we notice that is not entirely true. 

# In[41]:


census_transpose.loc[29:42]


# We notice that rows 30-41 have several columns where the data is not listed as a percentage, like the other rows, and is instead listed as a decimal. We need to convert the decimals to percentages to match the rest of the data.

# In[42]:


# Fix columns where percentages are listed as decimals

# List all columns to be fixed
columns_to_fix = [
    'percent_change_population',
    'female_employment_percentage', 
    'hs_diploma_percentage',
    'bachelors_degree_percentage',
    'total_employment_percentage',
    'poverty_percentage'
]


rows_to_fix = census_transpose.iloc[30:42,:].copy()

# Drop the problematic rows
census_transpose.drop(census_transpose.index[30:42],inplace= True, axis=0)

# Correct the percentage error in the `rows_to_fix` slice
for i in columns_to_fix:
    rows_to_fix[i] = 100 * rows_to_fix[i]


# In the above cell we are copying the problematic rows and performing the changes on them first before we add the corrected rows back to the data set.

# In[43]:


# Verify decimals have been changed to percentages
rows_to_fix.head()


# In[44]:


# Add back in the fixed rows
census_transpose = pd.concat([census_transpose, rows_to_fix])


# Since we have concatenated the corrected rows to the data set, the data set is out of order. 

# In[45]:


# Sort the data by index to ensure states are in order
census_transpose.sort_values(by = 'state', inplace = True)


# In[46]:


# Check that the end of the data set is in sequential order
census_transpose.iloc[30:]


# We have accomplished the following:
# 
# **Census Dataset**
# - Remove extraneous rows and columns
# - Remove non digit characters from the data \('$', ',', '\%')
# - Transpose rows and columns
# - Rename columns with more informative names
# - Convert all state names to lowercase to match NICS dataset
# - Convert data listed as decimals to percentages where appropriate
# 
# Now we can save the cleaned census dataset. We will save it as `census_clean`

# In[47]:


# Rename cleaned census dataset
census_clean = census_transpose


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > **Tip**: Now that you've trimmed and cleaned your data, you're ready to move on to exploration. **Compute statistics** and **create visualizations** with the goal of addressing the research questions that you posed in the Introduction section. You should compute the relevant statistics throughout the analysis when an inference is made about the data. Note that at least two or more kinds of plots should be created as part of the exploration, and you must  compare and show trends in the varied visualizations. Remember to utilize the visualizations that the pandas library already has available.
# 
# 
# 
# > **Tip**: Investigate the stated question(s) from multiple angles. It is recommended that you be systematic with your approach. Look at one variable at a time, and then follow it up by looking at relationships between variables. You should explore at least three variables in relation to the primary question. This can be an exploratory relationship between three variables of interest, or looking at how two independent variables relate to a single dependent variable of interest. Lastly, you  should perform both single-variable (1d) and multiple-variable (2d) explorations.
# 
# 

# Now that both datasets have been cleaned, let's see some summary statistics about each dataset. We'll start with the NICS dataset first.

# In[48]:


nics_clean.describe()


# We can notice from the data that there are on average more permit checks for long guns than any other kind however they also have the greatest variability at STD of 9,416. Although on average there are fewer permit re-checks, they so have the highest max.

# In[49]:


# Use histograms to see distribution of the data
nics_clean.hist(figsize=(16,16), layout=(6,6))


# From the histogram plots we notice that the data tends to be right-skewed except for the month column. There appears to be two spikes in permit checks at the beginning and end of the year. 

# ### Research Question 1 - What are the Annual and Monthly Trends for Gun Permit Checks?

# Before we consider investigating correlations between demographic data and the number of gun permit checks, it would be helpful to understand what trends exist in gun permit checks. The NICS data set provides us with nearly 19 years of data to analyze. We will create visualizatios for both the annual and monthly trends. 
# 
# **Find Monthly Trends in Gun Background Check Data**
# 
# 
# We will use `.grouby()` to group the background check data by month and then focus soley on the totals column to identify trends in gun background checks.

# In[50]:


# Determine trends in monthly background checks
monthly_permit_trends = nics_clean.groupby('month')['totals'].sum()
monthly_permit_trends.head()


# There appears to be a 40x increase in background checks between November and December of 1998. It is possible that partial data was collected for November and that is why the totals are so low. Between December 1998 and January 1999 there is a decrease of around 300,000 background checks, and yet the levels regain 2/3 of that loss by March 1999. On first inspection it seems as though time of year may play a role in the number of background checks. Further investigation is necessary to support this claim. 
# 
# **Find Annual Trends in Gun Background Check Data**
# 
# 
# Now we will use `.groupby()` again to explore yearly changes in background checks. 

# In[51]:


# Annual trends in background checks
annual_permit_trends = nics_clean.groupby('year')['totals'].sum()
annual_permit_trends.head()


# There was a 10x increase in background checks between 1998 and 1999; this is due to the partial data collected in 1998. Background checks briefly decreased in 2000 to only return to near 1999 levels in 2001. 
# 
# We can better see the monthly and annual trends in background checks by creating visualizations like line graphs.

# In[52]:


# Plot Monthly Trends in Gun Background Checks
monthly_permit_trends.plot()
plt.title('Trends in Monthly Background Checks (1998-2017)')
plt.xlabel('Month')
plt.ylabel('Background Checks (Millions)')


# Over time the number of background checks has increased significantly from less than 1 Million per year in 1999, to over 3.5 Million in 2016. From 1999 to 2009 there are noticeable repeatitive peaks and valleys in the number of background checks. Outside of what appear to be the cyclical spikes we also notice several larger than usual spikes in monthly background checks in  late 1999 to early 2000, mid 2012, and late 2015 / early 2016. Let's zoom in on this data to see if we can further understand what is goin on at these times. 

# In[53]:


#Create three data frames to zoom in on the spikes in background checks 
nics_1999_2000 = nics_clean.query('year >= "1999-01-01" & year <= "2000-12-31"')
nics_2012 = nics_clean.query('year >= "2012-01-01" & year <= "2012-12-31"')
nics_2015_2016 = nics_clean.query('year >= "2015-01-01" & year <= "2016-12-31"')

# Extract the monthly data for each of the three data frames
df_1999_2000 = nics_1999_2000.groupby('month')['totals'].sum()
df_2012 = nics_2012.groupby('month')['totals'].sum()
df_2015_2016 = nics_2015_2016.groupby('month')['totals'].sum()
df_2015_2016.head()


# In[54]:


# Plot 1999-2000 dataframe
df_1999_2000.plot()
plt.title('Trends in Background Checks (Jan 1999- Dec 2000)')
plt.xlabel('Month')
plt.ylabel('Background Checks (Millions)')
plt.grid(True, which = 'both')


# In[55]:


# Plot 2012 dataframe
df_2012.plot()
plt.title('Trends in Monthly Background Checks (Jan-Dec 2012)')
plt.xlabel('Month')
plt.ylabel('Background Checks (Millions)')
plt.grid(True, which = 'both')


# In[56]:


# Plot 2015-2016 dataframe
df_2015_2016.plot()
plt.title('Trends in Monthly Background Checks (Jan 2015 - Dec 2016)')
plt.xlabel('Month')
plt.ylabel('Background Checks (Millions)')
plt.grid(True, which = 'both')


# All of the spikes in the three time periods occur at the end of year. There also is a smaller, but noticeable increase in background checks in the first three months of the year. Notably, the beginning of the year peak is much larger in 2016, and does not feature the brief cooling off period like 1999. 

# Surprisingly, the spike in background checks in 1999 does track with some large/well known mass shootings, specifically the July Atlanta day trading shooting which killed and injured a total of 23 people. Every following month there after there was one mass shooting injuring or kiilling at least 5 people including the Woodward Baptist shooting in September of 1999. It is possible that in light of deadly mass shootings Americans are more likely to acquire guns as a means of protection.
# 
# The Sandy Hook School Shooting takes place right in between the dramatic end of year rise in background checks for 2012. It is possible that the sustained in increase seen at the end of 2012 was exacerbated by the Sandy Hook shooting. The increase begins in mid-September, increases in pace in mid October, and increases the rise once again in mid November.
# 
# There was a small unusual rise in July of 2012, which is around the time of the Aurora shooting. 
# 
# Notable Mass Shootings from 2015 to 2016 (More than 4 Decedents)
# - Feb-Mar 2015: Tyrone, Missouri
# - Jun 2015: Emanuel AME Church
# - Jul 2015: Chattanooga,TN & Lafayette, LA 
# - Nov 2015: Colorado Springs,CO
# - Dec 2015: San Bernadino,CA
# - Feb 2016: Kalamazoo, MI & Hesston, Kansas
# - Jun-Jul 2016: Pulse Night Club & Dallas,TX
# - Sept 2016: Cascade Mall, Townville Elementary School
# 
# 
# Interestingly enough there are no mass shootings after September 2016 for the remainder of 2016, and yet there is a sustained increase in background checks from the end of July/beinning of August to the end of the year. 

# In[57]:


annual_permit_trends.plot()
plt.title('Trends in Annual Background Checks (1998-2017)')
plt.xlabel('Year')
plt.ylabel('Background Checks (Millions)')
plt.grid(True, which = 'both')


# When we look at the above graph we see significant drop-off in 2017, and low background checks levels in 1998. This is outside of the apparent increase in background checks from 1999-2016. Let's inspect the data to understand why that is.

# In[58]:


# Query the NICS database to determine what data was collected for 1998
df_98 = nics_clean.query('year < "1999-01-01"')
print ('Data Collected for 1998:', df_98['month'].unique())
print('Data was only collected for November and December 1998')


# In[59]:


# Query the NICS database to determine what data was collected for 2017
df_17 = nics_clean.query('year >= "2017-01-01"')
print('Data Collected for 2017:', df_17['month'].unique())
print('Data was only collected for January to September 2017')


# We can observe that data was collected for only part of the year in 1998 and 2017. The remainder of the dataset contains datapoints for all 12 months. It would be hard to make valid conclusions with the partial data included, we will remove the partial data (Nov-Dec 1998, Jan-Sept 2017). 

# In[60]:


# Creating new dataset with the timeframe we want to keep, and check the shape
df_1999_2016 = nics_clean.query('year > "1998-12-31" & year <= "2016-12-31"')
df_1999_2016.shape


# In[61]:


#Check the first few rows of the new dataset to confirm changes
df_1999_2016.head()


# Let's redo the monthly and annual graphs with the revised data set. 

# In[63]:


# Recreating Annual Plot
annual_background_checks = df_1999_2016.groupby('year')['totals'].sum()
annual_background_checks.plot()
plt.title('Trends in Annual Background Checks (1999-2016)')
plt.xlabel('Year')
plt.ylabel('Background Checks (Millions)')
plt.grid(True, which = 'both')


# Now that the data has been corrected we can observe an overall increase in background checks from 2004 to 2016. We can also notice that initialliy there was a decrease in background checks from 1999 to 2000, and the number of checks nearly leveled off from 2002 to 2004, 2009-2010 and 2013-2014. 
# 
# From 1994 to 2004 there was an assault weapons ban initially legalized by the Clinton administration under the Violent Crime Control and Law Enforcement Act. This may explain the overall low levels of gun checks until 2004. 
# 
# In January 2008 the Bush administration enacted the National Instant Criminal Background Check Improvement Act whichh required gun background checks to screen for legally declared mentally ill purchasers. This may support the increase in background checks at the time. Perhaps in 2009-2010 the decrease could be attributed to a diversion of would-be purchasers to attempt to purchase a gun. 

# ### Exploratory Analysis - Census Data Set

# Now that we have explored the NICS dataset we will do the same for the Census data set. 

# In[68]:


# Create Histograms of Census Data 
census_clean.hist(bins = 20, figsize=(16,16), layout=(6,4))


# From the histograms we can see most of the data is rightward skewed data. For example land area, population density, population, and number of employers are heavily rightward skewed with the [majority] of variables hovering around the lower extremes of their ranges. On the other hand  high school diploma percentage is skewed leftward. Poverty percentage is the one of the most "normally" distributed variables present in the data set. These observations suggest that 

# ### Research Question 2  (Replace this header name!)

# In[119]:


# Continue to explore the data to address your additional research
#   questions. Add more headers as needed if you have more questions to
#   investigate.


# We will compare/ make correlations between gun background checks and demographic information provided by the census. The Census covers two time periods, 2010 and 2016. Therefore we will create a new gun dataset which only includes the years 2010 and 2016 to make a valid conclusions. 

# In[120]:


nics_clean.head()


# In[121]:


# Create 2010 and 2016 datasets from NICS dataset
temp_nics_2010 = nics_clean.query('year == "2010-01-01"')
nics_2010 = temp_nics_2010.groupby('state')['totals'].sum().reset_index()

temp_nics_2016 = nics_clean.query('year == "2016-01-01"')
nics_2016 = temp_nics_2016.groupby('state')['totals'].sum().reset_index()

# Verify the data was obtained correctly
nics_2016.head()


# In[122]:


# Rename the totals column for both datasets in preparation for merging the datasets
nics_2010.rename(columns = {'totals': 'gun_checks_2010'}, inplace = True)

nics_2016.rename(columns = {'totals': 'gun_checks_2016'}, inplace = True)

#Verify the changes
nics_2010.head()


# In[123]:


# Merge the 2010 and 2016 datasets
nics_2010_2016 = nics_2010.merge(nics_2016, how = 'inner', on = 'state')

#Verify the changes
nics_2010_2016.head()


# In[124]:


# Merge the 2010 and 2016 NICS Dataset with the Census dataset

nics_demographics= nics_2010_2016.merge(census_clean, how = 'inner', on= 'state')
nics_demographics.head()


# In[125]:


nics_demographics.loc[30:43, :]


# Let's calculate the guns per capita for each state in both 2010 and 2016 so we have an equal measure of comparison amonst each state. And this would eliminate population differences 

# In[126]:


#Calculating Guns per Capital in 2010 and 2016
nics_demographics['gun_checks_per_capita_2010'] =  nics_demographics['gun_checks_2010']/ nics_demographics['population_2010']
nics_demographics['gun_checks_per_capita_2016'] =  nics_demographics['gun_checks_2016']/ nics_demographics['population_2016']

nics_demographics.head()


# In[127]:


# States with highest female employment
nics_demographics[['state', 'female_employment_percentage', 'gun_checks_per_capita_2010', 'gun_checks_per_capita_2016']].sort_values(ascending = False, by = 'female_employment_percentage').head()


# Minnesota has the highest female employment and the second lowest gun checks per capita in 2010, but it has the third highest (out of the top 5) number of gun checks per capita in 2016. it nearly doubled the number of gun checks per capita in six years. All of the top five states show an increase in gun checks over the time period. 
# 
# Despite having a much smaller population to Minnesota, Alaska has the highest number of gun checks per capita in 2010. Gun checks ballooned in South Dakota from 2010 to 2016. 

# In[128]:


# States with lowest female employment
nics_demographics[['state', 'female_employment_percentage', 'gun_checks_per_capita_2010', 'gun_checks_per_capita_2016']].sort_values(ascending = True, by = 'female_employment_percentage').head()


# West Virgina has the lowest female employment and consistently has the highest gun checks per capita from 2010 and 2016. It is possible that low levels of female employment could be indicative of high levels of gun checks. However, the low female employment might also be correlated to other structural or geographic fators which are associated with high numbers of gun checks. 

# In[129]:


nics_demographics[['state', 'female_employment_percentage']].plot.bar(x = 'state', y = 'female_employment_percentage', color = 'pink')


# We can observe that female employment is generally >50% across all 50 states, however West Virginia visibly has one of the lowest levels of female employment. 
# 
# Let's see if there is a correlation between number of gun checks and female employment. 

# In[130]:


# Calculate Correlation Coefficient for female employment vs. gun checks in 2010 and 2016
correlation_2010 = nics_demographics['female_employment_percentage'].corr(nics_demographics['gun_checks_2010'])
correlation_2016 = nics_demographics['female_employment_percentage'].corr(nics_demographics['gun_checks_2016'])
print(
f'''
2010 Female Employment Correlation Coefficient: {correlation_2010} 

2016 Female Employment Correlation Coefficient:{correlation_2016}
'''
)


# There is a weak correlation between percentage of female employment and the number of gun checks per capita in 2010 and 2016. Let's see this graphically.

# In[131]:


# Create scatter plot with regression line of female employment percentage vs. gun checks per capita
sns.set(rc={'figure.figsize':(11.7,8.27)})

ax = sns.regplot(
    data = nics_demographics,
    x = 'female_employment_percentage',
    y ='gun_checks_per_capita_2010',
    label = '2010',
    color = '#dda0dd'
)
sns.regplot(
    data = nics_demographics,
    x = 'female_employment_percentage',
    y ='gun_checks_per_capita_2016',
    ax = ax,
    label = '2016',
    color = '#8b668b'
)

plt.xlabel('Female Employment Percentage', fontsize=20)
plt.ylabel('Gun Checks per Capita 2010', fontsize=20)
plt.title("Female Employment vs. Guns per Capita", fontsize = 20)
ax.legend(fontsize = 20)


# There is a negative correlation between female employment and number of gun checks in 2010 and 2016. Let's see what role income plays in number of gun checks. It's possible that simply being employed has a diminishing effect on the number of gun checks. Depending on the result of the regression plot with income, it could also be that higher income is also a deterrent to obtaining guns. 

# In[132]:


# Find states with highest median income
nics_demographics[['state', 'median_income', 'gun_checks_per_capita_2010', 'gun_checks_per_capita_2016']].sort_values(ascending = False, by = 'median_income').head()


# It is interesting that Maryland has the highest median income, this may be the case given it's proximity to the capital and the number of research institutions. Maryland has among the lowest number of gun checks per capita in both 2010 and 2016. This suggests that median income may be strongly associated with low levels of gun checks. It is also possible that as mentioned, Maryland's proximity to the capital and government headquarters could account for the high salaries. 
# 
# Interestingly three of the top five states are on the East Coast. New Jersey and Conneticut are bedroom communities for New York which is known as the financial capital of the country. 

# In[133]:


# Find states with lowest median income
nics_demographics[['state', 'median_income', 'gun_checks_per_capita_2010', 'gun_checks_per_capita_2016']].sort_values(ascending = True, by = 'median_income').head()


# Kentucky has the fifth lowest median income in the country and has nearly 5x the number of gun checks in 2010, and almost 8x the number of checks in 2016. Interestingly, all of the states with the lowest income are southern states. 

# In[134]:


# Compare Median Income to gun checks per capita 2010
sns.set(rc={'figure.figsize':(11.7,8.27)})

ax = sns.regplot(x ='median_income', y ='gun_checks_per_capita_2010', data = nics_demographics, label = '2010', color = '#7a378b')

sns.regplot(x ='median_income', y ='gun_checks_per_capita_2016', data = nics_demographics, ax=ax, label= '2016', color = '#ba55d3')

plt.xlabel('Median Income (Dollars)', fontsize=15)
plt.ylabel('Gun Checks per Capita', fontsize=15)
plt.title("Median Income vs. Guns per Capita", fontsize = 15)
plt.legend(fontsize = 15)
plt.show()


# In[135]:


# Calculate Correlation Coefficients for Median Income vs. gun checks
correlation_2010 = nics_demographics['median_income'].corr(nics_demographics['gun_checks_2010'])
correlation_2016 = nics_demographics['median_income'].corr(nics_demographics['gun_checks_2016'])
print(
f'''
2010 Median Income Correlation Coefficient: {correlation_2010} 

2016 Median Income Correlation Coefficient:{correlation_2016}
'''
)


# While graphically it appears there is a negative correlation between median income and the number of gun checks, in reality there is no correlationi. It will be interesting to see if this is the case when comparing income per capita.

# In[136]:


# Graph income per capita across 50 states
sns.set(rc={'figure.figsize':(11.7,8.27)})

sns.barplot(x= 'state', y='income_per_capita', data = nics_demographics, color='#ba55d3')
plt.ylabel('Income per Capita (Dollars)')
plt.title('Income per Capita Across United States')
plt.xticks(rotation = 90)
plt.show()


# There are wide variations in income per capita among the 50 states, with Arkansas, Mississippi, and West Virginia having some of the lowest incomes per capita. This corresponds to the findings regarding the states with the lowest median income. Similarly, Conneticut was one of the states with the highest median income, however here it has the highest income per capita.

# In[137]:


# Compare income per capita to gun checks per capita in 2010 and 2016
sns.set(rc={'figure.figsize':(11.7,8.27)})

ax = sns.regplot(x ='income_per_capita', y ='gun_checks_per_capita_2010', data = nics_demographics, label = '2010', color = '#8470ff')

sns.regplot(x ='income_per_capita', y ='gun_checks_per_capita_2016', data = nics_demographics, ax=ax, label= '2016', color = '#483d8b')

plt.xlabel('Income per Capita (Dollars)', fontsize=15)
plt.ylabel('Gun Checks per Capita', fontsize=15)
plt.title("Income per Capita vs. Guns per Capita", fontsize = 15)
plt.legend(fontsize = 15)


# In[138]:


# Calculate Correlation Coefficients for Income per Capita vs. gun checks
correlation_2010 = nics_demographics['income_per_capita'].corr(nics_demographics['gun_checks_2010'])
correlation_2016 = nics_demographics['income_per_capita'].corr(nics_demographics['gun_checks_2016'])
print(
f'''
2010 Income per Capita Correlation Coefficient: {correlation_2010} 

2016 Income per Capita Correlation Coefficient:{correlation_2016}
'''
)


# Surprisingly there is a weak correlation between income per capita and number of gun checks in 2010, which is borderline in 2016. It would require further investigation to understand why this occured.However our ability to do so is limited because the Census data set only provides population data for two years (2010 and 2016). If we had yearly population data we could compare income per capita vs. the yearly number of gun checks per capita. In addition, here income per capita is was only evaluated for **2010-2016**. We would need yearly income per capita data to accurately perform this analysis. 

# In[139]:


# Plot Senior Population in 2010 vs. 2016
ax = sns.barplot(y= 'percent_over_65_2010', x = 'state', data = nics_demographics, label = '2010', color='purple')

sns.barplot(y= 'percent_over_65_2016', x = 'state', data = nics_demographics, ax=ax, label='2016', color = 'blue', alpha = .5)
plt.title('Population over 65')
plt.ylabel('Percent Population over 65 (%)')
plt.xlabel('State')
plt.xticks(rotation = 90)
plt.legend()
#plt.show()


# Senior populations rose across all states from 2010 to 2016. Alaska and Utah consistently had the lowest senior populations between 2010 and 2016. Maine and Florida have the highest senior poppulations. It is interesting to note that A

# In[ ]:


# Compare Senior Population to gun checks per capita
sns.set(rc={'figure.figsize':(11.7,8.27)})

ax = sns.regplot(x ='percent_over_65_2010', y ='gun_checks_per_capita_2010', data = nics_demographics, color = '#6959cd', label = '2010')

sns.regplot(x ='percent_over_65_2016', y ='gun_checks_per_capita_2016', data = nics_demographics, ax=ax, color = '#cd96cd', label = '2016')
plt.xlabel('Population over 65 (%)', fontsize=12)
plt.ylabel('Gun Checks per Capita', fontsize=12)
plt.title("Senior Population vs. Guns per Capita")
plt.legend()
sns.set_theme()
plt.show()


# In 2010 there appears to be a weak negative correlation between the prevalence of seniors in a state and the number of gun checks per capita. However, this correlation seems to dissapear in 2016, much as was the case when evaluating the correlation between income and number of gun checks per capita. The limitations of the data mentioned previously apply here, the dataset is too small to make accurate conclusions. We would need more years of Census data to be more accurate. Let's calculate the correlation coefficients to verify the observations noted visibly. 

# In[ ]:


# Calculate Correlation Coefficients for Percentage of Seniors vs. Gun Checks
correlation_2010 = nics_demographics['percent_over_65_2010'].corr(nics_demographics['gun_checks_2010'])
correlation_2016 = nics_demographics['percent_over_65_2016'].corr(nics_demographics['gun_checks_2016'])
print(
f'''
2010 Senior Population Correlation Coefficient: {correlation_2010} 

2016 Senior Population Correlation Coefficient:{correlation_2016}
'''
)


# While visually there appears to be a weak negative correlation between the prevalence of seniors in the population and the number of gun checks, the correlation coefficients are not significant. 

# In[ ]:


# Graph Population with a high school degree vs. bachelors degree
sns.set(rc={'figure.figsize':(11.7,8.27)})
ax = sns.barplot(y= 'hs_diploma_percentage', x = 'state', data = nics_demographics, label='high school diploma', color = '#ffb6c1')

sns.barplot(y= 'bachelors_degree_percentage', x = 'state', data = nics_demographics, ax=ax, label='bachelors degree', color = '#5d478b', alpha = .7)
plt.title('Prevalence of High School and Bachelors Degrees in US')
plt.ylabel('Percent of Population (%)')
plt.xlabel('State')
plt.xticks(rotation = 90)
plt.legend()


# The vast majority of Americans have high school degrees, however the rates of bachelors degrees are far lower. Few states have levels of bachelors degrees above 40%. Massachusetts has the highest rate of bachelors degrees, as do Colorado, Conneticut, and Massachusetts. Given that high school diplomas are so prevalent in the US, it is possible to hypothesize that there would be either a weak correlation or no correlation between the level of high school degrees and the number of gun checks. On the other hand, there is more variability amoung the rate of bachelors degrees, and so it is reasonable to predict that there would be a stronger correlation between the prevalence of bachelors degrees and the number of gun checks. 

# In[ ]:


# Compare high school degree percentage to gun checks per capita
ax = sns.regplot(x ='hs_diploma_percentage', y ='gun_checks_per_capita_2010', data = nics_demographics, color = '#6959cd', label = '2010')

sns.regplot(x ='hs_diploma_percentage', y ='gun_checks_per_capita_2016', data = nics_demographics, ax=ax, color = '#cd96cd', label = '2016')
plt.xlabel('Percentage High School Diplomas(%)', fontsize=12)
plt.ylabel('Gun Checks per Capita', fontsize=12)
plt.title("Rate of High School Diplomas vs. Guns per Capita")
plt.legend()
sns.set_theme()
plt.show()


# In[ ]:


# Find correlation coefficient for high school diplomas vs. gun checks per capita
correlation_2010 = nics_demographics['hs_diploma_percentage'].corr(nics_demographics['gun_checks_2010'])
correlation_2016 = nics_demographics['hs_diploma_percentage'].corr(nics_demographics['gun_checks_2016'])
print(
f'''
2010 Rate of High School Diplomas Correlation Coefficient: {correlation_2010} 

2016 Rate of High School Diplomas Coefficient:{correlation_2016}
'''
)


# There is a moderate negative correlation between the prevalence of a high school diploma and the number of gun checks per capita. 

# In[ ]:


# Compare bachelors degree percentage to gun checks per capita
ax = sns.regplot(x ='bachelors_degree_percentage', y ='gun_checks_per_capita_2010', data = nics_demographics, color = '#6959cd', label = 'Gun Checks per Capita 2010')

sns.regplot(x ='bachelors_degree_percentage', y ='gun_checks_per_capita_2016', data = nics_demographics, ax=ax, color = '#cd96cd', label = 'Gun Checks per Capita 2016')
plt.xlabel('Percentage Bachelors Degrees (%)', fontsize=12)
plt.ylabel('Gun Checks per Capita', fontsize=12)
plt.title("Rate of Bachelors Degree vs. Guns per Capita")
plt.legend()
sns.set_theme()
plt.show()


# In[ ]:


# Find correlation coefficient for high school diplomas vs. gun checks per capita
correlation_2010 = nics_demographics['bachelors_degree_percentage'].corr(nics_demographics['gun_checks_2010'])
correlation_2016 = nics_demographics['bachelors_degree_percentage'].corr(nics_demographics['gun_checks_2016'])
print(
f'''
2010 Rate of Bachelors Degrees Correlation Coefficient: {correlation_2010} 

2016 Rate of Bachelors Degrees Coefficient:{correlation_2016}
'''
)


# While visually there appears to be a negative correlation between the rate of bachelors degrees and gun checks, mathematically there is no correlation in this sample. However we cannot come to the conclusion regarding a correlation in the population without performing hypothesis testing. We are limited by the size of the sample, and possible outliers that are skewing the data.

# In[ ]:


# Graph Uninsured Percentage across 50 states
sns.set(rc={'figure.figsize':(11.7,8.27)})

sns.barplot(x= 'state', y='uninsured_percentage', data = nics_demographics, color='#ba55d3')
plt.ylabel('Percent Unisured (%)')
plt.title('Level of Unisured Americans')
plt.xticks(rotation = 90)
plt.show()


# In[ ]:


# Compare uninsured percentage to gun checks per capita
ax = sns.regplot(x ='uninsured_percentage', y ='gun_checks_per_capita_2010', data = nics_demographics, color = '#6959cd', label = 'Gun Checks per Capita 2010')

sns.regplot(x ='uninsured_percentage', y ='gun_checks_per_capita_2016', data = nics_demographics, ax=ax, color = '#cd96cd', label = 'Gun Checks per Capita 2016')
plt.xlabel('Percent Uninsured(%)', fontsize=12)
plt.ylabel('Gun Checks per Capita', fontsize=12)
plt.title("Level of Uninsured vs. Guns per Capita")
plt.legend()
sns.set_theme()
plt.show()


# In[ ]:


# Find correlation coefficient for uninsured population vs. gun checks per capita

correlation_2010 = nics_demographics['uninsured_percentage'].corr(nics_demographics['gun_checks_2010'])
correlation_2016 = nics_demographics['uninsured_percentage'].corr(nics_demographics['gun_checks_2016'])
print(
f'''
2010 Uninsured population Correlation Coefficient: {correlation_2010} 

2016 Uninsured population Coefficient:{correlation_2016}
'''
)


# <a id='conclusions'></a>
# ## Conclusions
# 
# > **Tip**: Finally, summarize your findings and the results that have been performed in relation to the question(s) provided at the beginning of the analysis. Summarize the results accurately, and point out where additional research can be done or where additional information could be useful.
# 
# > **Tip**: Make sure that you are clear with regards to the limitations of your exploration. You should have at least 1 limitation explained clearly. 
# 
# > **Tip**: If you haven't done any statistical tests, do not imply any statistical conclusions. And make sure you avoid implying causation from correlation!
# 
# > **Tip**: Once you are satisfied with your work here, check over your report to make sure that it is satisfies all the areas of the rubric (found on the project submission page at the end of the lesson). You should also probably remove all of the "Tips" like this one so that the presentation is as polished as possible.
# 
# ## Submitting your Project 
# 
# > **Tip**: Before you submit your project, you need to create a .html or .pdf version of this notebook in the workspace here. To do that, run the code cell below. If it worked correctly, you should see output that starts with `NbConvertApp] Converting notebook`, and you should see the generated .html file in the workspace directory (click on the orange Jupyter icon in the upper left).
# 
# > **Tip**: Alternatively, you can download this report as .html via the **File** > **Download as** submenu, and then manually upload it into the workspace directory by clicking on the orange Jupyter icon in the upper left, then using the Upload button.
# 
# > **Tip**: Once you've done this, you can submit your project by clicking on the "Submit Project" button in the lower right here. This will create and submit a zip file with this .ipynb doc and the .html or .pdf version you created. Congratulations!

# In[ ]:


# Running this cell will execute a bash command to convert this notebook to an .html file
get_ipython().system('python -m nbconvert --to html Investigate_a_Dataset.ipynb')

