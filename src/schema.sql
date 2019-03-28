CREATE TABLE population(
  "Ward" TEXT,
  "Neighbourhood_Number" INT,
  "Neighbourhood_Name" TEXT,
  "CANADIAN_CITIZEN" INT,
  "NON_CANADIAN_CITIZEN" INT,
  "NO_RESPONSE" INT
);
CREATE TABLE coordinates(
  "Neighbourhood_Name" TEXT,
  "Latitude" REAL,
  "Longitude" REAL
);
CREATE TABLE crime_incidents(
  "Neighbourhood_Name" TEXT,
  "Crime_Type" TEXT,
  "Year" INT,
  "Quarter" INT,
  "Month" INT,
  "Incidents_Count" INT
);
