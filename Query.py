import pandas as pd
from constant import *

# Track sales per day, month, quarter, year?


ex_1 = '''The store's sales performance over the span of five years showcases varying trends. In 2009, the store recorded 454 invoices, resulting in total sales of 449.46. However, the following year, 2010, marked a notable upturn with 455 invoices and a substantial increase in total sales, reaching 481.45. This surge propelled the store to the top rank in sales performance. Despite a slight decline in total sales in 2011, down to 442, the total sales remained relatively robust at 469.58. The trend continued upwards in 2012, when the store experienced a rise in both the number of invoices (447) and total sales (477.53). However, by 2013, the number of invoices had reverted to 442, resulting in a decline in total sales to 450.58. This fluctuation in sales over the years indicates a varied trend in the store's performance, with notable highs and a subsequent decline in sales figures.
The store can formulate appropriate strategies regarding staffing, products, incentives, and well-targeted advertising and communication campaigns to navigate these fluctuations more effectively.
'''

ex_2 = '''The quarterly breakdown of sales reveals distinct patterns across the four quarters. Quarter 2 emerges as the standout period, boasting the highest sales performance among the quarters, marked by 566 invoices and total sales amounting to 592.34, securing the top position in sales rank. Following closely, Quarter 3 presents a strong performance with 560 invoices and 584.40 in total sales. Quarter 1, recording 558 invoices and 583.42 in total sales, while Quarter 4, with 556 invoices and 568.44 in total sales, exhibited a relatively lower sales performance among the quarters.'''

ex_3 = '''The breakdown of sales by month presents varying performances throughout the year. January emerged as the top-performing month, with 188 invoices totalling 201.12 in sales, securing the first rank in sales. June closely followed with 190 invoices and 201.1 in sales, claiming the second spot. April demonstrated a strong performance as well, with 186 invoices and 198.14 in sales, ranking third among the months. Meanwhile, February, November, and December displayed relatively lower sales performances, ranking towards the bottom with fewer invoices and lower total sales figures.
Implementing marketing campaigns during months with higher revenue can significantly enhance business effectiveness. Specifically, months like January, April, and June have shown substantial revenue. Focusing marketing efforts during these periods can attract customer attention and increase sales opportunities. By optimizing campaigns during these motivated buying periods, the store can leverage these revenue surges to achieve higher effectiveness from the marketing strategy.
'''

query_1_quarter = '''select Quarter, Year, 
    sum(ExtendedPrice) as 'Total Sales'
    from star.FactSales as fs
    join star.DimDate as dd
    on fs.InvoiceDateID = dd.DateID
    group by Quarter, Year
    order by Year, Quarter'''

req_1_quarter = pd.merge(df_FactSales, df_DimDate, left_on='InvoiceDateID', right_on='DateID')
req_1_quarter = req_1_quarter.groupby(['Quarter', 'Year']).agg({'ExtendedPrice': 'sum'}).reset_index().rename(columns={'ExtendedPrice':'Total Sales'})

query_1_day = '''select FullDate, Year, 
    sum(ExtendedPrice) as 'Total Sales'
from star.FactSales as fs
join star.DimDate as dd
on fs.InvoiceDateID = dd.DateID
group by FullDate, Year
order by FullDate'''

req_1_day = pd.merge(df_FactSales, df_DimDate, left_on='InvoiceDateID', right_on='DateID')
req_1_day = req_1_day.groupby(['FullDate', 'Year']).agg({'ExtendedPrice': 'sum'}).reset_index().rename(columns={'ExtendedPrice':'Total Sales'})

query_1_month = '''select MonthOfYear, MonthName, Year, 
    sum(ExtendedPrice) as 'Total Sales'
from star.FactSales as fs
join star.DimDate as dd
on fs.InvoiceDateID = dd.DateID
group by MonthOfYear, MonthName, Year
order by Year, MonthOfYear'''

req_1_month = pd.merge(df_FactSales, df_DimDate, left_on='InvoiceDateID', right_on='DateID')
req_1_month = req_1_month.groupby(['MonthOfYear', 'MonthName','Year']).agg({'ExtendedPrice': 'sum'}).reset_index().rename(columns={'ExtendedPrice':'Total Sales'})

query_1_year = '''select Year, 
    sum(ExtendedPrice) as 'Total Sales'
from star.FactSales as fs
join star.DimDate as dd
on fs.InvoiceDateID = dd.DateID
group by Year
order by Year'''

req_1_year = pd.merge(df_FactSales, df_DimDate, left_on='InvoiceDateID', right_on='DateID')
req_1_year = req_1_year.groupby(['Year']).agg({'ExtendedPrice': 'sum'}).reset_index().rename(columns={'ExtendedPrice':'Total Sales'})

#  Which album has the most listeners?

ex_2_1 = '''Rock seems to dominate the engagement metrics, with several albums accumulating high listen counts, such as "Greatest Hits," "Chronicle," and "The Best Of" compilations. Latin and Alternative & Punk also maintain a significant presence in the engagement numbers, with albums like "Acústico," "International Superhits," and various compilations receiving notable listens.
TV show soundtracks, especially from "Lost" and "The Office," have garnered substantial engagement, indicating the popularity of their music within these series. Additionally, albums from different genres, including Alternative & Punk, Metal have their own share of engagement across various albums.
'''

query_2 = '''select top %s 
    fl.AlbumId, 
        da.AlbumTitle, 
    sum(fl.PlaylistTrackViews) as [Views]
from star.FactListen as fl
join star.DimAlbum as da
on fl.AlbumId = da.AlbumId
group by fl.AlbumId, da.AlbumTitle'''

req_2 = pd.merge(df_FactListen, df_DimAlbum, how='inner', on='AlbumId')
req_2 = req_2.groupby(['AlbumId', 'AlbumTitle']).agg({'PlaylistTrackViews': 'sum'}).reset_index().rename(columns={'PlaylistTrackViews':'Views'})

query_2_1 = '''	select top %s 
		fl.AlbumId, 
		count(TrackId) as 'No of Track', 
		sum(fl.Milliseconds) as 'Song Duration', 
        da.AlbumTitle, 
        sum(fl.PlaylistTrackViews) as [Views]
	from star.FactListen as fl
	join star.DimAlbum as da
	on fl.AlbumId = da.AlbumId
	join star.DimGenre as dg
	on fl.GenreId = dg.GenreId
	group by fl.AlbumId, da.AlbumTitle'''

req_2_1 = pd.merge(df_FactListen, df_DimAlbum, how='inner', on='AlbumId')
req_2_1 = pd.merge(req_2_1, df_DimGenre, how='inner', on='GenreId')
req_2_1 = req_2_1.groupby(['AlbumId', 'AlbumTitle']).agg({
    'TrackId': 'count',
    'Milliseconds': 'sum',
    'PlaylistTrackViews': 'sum'
}).reset_index()

# Rename the columns
req_2_1.rename(columns={
    'TrackId': 'No of Track',
    'Milliseconds': 'Song Duration',
    'PlaylistTrackViews': 'Views'
}, inplace=True)

#  Which customers regularly buy music?
query_3_monthyear = '''with temp as
(
    select CustomerId, Year, Count(distinct MonthOfYear) as 'Month'
    from star.FactGenre as fg
    join star.DimDate as dd
    on dd.DateID = fg.OrderDateID
    group by CustomerId, Year
)
select temp.CustomerId, dc.CustomerName, Year, Month
from temp
join star.DimCustomer as dc
on dc.CustomerId = temp.CustomerId
order by temp.CustomerId'''

df_temp = pd.merge(df_FactGenre, df_DimDate, how='inner', left_on='OrderDateID', right_on='DateID')
df_temp = df_temp.groupby(['CustomerId', 'Year']).agg({'MonthOfYear': 'nunique'}).reset_index()
df_temp.rename(columns={'MonthOfYear': 'Month'}, inplace=True)
req_3_monthyear = pd.merge(df_temp, df_DimCustomer, how='inner', on='CustomerId')
req_3_monthyear = req_3_monthyear[['CustomerId', 'CustomerName', 'Year', 'Month']].sort_values('CustomerId')

query_3_year = '''with temp as 
(
    select CustomerId, Count(distinct Year) as Year
    from star.FactGenre as fg
    join star.DimDate as dd
    on dd.DateID = fg.OrderDateID
    group by CustomerId
)
select top %s temp.CustomerId, dc.CustomerName, Year
from temp
join star.DimCustomer as dc
on dc.CustomerId = temp.CustomerId
order by temp.CustomerId
'''

df_temp = pd.merge(df_FactGenre, df_DimDate, how='inner', left_on='OrderDateID', right_on='DateID')

df_temp = df_temp.groupby('CustomerId').agg({'Year': 'nunique'}).reset_index()

req_3_year = pd.merge(df_temp, df_DimCustomer, how='inner', on='CustomerId')
req_3_year = req_3_year[['CustomerId', 'CustomerName', 'Year']].sort_values('CustomerId')

#  Which customer spends the most money for buying album?
ex_4_1 = '''These key customers form the backbone of the store's sales, highlighting their substantial contributions to its revenue stream. Understanding and nurturing these relationships becomes paramount. By offering tailored experiences, exclusive perks, or personalized incentives, the store can solidify these connections, potentially encouraging increased spending and long-term loyalty. Analyzing what drives their loyalty and applying similar strategies to other segments of the customer base could amplify overall sales. 
Additionally, while these top customers hold significant value, diversification remains crucial. Exploring opportunities to attract new segments or expanding products and services can mitigate dependency on a handful of clients.
'''
query_4 = '''select top %s fs.CustomerId, 
    CustomerName, 
    count(InvoiceId) as 'Total No of invoices',
    sum(ExtendedPrice) as 'Total Sales'
from star.FactSales as fs 
join star.DimCustomer as dc 
on fs.CustomerId = dc.CustomerId 
group by fs.CustomerId, CustomerName 
order by 'Total Sales' desc'''

req_4 = pd.merge(df_FactSales, df_DimCustomer, how='inner', on='CustomerId')

# Group by 'CustomerId' and 'CustomerName', and calculate count of 'InvoiceId' and sum of 'ExtendedPrice'
req_4 = req_4.groupby(['CustomerId', 'CustomerName']).agg({
    'InvoiceId': 'count',
    'ExtendedPrice': 'sum'
}).reset_index()
req_4.rename(columns={'InvoiceId': 'Total No of invoices', 'ExtendedPrice': 'Total Sales'}, inplace=True)
req_4 = req_4.sort_values('Total Sales', ascending=False)
req_4

#  Which employee helps achieve invoices the most?

ex_5_1 = '''Among the three individuals in the Sales Support Agent department, Jane Peacock leads with a total invoice of 796 and total sales of 833.04, followed closely by Margaret Park with a total invoice of 760 and total sales of 775.40. Steve Johnson recorded a total invoice of 684 and total sales of 720.16. As for the remaining individuals in different departments—Andrew Adams, Laura Callahan, Michael Mitchell, Nancy Edwards, and Robert King—specific data for total invoices and sales aren't available'''

query_5 = '''select de.EmployeeId, de.EmployeeName, count(InvoiceId) as 'Total Invoices'
from star.FactSales as fs
right join star.DimEmployee as de
on de.EmployeeId = fs.EmployeeId
group by de.EmployeeId,de.EmployeeName'''

req_5 = pd.merge(df_DimEmployee, df_FactSales, how='right', on='EmployeeId')
# Group by 'EmployeeId' and 'EmployeeName', and calculate count of 'InvoiceId'
req_5 = req_5.groupby(['EmployeeId', 'EmployeeName']).agg({'InvoiceId': 'count'}).reset_index()
req_5.rename(columns={'InvoiceId': 'Total Invoices'}, inplace=True)

query_5_time = '''select 
    fs.EmployeeId, 
    EmployeeName, 
    FullDate, 
    MonthofYear, Year,
    count(InvoiceID) as 'Total Invoices'
from star.FactSales as fs
join star.DimEmployee as de
on de.EmployeeId = fs.EmployeeId
join star.DimDate as dd
on dd.DateID = fs.InvoiceDateID
group by fs.EmployeeId, EmployeeName, FullDate, MonthofYear, Year
order by fs.EmployeeId'''

req_5_time = pd.merge(df_FactSales, df_DimEmployee, how='inner', on='EmployeeId')
req_5_time = pd.merge(req_5_time, df_DimDate, how='inner', left_on='InvoiceDateID', right_on='DateID')

# Group by 'EmployeeId', 'EmployeeName', 'FullDate', 'MonthofYear', 'Year', and calculate count of 'InvoiceID'
req_5_time = req_5_time.groupby(['EmployeeId', 'EmployeeName', 'FullDate', 'MonthOfYear', 'Year']).agg({'InvoiceId': 'count'}).reset_index()
req_5_time.rename(columns={'InvoiceId': 'Total Invoices'}, inplace=True)

query_5_year = '''with temp as
(
    select EmployeeId, Year, MonthOfYear, 
        count(fs.InvoiceId) as Total_Invoices, 
        sum(fs.ExtendedPrice) as Total_Sales
	from star.FactSales as fs
	join star.DimDate as dd
	on dd.DateID = fs.InvoiceDateID
	group by EmployeeId, Year, MonthOfYear
)
select temp.EmployeeId, de.EmployeeName, 
    MonthOfYear,Year, Total_Invoices, Total_Sales
from temp
join star.DimEmployee as de
on de.EmployeeId = temp.EmployeeId
order by temp.EmployeeId, MonthOfYear, Year'''

df_temp = pd.merge(df_FactSales, df_DimDate, how='inner', left_on='InvoiceDateID', right_on='DateID')

# Group by 'EmployeeId', 'Year', 'MonthOfYear', and calculate count of 'InvoiceId' and sum of 'ExtendedPrice'
df_temp = df_temp.groupby(['EmployeeId', 'Year', 'MonthOfYear']).agg({
    'InvoiceId': 'count',
    'ExtendedPrice': 'sum'
}).reset_index()
df_temp.rename(columns={'InvoiceId': 'Total_Invoices', 'ExtendedPrice': 'Total_Sales'}, inplace=True)

# Merge with the 'DimEmployee' DataFrame on 'EmployeeId'
req_5_year = pd.merge(df_temp, df_DimEmployee, how='inner', on='EmployeeId')
req_5_year = req_5_year[['EmployeeId', 'EmployeeName', 'MonthOfYear', 'Year', 'Total_Invoices', 'Total_Sales']].sort_values(['EmployeeId', 'MonthOfYear', 'Year'])

#  Which employee has the highest sales revenue?

ex_6 = '''From 2009 to 2013, Margaret Park consistently secured a prominent spot as the top sales-generating employee for three out of these five years. Her sales performance remained strong, peaking in 2012 with a total of $197.2. Jane Peacock held the top position twice during these years, notably in 2011 and 2013, indicating a consistent contribution to sales. Steve Johnson consistently ranked third across these years, showing a stable performance but falling slightly behind Park and Peacock in terms of overall sales. And for each year, the productivity of employees will vary, based on which the store will have appropriate reward policies to encourage them.'''

query_6 = '''select de.EmployeeId, de.EmployeeName, sum(fs.ExtendedPrice) as Total_Sales
from star.FactSales as fs
right join star.DimEmployee as de
on de.EmployeeId = fs.EmployeeId
group by de.EmployeeId, de.EmployeeName'''

req_6 = pd.merge(df_DimEmployee, df_FactSales, how='right', on='EmployeeId')

# Group by 'EmployeeId' and 'EmployeeName', and calculate sum of 'ExtendedPrice'
req_6 = req_6.groupby(['EmployeeId', 'EmployeeName']).agg({'ExtendedPrice': 'sum'}).reset_index()
req_6.rename(columns={'ExtendedPrice': 'Total_Sales'}, inplace=True)

query_6_time = '''select 
    fs.EmployeeId, 
    EmployeeName, 
    FullDate, 
    MonthofYear, Year,
    sum(fs.ExtendedPrice) as Total_Sales
from star.FactSales as fs
join star.DimEmployee as de
on de.EmployeeId = fs.EmployeeId
join star.DimDate as dd
on dd.DateID = fs.InvoiceDateID
group by fs.EmployeeId, EmployeeName, FullDate, MonthofYear, Year
order by fs.EmployeeId'''

req_6_time = pd.merge(df_FactSales, df_DimEmployee, how='inner', on='EmployeeId')
req_6_time = pd.merge(req_6_time, df_DimDate, how='inner', left_on='InvoiceDateID', right_on='DateID')

# Group by 'EmployeeId', 'EmployeeName', 'FullDate', 'MonthofYear', 'Year', and calculate sum of 'ExtendedPrice'
req_6_time = req_6_time.groupby(['EmployeeId', 'EmployeeName', 'FullDate', 'MonthOfYear', 'Year']).agg({'ExtendedPrice': 'sum'}).reset_index()
req_6_time.rename(columns={'ExtendedPrice': 'Total_Sales'}, inplace=True)

query_6_year = '''with temp as
(
    select EmployeeId, Year, MonthOfYear, 
        sum(fs.ExtendedPrice) as Total_Sales
	from star.FactSales as fs
	join star.DimDate as dd
	on dd.DateID = fs.InvoiceDateID
	group by EmployeeId, Year, MonthOfYear
)
select temp.EmployeeId, de.EmployeeName, 
    MonthOfYear,Year, Total_Sales
from temp
join star.DimEmployee as de
on de.EmployeeId = temp.EmployeeId
order by temp.EmployeeId, MonthOfYear, Year'''

df_temp = pd.merge(df_FactSales, df_DimDate, how='inner', left_on='InvoiceDateID', right_on='DateID')

# Group by 'EmployeeId', 'Year', 'MonthOfYear', and calculate sum of 'ExtendedPrice'
df_temp = df_temp.groupby(['EmployeeId', 'Year', 'MonthOfYear']).agg({'ExtendedPrice': 'sum'}).reset_index()
df_temp.rename(columns={'ExtendedPrice': 'Total_Sales'}, inplace=True)

# Merge with the 'DimEmployee' DataFrame on 'EmployeeId'
req_6_year = pd.merge(df_temp, df_DimEmployee, how='inner', on='EmployeeId')
req_6_year = req_6_year[['EmployeeId', 'EmployeeName', 'MonthOfYear', 'Year', 'Total_Sales']].sort_values(['EmployeeId', 'MonthOfYear', 'Year'])

#  Which music genre is purchased the most by year?

ex_7 = '''Rock consistently maintains its leading position in the quantity of sales each year, demonstrating its enduring popularity. Latin music remains a strong contender in the market, consistently securing a notable rank over the years. From 2009 to 2010, the genre Alternative & Punk dropped from the third position to the fourth position, while Heavy Metal and Hip Hop/Rap experienced more significant declines from positions eight to ten through seventeen. These shifts might reflect changing consumer preferences or an increased attraction towards other genres during that period. 
These fluctuations suggest a dynamic music landscape where certain genres maintain their stronghold while others experience shifts in popularity, likely influenced by evolving consumer tastes, cultural influences, or the emergence of new musical trends. Understanding these trends can aid businesses in adapting their strategies to cater to changing consumer preferences and market dynamics.
'''

query_7_day = '''
select GenreId, FullDate, count(fs.InvoiceId) as 'Total Invoices' , sum(SumPrice) as 'Total Sales'
from star.FactGenre as fg
join star.FactSales as fs
on fs.InvoiceDateID = fg.OrderDateID
join star.DimDate as dd
on fg.OrderDateID = dd.DateID
group by GenreId, FullDate
order by GenreId, FullDate'''

df_temp = pd.merge(df_FactGenre, df_FactSales, how='inner', left_on='OrderDateID', right_on='InvoiceDateID')
df_temp = pd.merge(df_temp, df_DimDate, how='inner', left_on='OrderDateID', right_on='DateID')

# Group by 'GenreId', 'FullDate', and calculate count of 'InvoiceId' and sum of 'SumPrice'
req_7_day = df_temp.groupby(['GenreId', 'FullDate']).agg({'InvoiceId': 'count', 'SumPrice': 'sum'}).reset_index()
req_7_day.rename(columns={'InvoiceId': 'Total Invoices', 'SumPrice': 'Total Sales'}, inplace=True)

query_7_month = '''
select GenreId, MonthOfYear, count(fs.InvoiceId) as 'Total Invoices' , sum(SumPrice) as 'Total Sales'
from star.FactGenre as fg
join star.FactSales as fs
on fs.InvoiceDateID = fg.OrderDateID
join star.DimDate as dd
on fg.OrderDateID = dd.DateID
group by GenreId, MonthOfYear
order by GenreId, MonthOfYear'''

req_7_month = df_temp.groupby(['GenreId', 'MonthOfYear']).agg({'InvoiceId': 'count', 'SumPrice': 'sum'}).reset_index()
req_7_month.rename(columns={'InvoiceId': 'Total Invoices', 'SumPrice': 'Total Sales'}, inplace=True)

query_7_quarter = '''
select GenreId, Quarter, count(fs.InvoiceId) as 'Total Invoices' , sum(SumPrice) as 'Total Sales'
from star.FactGenre as fg
join star.FactSales as fs
on fs.InvoiceDateID = fg.OrderDateID
join star.DimDate as dd
on fg.OrderDateID = dd.DateID
group by GenreId, Quarter
order by GenreId, Quarter'''

req_7_quarter = df_temp.groupby(['GenreId', 'Quarter']).agg({'InvoiceId': 'count', 'SumPrice': 'sum'}).reset_index()
req_7_quarter.rename(columns={'InvoiceId': 'Total Invoices', 'SumPrice': 'Total Sales'}, inplace=True)

query_7_year = '''
select GenreId, Year, count(fs.InvoiceId) as 'Total Invoices' , sum(SumPrice) as 'Total Sales'
from star.FactGenre as fg
join star.FactSales as fs
on fs.InvoiceDateID = fg.OrderDateID
join star.DimDate as dd
on fg.OrderDateID = dd.DateID
group by GenreId, Year
order by GenreId, Year'''

req_7_year = df_temp.groupby(['GenreId', 'Year']).agg({'InvoiceId': 'count', 'SumPrice': 'sum'}).reset_index()
req_7_year.rename(columns={'InvoiceId': 'Total Invoices', 'SumPrice': 'Total Sales'}, inplace=True)

# Which country has the highest sales revenue, and how does this trend over time

ex_8_1 = '''There are fluctuations in sales revenue across different countries and years. Some countries showcase consistent or increasing revenue trends over the years, while others display more erratic patterns with significant variations in sales from year to year. For instance, the USA maintained high sales figures consistently until a slight drop in 2013. Some countries experienced considerable changes in sales revenue between certain years, indicating potential fluctuations in market conditions or business strategies. 
The data highlights varied sales performances across different countries, suggesting diverse market dynamics and potential areas for further analysis regarding market trends and business strategies in each specific region.
'''

query_8 = '''
select dc.CustomerCountry, dd.Year, sum(fs.ExtendedPrice) as 'Total Sales'
from star.FactSales as fs
join star.DimCustomer as dc
on dc.CustomerId = fs.CustomerId
join star.DimDate as dd
on dd.DateID = fs.InvoiceDateID
group by dc.CustomerCountry, dd.Year
order by 'Total Sales' desc'''

req_8 = pd.merge(df_FactSales, df_DimCustomer, how='inner', on='CustomerId')
req_8 = pd.merge(req_8, df_DimDate, how='inner', left_on='InvoiceDateID', right_on='DateID')

# Group by 'CustomerCountry', 'Year', and calculate sum of 'ExtendedPrice'
req_8 = req_8.groupby(['CustomerCountry', 'Year']).agg({'ExtendedPrice': 'sum'}).reset_index()
req_8.rename(columns={'ExtendedPrice': 'Total Sales'}, inplace=True)

# Sort the DataFrame by 'Total Sales' in descending order
req_8.sort_values('Total Sales', ascending=False, inplace=True)

#  How long does it take for customers to return to buy track?
# TODO: đúng khum má?
query_9_avg = '''select top %s 
    fs.CustomerId, 
    CustomerName, 
        avg(NumberOfDaysReturned) as 'Average Days returned'
from [star].[FactGenre] as fs
join star.DimCustomer as dc 
on fs.CustomerId = dc.CustomerId 
group by fs.CustomerId, CustomerName
order by fs.CustomerId'''

req_9_avg = pd.merge(df_FactGenre, df_DimCustomer, how='inner', on='CustomerId')

# Group by 'CustomerId' and 'CustomerName', and calculate the average of 'NumberOfDaysReturned'
req_9_avg = req_9_avg.groupby(['CustomerId', 'CustomerName']).agg({'NumberOfDaysReturned': 'mean'}).reset_index()
req_9_avg.rename(columns={'NumberOfDaysReturned': 'Average Days returned'}, inplace=True)
req_9_avg = req_9_avg[['CustomerId', 'CustomerName', 'Average Days returned']].sort_values('CustomerId')

query_9_last = '''
SELECT TOP %s CustomerName, OrderDateID, NumberOfDaysReturned
FROM ( 
    SELECT CustomerId, OrderDateID, NumberOfDaysReturned,
            ROW_NUMBER() OVER 
                (partition by CustomerId  ORDER BY OrderDateID desc) as rn
       FROM star.FactGenre
     ) as temp
join star.DimCustomer as dc
on temp.CustomerId = dc.CustomerId
WHERE temp.rn = 1'''

df_FactGenre_temp = df_FactGenre.copy()
df_FactGenre_temp['rn'] = df_FactGenre.groupby('CustomerId')['OrderDateID'].rank(ascending=False, method='first')

# Filter the DataFrame to keep only the rows where rn is 1
df_temp = df_FactGenre_temp[df_FactGenre_temp['rn'] == 1][['CustomerId', 'OrderDateID', 'NumberOfDaysReturned']]

# Merge with the 'DimCustomer' DataFrame on 'CustomerId'
req_9_last = pd.merge(df_temp, df_DimCustomer, how='inner', on='CustomerId')
req_9_last = req_9_last[['CustomerName', 'OrderDateID', 'NumberOfDaysReturned']]

# What is the total revenue generated by each genre?

ex_10 = '''Notably, genres like Rock emerge as the top earners, boasting substantial total revenue figures surpassing $800. Following closely behind, Latin, Metal, and Alternative & Punk also demonstrate robust financial success, each exceeding the $200 mark in revenue. On a moderate scale, genres like TV Shows, Jazz, Blues, Drama, R&B/Soul and Classical present respectable revenue figures, ranging between $40 and $90. However, some categories such as Opera, Rock and Roll, and Easy Listening showcase comparatively lower total revenues, falling below $10. This comprehensive range of revenue figures across the entertainment spectrum signifies varying degrees of commercial success and market demand within each genre, illustrating the financial diversity and performance within these distinct entertainment segments.'''

query_10 = '''select dg.GenreName, sum(fg.SumPrice) as 'Total Sales'
from star.FactGenre as fg
join star.DimGenre as dg
on fg.GenreId = dg.GenreId
group by dg.GenreName
order by 'Total Sales' desc'''

req_10 = pd.merge(df_FactGenre, df_DimGenre, how='inner', on='GenreId')

# Group by 'GenreName' and calculate sum of 'SumPrice'
req_10 = req_10.groupby('GenreName').agg({'SumPrice': 'sum'}).reset_index()
req_10.rename(columns={'SumPrice': 'Total Sales'}, inplace=True)

# Sort the DataFrame by 'Total Sales' in descending order
req_10.sort_values('Total Sales', ascending=False, inplace=True)
