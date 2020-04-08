/****** SSMS 中 SelectTopNRows 命令的指令碼  ******/
SELECT TOP (1000) [TerritoryID]
    ,[Name]
    ,[CountryRegionCode]
    ,[Group]
    ,[SalesYTD]
    ,[SalesLastYear]
    ,[CostYTD]
    ,[CostLastYear]
    ,[rowguid]
    ,[ModifiedDate]
FROM [AdventureWorks2017].[Sales].[SalesTerritory]

---VIEWS (US VIEW)
CREATE VIEW MyCustomerUSView
AS
SELECT * FROM [Sales].[SalesTerritory]
WHERE CountryRegionCode LIKE 'US'

SELECT * FROM MyCustomerUSView

CREATE VIEW NASalesQuota
AS
SELECT [Name],[Group],[SalesQuota],[Bonus]
FROM [Sales].[SalesTerritory] A INNER JOIN [Sales].[SalesPerson] B
ON A.TerritoryID = B.TerritoryID
WHERE [Group] LIKE 'North America'

SELECT * FROM NASalesQuota

-----------------
------TRIGGRT----
SELECT * FROM [HumanResources].[Shift]
  
CREATE TRIGGER Demo_Trigger2
ON [HumanResources].[Shift]
AFTER INSERT
--AFTER/BEFORE
--INSERT/UPDATE/DELETE
AS
BEGIN
PRINT 'INSERT IS NOT ALLOWED. YOU NEED APPROVAL'
ROLLBACK TRANSACTION
END
GO

--TEST THE TRIGER
INSERT INTO [HumanResources].[Shift]
(
[Name],
[StartTime],
[EndTime],
[ModifiedDate]
)
VALUES
('CLAIRE'
,'07:00:00.0000000'
,'08:00:00.0000000'
,getdate()
)

------------------------------------------------
---------DATABASE LEVEL TRIGGER
CREATE TRIGGER DEMO_DBTRIGGER
ON DATABASE
AFTER CREATE_TABLE
AS
BEGIN
PRINT 'CREATION OF NEW TABLES NOT ALLOWED'
ROLLBACK TRANSACTION
END
GO

CREATE TABLE DEMOTABLE(Col1 varchar(10))

-------------------------------------------
-----STORED PROCEDURES
-------------------------------------------
CREATE PROCEDURE MyTestProc
AS
SET NOCOUNT ON
SELECT * FROM [HumanResources].[Shift]

EXECUTE MyTestProc

CREATE PROCEDURE MyTestProc2
AS
SET NOCOUNT OFF
SELECT * FROM [HumanResources].[Shift]

EXECUTE MyTestProc2

DROP PROC MytestPRoc
DROP PROC MyTestProc2

CREATE PROCEDURE MyFirstParamProc
@Parama_Name VARCHAR(50)
AS
SET NOCOUNT ON
SELECT * FROM [HumanResources].[Shift]
WHERE Name = @Parama_Name;

EXEC MyFirstParamProc @Parama_Name = 'Day'
EXEC MyFirstParamProc 'Day'

DROP PROC MyFirstParamProc

CREATE PROCEDURE MyFirstParamProc
@Parama_Name VARCHAR(50) = 'Evening'
AS
SET NOCOUNT ON
SELECT * FROM [HumanResources].[Shift]
WHERE Name = @Parama_Name;

EXEC MyFirstParamProc

---OUTPUT PARAMETERS
CREATE PROC MyOutputSP
@TopShift varchar(50) OUTPUT
AS
SET @TopShift = (SELECT TOP(1) ShiftID FROM [HumanResources].[Shift])

DECLARE @outputresult VARCHAR(50)
EXEC MyOutputSP @outputresult output
select @outputresult

DROP PROC MyOutputSP
---RETURNING VALUES FROM STORED PROCEDURES
CREATE PROC myFirstReturningSP
AS
RETURN 12

DECLARE @resturnvalue INT
EXEC @resturnvalue = myFirstReturningSP
SELECT @resturnvalue

--------------------------------------
---USER DEFINED FUNCTIONS
SELECT * FROM [Sales].[SalesTerritory]

CREATE FUNCTION YTDSALES()
RETURNS MONEY
AS
BEGIN
DECLARE @YTDSALES MONEY
SELECT @YTDSALES = SUM(SALESYTD) FROM [Sales].[SalesTerritory]
RETURN @YTDSALES
END

DECLARE @YTDRESULTS AS MONEY
SELECT @YTDRESULTS = dbo.YTDSALES()
PRINT @YTDRESULTS

---PARAMETERIZED FUNCTIONS

CREATE FUNCTION YTD_GROUP
(@GROUP VARCHAR(50))
RETURNS MONEY
AS
BEGIN
DECLARE @YTDSALES AS MONEY
SELECT @YTDSALES = SUM(SalesYTD) FROM [Sales].[SalesTerritory]
WHERE [GROUP] = @GROUP
RETURN @YTDSALES
END

DECLARE @RESULTS MONEY
SELECT @RESULTS = dbo.YTD_GROUP('North America')
PRINT @RESULTS

DROP FUNCTION YTD_GROUP

------FUNCTIONS RETURNING TABLES
CREATE FUNCTION ST_TABVALUED
(@TerritoryID INT)
RETURNS TABLE
AS RETURN
SELECT [Name],[CountryRegionCode], [Group], [SalesYTD]
FROM Sales.SalesTerritory
Where TerritoryID = @TerritoryID

SELECT * FROM dbo.ST_TABVALUED(7)
