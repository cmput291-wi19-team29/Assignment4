-- This query is for getting the coordinates for mapping
SELECT Neighbourhood_Name, Latitude, Longitude 
FROM coordinates 
WHERE Latitude!=0.0 AND Longitude!=0.0 -- Exclude zero'd rows
AND Neighbourhood_Name!='NEIGHBOURHOOD_NAME' -- Database somehow has this tuple in it
;