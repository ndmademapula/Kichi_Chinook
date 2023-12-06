import streamlit as st
import pandas as pd
import pyodbc
from PIL import Image
# Initialize connection.
# Uses st.cache_resource to only run once.
st.set_page_config(layout="wide")
st.title("Chinook Dataset Overview")


Album = '''
- Description: Contains information about music albums.
- Number of Rows: 347
- Number of Features: 3 

| **Columns**                   | **Description**                |
| ----------------------------- | ------------------------------ |
| AlbumId                       | ID of the album                |
| Title                         | Title of the album             |
| ArtistId                      | ID of the artist               |
'''
customer = '''
- Description: Stores details about customers.
- Number of Rows: 59
- Number of Features: 13 

| **Columns**                   | **Description**                |
| ----------------------------- | ------------------------------ |
| CustomerId                    | ID of the customer             |
| FirstName                     | First name of the customer     |
| LastName                      | Last name of the customer      |
| Company                       | Company name                   |
| Address                       | Customer address               |
| City                          | City of the customer           |
| State                         | State of the customer          |
| Country                       | Country of the customer        |
| PostalCode                    | Postal code of the customer    |
| Phone                         | Phone number of the customer   |
| Fax                           | Fax number of the customer     |
| Email                         | Email address of the customer  |
| SupportRepId                  | ID of the support representative|
'''
employee = '''
- Description: Holds information about employees.
- Number of Rows: 8
- Number of Features: 15

| **Columns**                   | **Description**                |
| ----------------------------- | ------------------------------ |
| EmployeeId                    | ID of the employee              |
| LastName                      | Last name of the employee      |
| FirstName                     | First name of the employee     |
| Title                         | Title/position of the employee |
| ReportsTo                     | ID of the supervisor            |
| BirthDate                     | Birth date of the employee     |
| HireDate                      | Hire date of the employee      |
| Address                       | Address of the employee        |
| City                          | City of the employee           |
| State                         | State of the employee          |
| Country                       | Country of the employee        |
| PostalCode                    | Postal code of the employee    |
| Phone                         | Phone number of the employee   |
| Fax                           | Fax number of the employee     |
| Email                         | Email address of the employee  |
'''
genre='''
- Description: Contains music genres.
- Number of Rows: 28
- Number of Features: 2

| **Columns**                   | **Description**                |
| ----------------------------- | ------------------------------ |
| GenreID                       | ID of the genre                |
| Name                          | Name of the genre              |
'''
invoice = '''
- Description: Records invoice details.
- Number of Rows: 412
- Number of Features: 9

| **Columns**                   | **Description**                |
| ----------------------------- | ------------------------------ |
| InvoiceId                     | ID of the invoice              |
| CustomerId                    | ID of the customer             |
| InvoiceDate                   | Date of the invoice            |
| BillingAddress                | Billing address                |
| BillingCity                   | City in the billing address    |
| BillingState                  | State in the billing address   |
| BillingCountry                | Country in the billing address |
| BillingPostalCode              | Postal code in billing address  |
| Total                         | Total amount of the invoice    |
'''
invoiceline = '''
- Description: Provides line-level details for each invoice.
- Number of Rows: 2240
- Number of Features: 5

| **Columns**                   | **Description**                |
| ----------------------------- | ------------------------------ |
| InvoiceLineId                 | ID of the invoice line         |
| InvoiceId                     | ID of the associated invoice   |
| TrackId                       | ID of the track                |
| UnitPrice                     | Unit price of the track        |
| Quantity                      | Quantity of the track          |
| **Rows**                      | 2240                           |
'''
mediatype = '''
- Description: Describes media types.
- Number of Rows: 5
- Number of Features: 2

| **Columns**                   | **Description**                |
| ----------------------------- | ------------------------------ |
| MediaTypeId                   | ID of the media type           |
| Name                          | Name of the media type         |
'''
playlist = '''
- Description: Contains playlists.
- Number of Rows: 18
- Number of Features: 2

| **Columns**                   | **Description**                |
| ----------------------------- | ------------------------------ |
| PlaylistId                    | ID of the playlist             |
| Name                          | Name of the playlist           |
'''
playlisttrack='''
- Description: Maps tracks to playlists.
- Number of Rows: 8715
- Number of Features: 2

| **Columns**                   | **Description**                |
| ----------------------------- | ------------------------------ |
| PlaylistId                    | ID of the playlist             |
| TrackId                       | ID of the track                |
'''
track='''
- Description: Stores details about individual music tracks.
- Number of Rows: 3503
- Number of Features: 9 

| **Columns**                   | **Description**                |
| ----------------------------- | ------------------------------ |
| TrackId                       | ID of the track                |
| Name                          | Name of the track              |
| AlbumId                       | ID of the associated album     |
| MediaTypeId                   | ID of the media type           |
| GenreId                       | ID of the genre                |
| Composer                      | Composer of the track          |
| Milliseconds                  | Duration of the track in milliseconds |
| Bytes                         | Size of the track in bytes      |
| UnitPrice                     | Unit price of the track        |
'''
dataframes = {
    "Album": Album,
    "Customer": customer,
    "Employee": employee,
    "Genre": genre,
    "Invoice": invoice,
    "InvoiceLine": invoiceline,
    "MediaType": mediatype,
    "Playlist": playlist,
    "PlaylistTrack": playlisttrack,
    "Track": track,
}

col1, col2= st.columns([1,2], gap='large')
with col1:
    st.markdown(
        r'''The Chinook data model represents a digital media store, including tables for artists, albums, media tracks, invoices, and customers. Details about purchases of music products from :red[2009 to 2013].

Media-related data was created using real data from an :red[Apple iTunes library]. Customer and employee information was created using fictitious names and addresses that can be located on Google maps, and other well formatted data (phone, fax, email, etc. 

Sales information was auto generated using random data for a four year period between 2009-2013.
    '''
    )
with col2:
    tables = st.selectbox(placeholder='Select table to see information',label='The Chinook sample database includes: ',
                        options=dataframes.keys(), index=None)
    if tables == None:
        st.warning("Choose a table above to view information")
    else:
        st.markdown(dataframes[tables]) 
st.divider()
