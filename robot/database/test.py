import mysql.connector
db=mysql.connector.connect(user="root", password="toor",database="database_name")

cursor=db.cursor()

query="SELECT Students.Id,Students.Student_name,Department.Department_name FROM Students INNER JOIN Department ON Students.Dept_Id=Department.Dept_Id"
cursor.execute(query)
rows=cursor.fetchall()
for x in rows:
   print(x)

db.close()