import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="mydatabase"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT answer_1 FROM customers")
myresult = mycursor.fetchall()
count = 0
for x in myresult:
    if x != ('',):
        count += 1
print(count)
