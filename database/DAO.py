from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    @staticmethod
    def getAnno():
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)

        result = []

        query = """ select distinct year(gds.`Date`) as anno
                from go_sales.go_daily_sales gds """

        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getCountry():
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)

        result = []

        query = """ select distinct gr.Country 
from go_sales.go_retailers gr 
 """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getRetailerCountry(country):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)

        result = []

        query = """ select distinct *
from go_sales.go_retailers gr 
where gr.Country = %s
     """

        cursor.execute(query,(country, ))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getArchi(c1,c2,anno,idMap):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select gr2.Retailer_code as r1, gr1.Retailer_code as r2, count(distinct gds2.Product_number) as n
from (select distinct *
from go_sales.go_retailers gr 
where gr.Country = %s) gr1,
(select distinct *
from go_sales.go_retailers gr 
where gr.Country = %s)gr2, go_sales.go_daily_sales gds, go_sales.go_daily_sales gds2
where gr2.Retailer_code = gds2.Retailer_code 
and gr1.Retailer_code = gds.Retailer_code
and gds.Product_number=gds2.Product_number 
and year(gds2.`Date` )= %s
and year(gds2.`Date` )= year(gds.`Date`) 
and gr2.Retailer_code < gr1.Retailer_code
group by gr2.Retailer_code , gr1.Retailer_code
         """

        cursor.execute(query, (c1,c2,anno, ))

        for row in cursor:
            result.append((idMap[row["r1"]],idMap[row["r2"]],row["n"]))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getRet():
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)

        result = []

        query = """ select *
from go_sales.go_retailers gr """

        cursor.execute(query)

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()

        return result