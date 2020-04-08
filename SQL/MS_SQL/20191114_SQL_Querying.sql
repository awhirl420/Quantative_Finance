-- Learn From '1keydata.com/tw/sql/sqlorderby.html'
-- Refernece 'https://docs.microsoft.com/zh-tw/sql/t-sql/functions/functions?view=sql-server-ver15'

-- Basics
SELECT [GroupName] FROM [HumanResources].[Department];

SELECT DISTINCT [GroupName] FROM [HumanResources].[Department];

SELECT * FROM [Sales].[SalesPerson] WHERE [Bonus] > 2000;

SELECT * FROM [Sales].[SalesPerson] WHERE [Bonus] > 2000 OR ([Bonus]<1000 AND [Bonus]>500);

SELECT [FirstName], [LastName], [EmailPromotion] FROM [Person].[Person] WHERE [FirstName]  IN ('Mary','Pete');

SELECT * FROM [Sales].[SpecialOffer] WHERE [StartDate] BETWEEN '2012-01-01' AND '2012-12-31';

SELECT [FirstName], [LastName], [EmailPromotion] FROM [Person].[Person] WHERE [FirstName]  LIKE 'K_n';

SELECT [FirstName], [LastName], [EmailPromotion] FROM [Person].[Person] WHERE [FirstName]  LIKE 'An%';

SELECT [FirstName], [LastName], [EmailPromotion] FROM [Person].[Person] WHERE [FirstName]  LIKE '%an';

SELECT [FirstName], [LastName], [EmailPromotion] FROM [Person].[Person] WHERE [FirstName]  LIKE '%an%';

SELECT [FirstName], [LastName], [EmailPromotion] FROM [Person].[Person] WHERE [FirstName]  LIKE '_an%';

-- IN: perfect match
-- LIKE: pattern

SELECT [BusinessEntityID], [Bonus] FROM [Sales].[SalesPerson] ORDER BY [Bonus] ASC;

SELECT [BusinessEntityID], [Bonus] FROM [Sales].[SalesPerson] ORDER BY [Bonus] DESC;

SELECT [BusinessEntityID], [Bonus] FROM [Sales].[SalesPerson] ORDER BY 2 ASC;

SELECT AVG([Bonus]) AS 'AVG' FROM [Sales].[SalesPerson];
SELECT COUNT([Bonus]) '#' FROM [Sales].[SalesPerson];
SELECT MAX([Bonus]) 'MAX' FROM [Sales].[SalesPerson];
SELECT MIN([Bonus]) 'MIN' FROM [Sales].[SalesPerson];

SELECT [Color], SUM([SafetyStockLevel]) FROM [Production].[Product] GROUP BY [Color];

-- WHERE在GROUP BY之前，HAVING在GROUP BY之後
-- HAVING可對彙總欄位進行篩選

SELECT [Color], SUM([SafetyStockLevel]) FROM [Production].[Product] GROUP BY [Color]
HAVING SUM([SafetyStockLevel]) >10000;

SELECT A1.[Color], SUM(A1.[SafetyStockLevel]) "Inventory" FROM [Production].[Product] A1 GROUP BY A1.[Color]
HAVING SUM(A1.[SafetyStockLevel]) >10000;

-- 篩選彙總欄位時，有辦法使用的新增函數別名嗎?

SELECT A1.[Color] AS Type, SUM(A1.[SafetyStockLevel]) AS "Inventory" FROM [Production].[Product] AS A1 
GROUP BY A1.[Color];

-- JOINT概念: complete materials please refer to '20191110_SQL_Querying.sql'
SELECT A2.[LocationID] Location, SUM([SafetyStockLevel]) Quantity
FROM [Production].[Product] A1, [Production].[ProductInventory] A2
WHERE A1.[ProductID] = A2.[ProductID]
GROUP BY A2.[LocationID];

SELECT CONCAT([ProductID],' ',[Name]) FROM [Production].[Product];

SELECT SUBSTRING([Name],3,LEN([Name])) FROM [Production].[Product];

-- 3個資料表Join                                  
SELECT 
A1.[ProductID],
A1.[Color],
A2.[LocationID], 
A3.[StartDate]
INTO CustomerView2
FROM ([Production].[Product] A1 
      INNER JOIN [Production].[ProductInventory] A2
      ON A1.[ProductID] = A2.[ProductID])
INNER JOIN [Production].[ProductCostHistory] A3
ON A1.[ProductID] = A3.[ProductID];
                               
                               
-- 2個Group By
SELECT ProductID,
Color,
COUNT(*) As 'OwnersCountt',
SUM(LocationID) As 'TotalAmount',
(SUM(LocationID)/COUNT(*)) As 'Answer'
FROM CustomerView2
WHERE ProductID >= 700 AND ProductID <750
GROUP BY ProductID, Color;


--  用for迴圈建立新資料表
DECLARE @_i int
DECLARE @_MAX int

CREATE TABLE ID(ProductID int, ProductDate datetime)
SET @_i=700
SET @_MAX =750
WHILE(@_i<@_MAX)
BEGIN
	INSERT INTO ID VALUES (@_i,GETDATE())
	SET @_i=@_i+1;
END

SELECT * FROM ID;




-- Boolean

SELECT * 
FROM CutomerView4
WHERE (ProductDate IS NULL) AND
(SellStartDate BETWEEN '2012-01-01' AND '2012-12-31') AND
(LocationID > 10);
