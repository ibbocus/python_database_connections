from database_connection import Database_OOP
import pandas as pd



class SQLQueries:
    def __init__(self):
        pass

    def color_negative_red(self, shiptime):
        for i in shiptime:
            if i < 20:
                color = 'red'
            elif i > 20:
                color = 'green'
            else:
                color = 'black'
            return 'color: %s' % color

    def shiptime(self):
        object = Database_OOP()
        cursor = object.connect_sql()
        sql_command = """SELECT 
             CONCAT(sq1.MonthName,' ', sq1.YearOrdered) "Date Ordered"
            ,AVG("ShipTimePerproductindays") "AverageShipTimePerproductindays"
        /*This uses the subquery information and averages the amount of shipping time for the column*/
        FROM
        
                (SELECT
                     DATEDIFF(d,o.orderdate,o.ShippedDate) "ShipTimePerproductindays"
                    ,MONTH(o.OrderDate) "MonthOrdered"
                    ,YEAR(o.orderdate) "YearOrdered"
                    ,DateName(MONTH,DATEADD(MONTH,MONTH(o.orderdate) , 0 ) - 1 ) "MonthName"
                /* This converts the month number to month name */
                FROM
                    Orders o) sq1, Orders o
        WHERE
            o.ShippedDate IS NOT NULL
        /* This subquery gives the time it took to ship each order, and also the month that the order was made*/
        GROUP BY
             sq1.YearOrdered
        /*This tells the AVG function to only average the shiptimes for each month*/
            ,sq1.MonthName
            ,sq1.MonthOrdered
        ORDER BY
             CONVERT(datetime, CONCAT(sq1.YearOrdered,'/',sq1.MonthOrdered,'/','1'))
        /* This puts it in a nice format for excel*/"""
        rows = cursor.execute(sql_command)  # execute query using connection/ cursor
        date = []  # Setting up empty list for date values
        avg_shiptime = []

        for keys, values in rows:
            date.append(keys)
            avg_shiptime.append(values)
        # print(date)
        # print(avg_shiptime)
        df = pd.DataFrame()
        # df.style.applymap(self.color_negative_red(avg_shiptime))
        df['Date'] = date  # Naming the column 'Date' and filling it with the data from the list previously created
        df['Shiptime'] = avg_shiptime

        print(df.head(len(date)))

    def avg_query(self):
        a = Database_OOP()
        cursor = a.connect_sql()
        query = "SELECT AVG(UnitPrice) FROM Products"
        rows = cursor.execute(query)  # execute query using connection/ cursor
        a = []
        for row in rows:
            a.append(row)
        df = pd.DataFrame()
        df['Average Price'] = a  # Naming the column 'Date' and filling it with the data from the list previously created
        print(df)





# object = Database_OOP()
# object.connect_sql()
