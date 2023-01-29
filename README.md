# Ping-csv.input-email.output
Pings list of devices from CSV, sorts failed responses to top of table and emails result as HTML.

Imports list from .csv to new dataframe
New column put into dataframe
Pings each IP from the dataframe
Ping results put into new column in same dataframe
New dataframe for passed pings created and populated
New dataframe for faile pings created and populated
New dataframe created by appending passed pings on to failed pings 
Failed pings are now at the top f the dataframe with passed pings below
Dataframe with sorted ping responses is put into email body as HTML
