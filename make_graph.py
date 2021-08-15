import sqlite3
#from graph_tool.all import *
from igraph import *
import timeit

start_time = timeit.default_timer()
conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

cur.execute('''SELECT DISTINCT startpage FROM edges''')# get all distinct ids of pages from which edge is starting and store them in list named start_id
start_ids = list()
for row in cur: 
    start_ids.append(row[0])

beta=0.8
end_ids = list()#stores all distinct ids of pages where edges are pointing to
edges = list()#stores all edges
cur.execute('''SELECT DISTINCT startpage, finalpage FROM edges''')
for row in cur:
    start_id = row[0]
    end_id = row[1]
    edges.append(row)
    if (end_id not in end_ids) : 
        end_ids.append(end_id)

k = input('type no. of nodes you want in graph:' )
k=int(k)
oldranks = dict()#stores older ranks of all nodes
nod=list()
for i in start_ids:
    cur.execute('''SELECT nrank FROM nodes WHERE id = ?''', (i, ))
    row = cur.fetchone()
    oldranks[i] = row[0]
    if (i not in nod and i<k) : 
        nod.append(i)
for i in end_ids:
    cur.execute('''SELECT nrank FROM nodes WHERE id = ?''', (i, ))
    row = cur.fetchone()
    oldranks[i] = row[0]
    if (i not in nod and i<k) : 
        nod.append(i)
edges=list()
cur.execute('''SELECT id FROM nodes ORDER BY id DESC LIMIT 1''')
row = cur.fetchone()
total=row[0]
for (node, oldrank) in list(oldranks.items()):
    cur.execute('''SELECT DISTINCT startpage, finalpage FROM edges WHERE startpage = ?''', (node, ))
    row = cur.fetchone()
    if row is None :
        continue
    for (row in cur and row[0]<k and row[1]<k):
        edges.append((row[0],row[1]))
print(edges)
g = Graph(edges=edges, directed=True)

visual_style = {}

# Scale vertices based on degree
ranks=list()
for i in range(k):
    if (i in nod):
        ranks.append(oldranks[i])
    else:
        ranks.append(0)
visual_style["vertex_size"] = [200*x for x in ranks]
print(visual_style["vertex_size"])
# Set bbox and margin
visual_style["bbox"] = (800,800)
visual_style["margin"] = 100


plot(g, **visual_style)
cur.close()#close database

elapsed = timeit.default_timer() - start_time
print("Time Elapsed:")
print(elapsed)