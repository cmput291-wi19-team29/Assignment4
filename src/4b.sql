-- given a neighborhood, fetch the most frequent crime type in that area

-- args are: year range [a,b], neighborhood name

-- filter by empty population / zero longitude-latitude, neighborhood, then by years, bin incidents by type (descending)

SELECT 