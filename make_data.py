import sqlite3
import timeit

start_time = timeit.default_timer()
conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS nodes(id INTEGER PRIMARY KEY,orank REAL, nrank REAL)''')#create table nmaed nodes with attributes id(for storing page id), orank(for storing previous rank of page), and nrank(for storing current rank of page)
l = 0
cur.execute('''CREATE TABLE IF NOT EXISTS edges(startpage INTEGER,finalpage INTEGER)''')#create table nmaed edges with attributes startpage(for storing id for page from where edge startrs), finalpage(for storing id for page that egde is pointing to)
with open('p2p-Gnutella04.txt', 'r') as f:#read data
    for line in f:#loop for every line in data
        y = line.split()
        print(l)
        l += 1
        start_id = int(y[0])#for storing id for page from where edge startrs
        end_id = int(y[1])#for storing id for page that egde is pointing to
        cur.execute('SELECT * FROM nodes WHERE id=?' , (start_id,))
        row = cur.fetchone()
        if(row is None) :
            cur.execute('INSERT OR IGNORE INTO nodes ( id, orank, nrank) VALUES ( ?, 0.0 , 1.0 )' , (start_id,))
        cur.execute('INSERT OR IGNORE INTO edges (startpage, finalpage) VALUES ( ?, ? )', ( start_id, end_id ))
        conn.commit()#save changes in database
        cur.execute('SELECT * FROM nodes WHERE id=?' , (end_id,))
        row = cur.fetchone()
        if(row is None) :
            cur.execute('INSERT OR IGNORE INTO nodes ( id, orank, nrank) VALUES ( ?, 0.0 , 1.0 )' , (end_id,))
        conn.commit()#save changes in database
cur.execute('''SELECT COUNT(*) AS c from nodes''')
row = cur.fetchone()
total=row[0]
cur.execute('''SELECT * FROM nodes''')
new_rank=1.0/total
cur.execute('''UPDATE nodes SET nrank=?''', (new_rank, ))
conn.commit()#save changes in database
cur.close()#close database
elapsed = timeit.default_timer() - start_time
print("Time Elapsed:")
print(elapsed)