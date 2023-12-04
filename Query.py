import pandas as pd
from constant import *

# Track sales per day, month, quarter, year?
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
# TODO: - check distinct InvoiceID, - đúng khum má
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

#!  How much gerne music in playlist?
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

#!  How much genre in playlist?