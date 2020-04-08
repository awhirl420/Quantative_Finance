-- LEARN FROM Udemy <Introduction to Databases and SQL Querying>

-- 建立資料庫
create database testdb

-- 指定使用資料庫
use testdb

-- 建立表格
create table testtable ( no int, firstname varcha(50), lastname varcha(50) )

-- 新增資料
insert into testtable(no, firstname, lastname) values(1, 'Claire', 'Tsai')

-- 選取資料(特定欄位)
select no, firstname, lastname from testtable

-- 選取資料(全部欄位)
use [AdventureWorks2012]
SELECT * FROM [HumanResources].[Department]

-- 刪除資料表
TRUNCATE TABLE MYCUSTOMERS

-- SHOW ALL THE DISTINCT GROUPNAME
SELECT DISTINCT GROUPNAME FROM [HumanResources].[Department]

-- SHOW ALL THE GROUPNAME IS COMPOSED OF MANUFACTURING 
SELECT NAME, GROUPNAME FROM [HumanResources].[Department]
WHERE GROUPNAME LIKE 'MANUFACTURING'

-- SHOW ALL THE EMPLOYEE WHOESE LEVEL EQUAL 2
SELECT * FROM [HumanResources].[Employee] WHERE ORGANIZATIONLEVEL = 2 

-- SHOW ALL THE EMPLOYEE WHOESE LEVEL EQUAL 2 or 3
SELECT * FROM [HumanResources].[Employee] WHERE ORGANIZATIONLEVEL IN (2,3)

-- SHOW ALL EMPLOYEE WHO IS MANAGER
SELECT * FROM [HumanResources].[Employee] WHERE JOBTITLE LIKE '%Manager'

-- SHOW ALL EMPLOYEE BORN AFTER Jun 1, 1980
SELECT * FROM [HumanResources].[Employee] WHERE Birthdate > '6/1/1980'

-- SHOW ALL EMPLOYEE BORN BETWEEN Jun 1, 1970 and Jun 1, 1980
-- OPTION-1
SELECT * FROM [HumanResources].[Employee] WHERE Birthdate > '6/1/1970' AND Birthdate < '6/1/1980'
SELECT * FROM [HumanResources].[Employee] WHERE Birthdate BETWEEN '6/1/1970' AND '6/1/1980'

-- CREATE NEW COLUMN
SELECT NAME, LISTPRICE, LISTPRICE + 10 AS ADJUSTED_LIST_PRICE FROM [Production].[Product]
-- SAVE NEW COLUMN TO NEW TABLE
SELECT NAME, LISTPRICE, LISTPRICE + 10 AS ADJUSTED_LIST_PRICE INTO [Production].[Product_2] FROM [Production].[Product]
SELECT NAME, LISTPRICE, LISTPRICE + 10 AS ADJUSTED_LIST_PRICE INTO #temptable FROM [Production].[Product]

-- DELETE DATA FROM TABLE
DELETE FROM [Production].[Product_2] WHERE NAME LIKE '%Ball'

-- UPDATE DATA
UPDATE [Production].[Product_2]
SET NAME = 'BLADE_NEW'
WHERE NAME LIKE 'BLADE'

-- JOINS
CREATE TABLE EMPLOYEE (ID INT, FIRSTNAME VARCHAR(20), LASTNAME VARCHAR(20))
INSERT INTO EMPLOYEE VALUES (1, 'Claire', 'Tsai')
INSERT INTO EMPLOYEE VALUES (2, 'Mandy', 'Lin')
INSERT INTO EMPLOYEE VALUES (3, 'Tom', 'Hank')

CREATE TABLE SALARY (ID INT, SALARY FLOAT)
INSERT INTO SALARY VALUES (1, 10000)
INSERT INTO SALARY VALUES (2, 40000)
INSERT INTO SALARY VALUES (4, 10000000)                                                                              

SELECT * FROM EMPLOYEE
SELECT * FROM SALARY
                                                                                                                                  
-- INNER JOIN
SELECT A.FIRSTNAME, A.LASTNAME, B.SALARY
FROM EMPLOYEE A INNER JOIN SALARY B ON A.ID = B.ID                                                                       
                                                                       
-- LEFT OUTER JOIN
-- all rows in left show and prsent 'NULL' in right if empty
SELECT A.FIRSTNAME, A.LASTNAME, B.SALARY                                                                      
FROM EMPLOYEE A LEFT JOIN SALARY B ON A.ID = B.ID
                                                                       
-- FULL OUTER JOIN
SELECT A.FIRSTNAME, A.LASTNAME, B.SALARY                                                                      
FROM EMPLOYEE A OUTER JOIN SALARY B ON A.ID = B.ID                                                                       

-- CROSS JOIN
-- OPTION-1
SELECT * FROM EMPLOYEE CROSS JOIN SALARY
-- OPTION-2
SELECT * FROM EMPLOYEE, SALARY

-- TSQL Date
SELECT GETDATE()
SELECT GETDATE() - 2

SELECT DATEPART(yyyy,GETDATE()) AS YEARNUMBER
SELECT DATEPART(mm,GETDATE())
SELECT DATEPART(dd,GETDATE())

SELECT DATEADD(day, 4, '7/4/2015')
SELECT DATEADD(month, 4, GETDATE())
SELECT DATEADD(year, 4, GETDATE())

SELECT TOP 10 * FROM [Production].[WorkOrder]
SELECT workOrderID, StartDate, EndDate, DATEDIFF(day, StartDate, EndDate)
FROM [Production].[WorkOrder]               

SELECT DATEADD(dd, -(DATEPART(day, GETDATE())-1), GETDATE())                              

-- TSQL Aggregation
SELECT AVG(SALARY) FROM SALARY
SELECT COUNT(SALARY) FROM SALARY
-- ONLY COUNT ROWS
SELECT COUNT(*) FROM SALARY
SELECT SUM(SALARY) FROM SALARY
SELECT MIN(SALARY) FROM SALARY
SELECT MAX(SALARY) FROM SALARY
                     
-- CONCAT
PRINT CONCAT('String 1','String 2')

SELECT ORDERNUMBER, ORDERNAME, CONCAT(ORDERNAME, ' ', RAND()) AS CONTEXT
FROM MYORDER
                                      
-- 擷取文字
SELECT ORDERNUMBER, ORDERNAME, LEFT(ORDERNAME, 5) FROM MYORDER
SELECT ORDERNUMBER, ORDERNAME, RIGHT(ORDERNAME, 5) FROM MYORDER
SELECT ORDERNUMBER, ORDERNAME, SUBSTRING(ORDERNAME, 3, 5) FROM MYORDER

SELECT ORDERNUMBER, ORDERNAME, LOWER(ORDERNAME) FROM MYORDER
SELECT ORDERNUMBER, ORDERNAME, UPPER(ORDERNAME) FROM MYORDER
SELECT ORDERNUMBER, ORDERNAME, LEN(ORDERNAME) FROM MYORDER

-- 首位字母大寫
CONCAT(UPPER(LEFT(ORDERNAME,1)),LOWER(SUBSTRING(ORDERNAME,2,LEN(ORDERNAME))))

-- TRIM
SELECT LTRIM(' Mytext ')
SELECT RTRIM(' Mytext ')
SELECT LTRIM(RTRIM(' Mytext '))
