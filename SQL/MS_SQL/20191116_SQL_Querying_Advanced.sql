---TRANSACTIONS
SELECT * FROM [Sales].[SalesTerritory]

BEGIN TRANSACTION
   UPDATE Sales.SalesTerritory
   SET costYTD = 1.00
   WHERE TerritoryID = 1
COMMIT TRANSACTION


---@@error 0 = success, > 0 means error
DECLARE @ERRORRESULTS VARCHAR(50)
BEGIN TRANSACTION
INSERT INTO [Sales].[SalesTerritory]
           ([Name]
           ,[CountryRegionCode]
           ,[Group]
           ,[SalesYTD]
           ,[SalesLastYear]
           ,[CostYTD]
           ,[CostLastYear]
           ,[rowguid]
           ,[ModifiedDate])
     VALUES
           ('ABC'
           ,'us'
           ,'na'
           ,1.00
           ,1.00
           ,1.00
           ,1.00
           ,'43689A10-E30B-497F-B0DE-11DE20267FF3'
           ,GETDATE())

SET @ERRORRESULTS = @@ERROR

IF(@ERRORRESULTS = 0)
BEGIN
	PRINT 'SUCCESS!!!!'
	COMMIT TRANSACTION
END
ELSE
BEGIN
    PRINT 'STATEMENT FAILED!!!!'
	ROLLBACK TRANSACTION
END
            
           
--custom error message
DECLARE @ERRORRESULTS VARCHAR(50)
BEGIN TRANSACTION
INSERT INTO [Sales].[SalesTerritory]
           ([Name]
           ,[CountryRegionCode]
           ,[Group]
           ,[SalesYTD]
           ,[SalesLastYear]
           ,[CostYTD]
           ,[CostLastYear]
           ,[rowguid]
           ,[ModifiedDate])
     VALUES
           ('ABC'
           ,'us'
           ,'na'
           ,1.00
           ,1.00
           ,1.00
           ,1.00
           ,'43689A10-E30B-497F-B0DE-11DE20267FF3'
           ,GETDATE())

SET @ERRORRESULTS = @@ERROR

IF(@ERRORRESULTS = 0)
BEGIN
	PRINT 'SUCCESS!!!!'
	COMMIT TRANSACTION
END
ELSE
BEGIN
    RAISERROR('STATEMENT FAILED - THIS IS MY CUSTOM MESSAGE', 16, 1)
	ROLLBACK TRANSACTION
END
            
           
--TRY AND CATCH
BEGIN TRY
BEGIN TRANSACTION
INSERT INTO [Sales].[SalesTerritory]
           ([Name]
           ,[CountryRegionCode]
           ,[Group]
           ,[SalesYTD]
           ,[SalesLastYear]
           ,[CostYTD]
           ,[CostLastYear]
           ,[rowguid]
           ,[ModifiedDate])
     VALUES
           ('ABC'
           ,'us'
           ,'na'
           ,1.00
           ,1.00
           ,1.00
           ,1.00
           ,'43689A10-E30B-497F-B0DE-11DE20267FF3'
           ,GETDATE())

		   commit TRANSACTION
END TRY

BEGIN CATCH
    PRINT 'CATCH STATEMENT ENTERED'
	ROLLBACK TRANSACTION
END CATCH
            
            
--Common Table Expression
WITH CTE_SALESTERR
AS
(
   SELECT Name, CountryRegionCode FROM Sales.SalesTerritory
)

SELECT * FROM CTE_SALESTERR
WHERE NAME LIKE 'North%';

            
--Present each layer of GROUPs at the same time
SELECT Name, NULL, NULL, SUM(SalesYTD)
FROM [Sales].[SalesTerritory]
GROUP BY Name, CountryRegionCode, [group]

UNION ALL

SELECT Name, CountryRegionCode, NULL, SUM(SalesYTD)
FROM [Sales].[SalesTerritory]
GROUP BY Name, CountryRegionCode, [group]

UNION ALL

SELECT Name, CountryRegionCode, [Group], SUM(SalesYTD)
FROM [Sales].[SalesTerritory]
GROUP BY Name, CountryRegionCode, [group]
            
            
---GROUPING SETS
SELECT Name, CountryRegionCode, [Group], SUM(SalesYTD)
FROM [Sales].[SalesTerritory]
GROUP BY GROUPING SETS
(
(Name),
	(Name, CountryREgionCode),
	(Name, CountryRegionCode, [Group])
)

--ROLLUP (Hierarchical Data)
SELECT Name, CountryRegionCode, [Group], SUM(SalesYTD)
FROM [Sales].[SalesTerritory]
GROUP BY ROLLUP
(
	(Name, CountryRegionCode, [Group])
)


 --CUBE(Show all possible combinations)
 SELECT Name, CountryRegionCode, [Group], SUM(SalesYTD)
 FROM [Sales].[SalesTerritory]
GROUP BY CUBE
(
	(Name, CountryRegionCode, [Group])
)
