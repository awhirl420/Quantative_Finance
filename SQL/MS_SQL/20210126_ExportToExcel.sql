--Method1
--Working with data in Excel or Access requires the appropriate driver:
--https://www.microsoft.com/en-us/download/details.aspx?id=54920

INSERT INTO OPENROWSET('Microsoft.Jet.OLEDB.4.0',
'Excel 8.0;Database=C:\Users\WinnieTsai\testing.xls;',
'SELECT * FROM [Sheet1$]')
SELECT *, GETDATE() FROM AdventureWorks2017.dbo.CustomerView
GO



