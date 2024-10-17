import pyodbc
import pandas as pd

server = ''
database = ''
username = ''
password = ''

connection_string = (
    f'DRIVER={{SQL Server Native Client 11.0}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

try:
    connection = pyodbc.connect(connection_string)
    print("Connection to database successful.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    exit()  

cursor = connection.cursor()
sqlquery = ("""SELECT T0.[U_Region] AS [Zone],T1.[GroupName] AS [Group], T0.[CardCode], T0.[CardName], T2.[PymntGroup] as [Payment Terms], T0.[CreditLine], T0.[Balance]  As [Total Balance]
            ,(SELECT count(*) FROM OINV WHERE CANCELED='N' and  CardCode=T0.CardCode and  year([DocDate])=Year(getdate()) Group by [CardCode]) As [Total Invoice]
            ,(SELECT sum([DocTotal]) FROM OINV WHERE CANCELED='N' and  CardCode=T0.CardCode and  year([DocDate])=Year(getdate()) Group by [CardCode]) As [SALE]
            ,(SELECT sum([PaidToDate]) FROM OINV WHERE CANCELED='N' and  CardCode=T0.CardCode and  year([DocDate])=Year(getdate()) Group by [CardCode]) As [Recovery]
            ,(SELECT sum([DocTotal]-[PaidToDate]) FROM OINV WHERE CANCELED='N' and  CardCode=T0.CardCode and  year([DocDate])=Year(getdate()) Group by [CardCode]) As [Open Invoice]
            FROM OCRD T0  

            INNER JOIN OCRG T1 ON T0.GroupCode = T1.GroupCode 
            INNER JOIN OCTG T2 ON T0.GroupNum = T2.GroupNum 

            WHERE T0.[CardType] ='C' and  T0.[validFor] ='Y' 
            Order by T0.[U_Region],T1.[GroupName],T0.[CardName]""")

cursor.execute(sqlquery)
rows = cursor.fetchall()
columns = [column[0] for column in cursor.description]
data1 = pd.DataFrame.from_records(data=rows, columns=columns)


data1.to_excel('Output\ETL_Data.xlsx', index = False)
data1.to_csv('Output\ETL_Data.csv', index=False)
connection.close()
