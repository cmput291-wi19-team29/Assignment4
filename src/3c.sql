-- Extra: get the year ranges available
SELECT MIN(Year) AS min, MAX(Year) AS max 
FROM crime_incidents 
WHERE Year!='Year'; -- For some reason the DB has the column name included as a tuple.