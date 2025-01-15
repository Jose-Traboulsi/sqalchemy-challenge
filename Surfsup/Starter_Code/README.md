# sqalchemy-challenge

I referred to class materials and used AI when needed to fix typos or errors on query structure. I also booked tutoring sessions to go over the class materials to enhace my
understanding of it.

Exploratory Precipitation Analysis
The key here is to obtain the last date in the data so we can calculate the starting date for the analysis by using the datetime library.
We make a query for the date table, organize it in descending order, and then use the .first() function to get the first row of data (i.e. the most recent date).
We then use timedelta to find the start date. Months are not an allowed parameter within the datetime library's timedelta() fuction, so the key here was to use 365 days.
We sort the dates in descending order so we can plot the values, since our x axis are the dates.
I used the .plot function directly in the sorted data_frame as the output was clearner (i.e., when I tried using .plt method, the legend on the graph was not readable since it
showed all dates in the series vs. a few sample ones, like the version provided in the solution).
To obtain the summary statistics, we use the .describe() function. For visual appeal, I converted the results into a data frame.

Exploratoy Station Analysis
To find out the total number of stations, we make a query on station class using for station names and the total row count in this column.
For the latter, we use .func.count. I added .scalar() so we can extract the result, but it was not needed to find the solution.
To rank stations by number of observations, the trick is to use group by on a query of station names and the count of measurements so we can get the total count per station. We add .desc() to specificy the results should be on descending order by observation count. From the results we can take the "most active" station id ('USC00519281').
With the code in hand, we can proceed to calculate the max, min and avg. temperatures at this station.
Next, we can use this id to filter the results on a query of measurement dates combined with the .max() function to extract the most recent observation date for this station.
With this date, we can then proceed to obtain results from there onwards that we can use in the histogram. I have added some comments on my Jupyter Notebook to explain some of the logic behind my code.

