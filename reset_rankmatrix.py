import sqlite3
import timeit

start_time = timeit.default_timer()
conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

cur.execute('''SELECT COUNT(*) AS c from nodes''')
row = cur.fetchone()
total=row[0]
print("total no. of nodes in our rank system are:")
print(total)

cur.execute('''SELECT * FROM nodes''')
new_rank=1.0/total
cur.execute('''UPDATE nodes SET nrank=?, orank=0.0''', (new_rank, ))#All pages re-initialized and set to a rank of 1.0/N
conn.commit()#save changes in database
cur.close()#close database

print("All pages set to a rank of 1.0")
elapsed = timeit.default_timer() - start_time
print("Time Elapsed:")
print(elapsed)