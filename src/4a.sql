-- Given a range of years and an integer N, show (in a map) the Top-N neighborhoods with the highest crimes to 
-- population ratio within the provided range. Also, show the most frequent crime type in each of these neighborhoods.

-- do not consider the neighbourhoods which do not have a reported population
-- filter out zero longitude and latitude

-- args are in the format year range [a, b], (top) n

-- filter by empty population / zero longitude-latitude, ratio (descending)

SELECT "Neighbourhood_Name", 

"Incidents_Count" / ("CANADIAN_CITIZEN" + "NON_CANADIAN_CITIZEN" + "NO_RESPONSE")