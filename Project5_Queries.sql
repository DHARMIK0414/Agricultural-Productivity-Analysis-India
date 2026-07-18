-- =========================================================================
-- LinuxWorld Informatics Pvt. Ltd. - Summer Industrial Training
-- Capstone Project 5: Agricultural Productivity & Yield Analysis in India
-- Phase 3: SQL Database Analysis Script (SQLite / SQLite3 compatible)
-- Author: Trivedi Dharmik
-- =========================================================================

-- -------------------------------------------------------------------------
-- SETUP: Tables structures description (for reference)
-- 
-- 1. Main Table: crop_production_cleaned
--    Columns: State_Name, District_Name, Crop_Year, Season, Crop, Area,
--             Production, Yield, Yield_Index, is_outlier
-- 
-- 2. Join Table: state_zone_ref
--    Columns: State_Name, Zone
-- -------------------------------------------------------------------------


-- =========================================================================
-- TASK 1: BASIC AGGREGATIONS
-- Goal: Analyze total area, total production, and average yield by Crop
-- =========================================================================

SELECT 
    Crop,
    COUNT(*) AS Total_Records,
    ROUND(SUM(Area), 2) AS Total_Area_Hectares,
    ROUND(SUM(Production), 2) AS Total_Production,
    ROUND(AVG(Yield), 4) AS Avg_Yield_Raw,
    ROUND(MIN(Yield), 4) AS Min_Yield_Raw,
    ROUND(MAX(Yield), 4) AS Max_Yield_Raw
FROM 
    crop_production_cleaned
GROUP BY 
    Crop
ORDER BY 
    Total_Area_Hectares DESC;


-- =========================================================================
-- TASK 2: FILTERING AND SEGMENTATION
-- Goal: Query yields for a specific year range and filter out flagged outliers
-- =========================================================================

SELECT 
    State_Name,
    Crop,
    Crop_Year,
    Yield,
    Yield_Index
FROM 
    crop_production_cleaned
WHERE 
    Crop_Year BETWEEN 2005 AND 2012
    AND is_outlier = 0
    AND Crop = 'Rice'
ORDER BY 
    Yield_Index DESC
LIMIT 10;


-- =========================================================================
-- TASK 3: INNER JOIN
-- Goal: Combine transactional crop records with the State-to-Zone mapping table
-- =========================================================================

SELECT 
    c.State_Name,
    z.Zone,
    c.Crop,
    c.Crop_Year,
    c.Area,
    c.Production,
    c.Yield_Index
FROM 
    crop_production_cleaned c
INNER JOIN 
    state_zone_ref z ON c.State_Name = z.State_Name
WHERE 
    c.is_outlier = 0
LIMIT 15;


-- =========================================================================
-- TASK 4: WINDOW FUNCTIONS (RANK, LAG, LEAD)
-- Goal: Rank states by productivity index and calculate YoY yield changes
-- =========================================================================

-- Query 4A: Rank states by average Yield Index in the Kharif season
SELECT 
    z.Zone,
    c.State_Name,
    ROUND(AVG(c.Yield_Index), 4) AS Avg_Yield_Index,
    RANK() OVER (PARTITION BY z.Zone ORDER BY AVG(c.Yield_Index) DESC) AS Zone_Yield_Rank
FROM 
    crop_production_cleaned c
INNER JOIN 
    state_zone_ref z ON c.State_Name = z.State_Name
WHERE 
    c.Season = 'Kharif'
GROUP BY 
    z.Zone, c.State_Name;


-- Query 4B: Calculate Year-over-Year (YoY) productivity change using LAG
WITH YearlyNationalYield AS (
    SELECT 
        Crop_Year,
        AVG(Yield_Index) AS Avg_Yield_Index
    FROM 
        crop_production_cleaned
    WHERE 
        Crop_Year BETWEEN 1997 AND 2014 -- 2015 excluded due to incomplete records
    GROUP BY 
        Crop_Year
)
SELECT 
    Crop_Year,
    ROUND(Avg_Yield_Index, 4) AS National_Yield_Index,
    ROUND(LAG(Avg_Yield_Index, 1) OVER (ORDER BY Crop_Year), 4) AS Prev_Year_Index,
    ROUND(
        ((Avg_Yield_Index - LAG(Avg_Yield_Index, 1) OVER (ORDER BY Crop_Year)) / 
         LAG(Avg_Yield_Index, 1) OVER (ORDER BY Crop_Year)) * 100, 
        2
    ) AS YoY_Growth_Pct
FROM 
    YearlyNationalYield;


-- =========================================================================
-- TASK 5: SUBQUERIES AND CTE (COMMON TABLE EXPRESSIONS)
-- Goal: Isolate districts that perform 25%+ above their state's average yield
-- =========================================================================

WITH StateAverageYield AS (
    SELECT 
        State_Name,
        AVG(Yield_Index) AS State_Avg_Index
    FROM 
        crop_production_cleaned
    GROUP BY 
        State_Name
),
DistrictAverageYield AS (
    SELECT 
        State_Name,
        District_Name,
        AVG(Yield_Index) AS Dist_Avg_Index
    FROM 
        crop_production_cleaned
    GROUP BY 
        State_Name, District_Name
)
SELECT 
    d.State_Name,
    d.District_Name,
    ROUND(d.Dist_Avg_Index, 4) AS District_Yield_Index,
    ROUND(s.State_Avg_Index, 4) AS State_Yield_Index,
    ROUND((d.Dist_Avg_Index / s.State_Avg_Index - 1) * 100, 2) AS Performance_Above_State_Avg_Pct
FROM 
    DistrictAverageYield d
INNER JOIN 
    StateAverageYield s ON d.State_Name = s.State_Name
WHERE 
    d.Dist_Avg_Index > s.State_Avg_Index * 1.25
ORDER BY 
    Performance_Above_State_Avg_Pct DESC;


-- =========================================================================
-- TASK 6: FINAL VIEW FOR BI DASHBOARDING
-- Goal: Create a denormalized VIEW summarizing crop, state, zone, and time
--       dimensions, optimized for BI dashboard visualization layers.
-- =========================================================================

DROP VIEW IF EXISTS V_Agricultural_Productivity_KPIs;

CREATE VIEW V_Agricultural_Productivity_KPIs AS
SELECT 
    c.State_Name,
    z.Zone,
    c.District_Name,
    c.Crop_Year,
    c.Season,
    c.Crop,
    c.Area AS Area_Ha,
    c.Production AS Production_Qty,
    c.Yield AS Yield_Raw,
    c.Yield_Index,
    c.is_outlier
FROM 
    crop_production_cleaned c
INNER JOIN 
    state_zone_ref z ON c.State_Name = z.State_Name;

-- Verify View Structure
SELECT * FROM V_Agricultural_Productivity_KPIs LIMIT 5;
