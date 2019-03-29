-- Extra: get the crime types available
SELECT DISTINCT Crime_Type 
FROM crime_incidents 
WHERE Crime_Type!='CRIME_TYPE' -- For some reason the DB has the column name included as a tuple.
ORDER BY Crime_Type;