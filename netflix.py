import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("netflix_titles.csv",encoding="latin1")
print(df.head())
null_values = df.isnull().sum()
print(null_values)
df['director'].fillna('Unknown', inplace=True)
null_values = df.isnull().sum()
print(null_values)
df.dropna(subset=['cast'], inplace=True)
print(df.isnull().sum())
df['country'].fillna('Unknown', inplace=True)
print(df.isnull().sum())

#Deleting the rows of missing date
df.dropna(subset=['date_added'], inplace=True)
df.dropna(subset=['rating'], inplace=True)
df.dropna(subset=['duration'], inplace=True)
print(df.isnull().sum())
print(df.nunique())

# How many unique values are there in the 'type' and 'rating' columns?
print(df['type'].value_counts())
# How many unique values are there in the 'rating' column?
print(df['rating'].value_counts())

print(df['release_year'].isnull().sum())
print(df['release_year'].value_counts().sort_index())

print(df.shape)
print(df.info())
print(df.describe())
print(df['country'].value_counts())


no_of_duplicates = df.duplicated().sum()
print(f"Number of duplicate rows: {no_of_duplicates}")

# Analysis of the 'listed_in' column to find the most common genres
genere_counts = df['listed_in'].str.split(",").explode().value_counts()
print(genere_counts.sort_values(ascending=False).head())

# Excluding unknown directors and counting the top 10 directors
top_directors = df[df['director'] != 'Unknown']['director'].value_counts().head(10)
print(top_directors)

print(df['release_year'].value_counts().sort_values(ascending=False).head(10))

# Seperating the type into movies and TV shows
movies_df = df[df['type']=="Movie"]
print(movies_df.to_string())
print(movies_df.columns)
tv_shows_df = df[df['type'] == "TV Show"]
print(tv_shows_df.head())


movies_df['minutes'] = movies_df['duration'].str.extract(r'(\d+)').astype(int)
# extracting only the number from strings for duration column
print(movies_df['minutes'].head())
avg_movie_duration = movies_df['minutes'].mean()
print(f"Average movie duration: {avg_movie_duration:.2f} minutes")
longest_movie_duration = movies_df['minutes'].max()
print(f"The Longest movie duration: {longest_movie_duration:.2f}")
shortest_movie_duration = movies_df['minutes'].min()
print(f"The Shortest movie duration: {shortest_movie_duration:.2f}")

#Changing the date_added column format to datetime from object
df['date_added'] = df['date_added'].str.strip() 
#strip() removes the leading and trailing spaces
df['date_added'] = pd.to_datetime(df['date_added'],
                                  format='mixed',
                                  dayfirst=True # Format will be as dd-mm-yyyy
                                  )
print(df['date_added'].dtype)
#Extracting the year from date_added
df['year_added'] = df['date_added'].dt.year
print(df['year_added'].head())

#Month wise
df['month_added'] = df['date_added'].dt.month_name()
# dt helps the pandas to understand that we are working with datetime
print(df['month_added'])

# Counting titles on every month
month_counts = df['month_added'].value_counts()
print(month_counts) #The months will be unordered

month_order = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]
month_counts = month_counts.reindex(month_order) 
# This will reorder the months from Jan to Dec
print(month_counts)

label_props = dict(
    fontsize=15,
    family = "Times New Roman",
    fontweight = "bold",
    color="#6d0d03"
)

# Visualizing Movie vs TV show
sns.countplot(data=df, y='type',color="#115b6d")
plt.title("Movies Vs TV Shows")
plt.xlabel("Title Count",**label_props)
plt.ylabel("Content Type",**label_props)
plt.legend()
plt.show()

# Insights:
#     Movies make up the majority of Netflix's content library, significantly outnumbering TV Shows.

# Visualizing which genere performing good

genres = df['listed_in'].str.split(',').explode()
genres = genres.str.strip() #Removing trailing and leading space
print(genres)
genre_counts = genres.value_counts().head()
print(genre_counts)

# by default, the value_counts() function in pandas sorts the results in descending order.
#Plotting

sns.barplot(x = genre_counts.values, # Titles
            y = genre_counts.index, # No of times it appeared
            color='#4b6d06'
            )
plt.xticks(rotation = 45, ha='right')
# 'ha' stands for Horizontal Alignment.
    # When you rotate the X-axis labels, they can overlap or look awkward. ha='right' tells Matplotlib to align the right edge of each label with its tick mark.

plt.title("Top Performing Genre",**label_props)
plt.xlabel("Count",**label_props)
plt.ylabel("Genre",**label_props)

# Insight 1

# International Movies is the most common genre on Netflix, indicating a strong focus on global content.

# Insight 2

# Dramas and Comedies are among the most frequently available genres, showing that Netflix offers a wide variety of entertainment content.

# Insight 3

# The top 10 genres account for a significant portion of Netflix's catalog, reflecting the platform's emphasis on diverse viewing preferences.

# Visualizing the Top countries that contributes most Netflix content
country_counts = df[df['country']!="Unknown"]['country'].value_counts().head(10)
# Excluding the unknowns

sns.barplot(x=country_counts.values,
              y = country_counts.index,
              color="#296d53")
plt.xticks(rotation = 45, ha='right')
plt.title("Top Performing Country",**label_props)
plt.xlabel("Titles Count",**label_props)
plt.ylabel("Country",**label_props)

# Ratings Distribution Analysis

ratings = df['rating'].value_counts().head(10)
sns.barplot(x = ratings.index,
            y = ratings.values,
            color="#442424")
plt.title("Ratings Distribution Analysis",**label_props)
plt.xlabel("Ratings",**label_props)
plt.ylabel("Number of Titles",**label_props)

#  Insight 1

# TV-MA is the most common content rating on Netflix, indicating that a large portion of the catalog is intended for mature audiences.

#  Insight 2

# TV-14 is the second most common rating, showing that Netflix also offers a substantial amount of content suitable for teenagers and older viewers.

#  Insight 3

# Ratings such as NR and TV-G appear much less frequently, suggesting that Netflix has comparatively fewer unrated or general-audience titles.

# Visualizing Titles Added Per Year

year_counts = df['year_added'].value_counts()
print(year_counts)

plt.plot(year_counts.index, year_counts.values,
         marker = "P",
         color = "#4a7400")
plt.xticks(range(2008,2022,2)) # Checking for every 2 years from 2008 to 2022
plt.title("Titles Added Per Year",**label_props)
plt.xlabel("Year",**label_props)
plt.ylabel("No of Titles",**label_props)

# Insight 1

# The number of titles added to Netflix increased gradually from 2008 to 2015, indicating slow expansion during the early years.

#  Insight 2

# Netflix experienced rapid growth from 2016 to 2019, with the highest number of titles added in 2019.

#  Insight 3

# After reaching its peak in 2019, the number of titles added declined in 2020 and 2021, showing a slowdown in content additions.

# Visualizing Titles added per month

print(month_counts)
month_counts.index = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
] # For Good alignment using short form
sns.barplot(x=month_counts.index, y=month_counts.values, color="#7b0067")
plt.tight_layout()
plt.title("Titles added per month",**label_props)
plt.xlabel("Months",**label_props)
plt.ylabel("No of Titles",**label_props)

# Insight 1

# July and December recorded the highest number of titles added, indicating that Netflix released more content during these months.

# Insight 2

# February had the lowest number of titles added, making it the month with the fewest content additions.

# Insight 3

# The number of titles added remained relatively consistent throughout most months, suggesting that Netflix follows a steady content release strategy rather than concentrating releases in only a few months.

# Creating single dashboard

fig, axes = plt.subplots(3,2,figsize=(18,15))
plt.suptitle("Netflix Data Analysis Dashboard",
             fontsize = 22,
             fontweight="bold",
             color = "#b20710")

#Creates multiple charts in one figure.
# 3 → 3 rows
# 2 → 2 columns

#Chart 1
sns.countplot(
    data=df,
    y='type',
    color="#115b6d",
    ax=axes[0,0]
)

axes[0,0].set_title("Movies vs TV Shows")
axes[0,0].set_xlabel("Title Count")
axes[0,0].set_ylabel("Content Type")

#Chart 2
sns.barplot(
    x=genre_counts.values,
    y=genre_counts.index,
    color="#4b6d06",
    ax=axes[0,1]
)

axes[0,1].set_title("Top Genres")
axes[0,1].set_xlabel("Count")
axes[0,1].set_ylabel("")

#Chart 3
sns.barplot(
    x=country_counts.values,
    y=country_counts.index,
    color="#296d53",
    ax=axes[1,0]
)

axes[1,0].set_title("Top Countries")

#Chart 4
sns.barplot(
    x=ratings.index,
    y=ratings.values,
    color="#442424",
    ax=axes[1,1]
)

axes[1,1].tick_params(axis='x', rotation=45)

axes[1,1].set_title("Ratings")

#Chart 5
axes[2,0].plot(
    year_counts.index,
    year_counts.values,
    marker='P',
    color="#4a7400"
)

axes[2,0].set_title("Titles Added Per Year")
axes[2,0].set_xticks(range(2008,2022,2))

#Chart 6
sns.barplot(
    x=month_counts.index,
    y=month_counts.values,
    color="#7b0067",
    ax=axes[2,1]
)

axes[2,1].set_title("Titles Added Per Month")
plt.tight_layout(rect=[0, 0, 1, 0.96])
#Writing the cleaned dataset
df.to_csv("Netflix_cleaned_dataset.csv", index=False)