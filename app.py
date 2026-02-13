import mysql.connector
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="abhi@30121310",
    database="testdb"
)
cursor = conn.cursor()
name=input("Enter Student Name:")
college=input("Enter College Name:")
r1=float(input("Enter Round1 Marks(0-10):"))
r2=float(input("Enter Round2 Marks(0-10):"))
r3=float(input("Enter round3 Marks(0-10):"))
tech=float(input("Enter technical Round Marks(0-20):"))

if len(name)>30:
    print("Student name too long")
    exit()
if len(college)>50:
    print("College name too long")
    exit()
if not (0<= r1 <=10 and 0<= r2 <=10 and 0<= r3 <=10):
    print("Round marks must be between 0 and 10")
    exit()
total=r1+r2+r3+tech
if total>=35:
    result="Selected"
else:
    result="Rejected"
insert_query = """
    INSERT INTO students1
    (name, college, marks1, marks2, marks3, TechnicalMarks, TotalMarks, Result, RankPosition)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
values = (name, college, r1, r2, r3, tech, total, result, None)
cursor.execute(insert_query, values)
conn.commit()
rank_query = """
UPDATE students1 s1
JOIN (
    SELECT name,
           (SELECT COUNT(DISTINCT s2.TotalMarks)
            FROM students1 s2 
            WHERE s2.TotalMarks > s.TotalMarks) + 1 AS new_rank
    FROM students1 s 
) ranked 
ON s1.name = ranked.name  
SET s1.RankPosition = ranked.new_rank 
"""
cursor.execute(rank_query)
conn.commit()
print("\nRecord inserted successfully!")
cursor.execute("SELECT * FROM students1 ORDER BY RankPosition ASC")
records=cursor.fetchall()
print("\nAll Students Records:")
for row in records:
    print(row)
conn.close()
