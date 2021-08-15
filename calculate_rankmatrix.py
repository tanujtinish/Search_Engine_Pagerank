import sqlite3
import timeit

start_time = timeit.default_timer()
conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

cur.execute('''SELECT DISTINCT startpage FROM edges''')# get all distinct ids of pages from which edge is starting and store them in list named start_id
start_ids = list()
for row in cur: 
    start_ids.append(row[0])

print(start_ids)
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
print(start_ids)
oldranks = dict()#stores older ranks of all nodes
for i in start_ids:
    cur.execute('''SELECT nrank FROM nodes WHERE id = ?''', (i, ))
    row = cur.fetchone()
    oldranks[i] = row[0]

for i in end_ids:
    cur.execute('''SELECT nrank FROM nodes WHERE id = ?''', (i, ))
    row = cur.fetchone()
    if row is None :
        continue
    oldranks[i] = row[0]
print(oldranks)
print(edges)
# for implementing topic specific search
topics = list()# list that will contain topic_id for topic specific search
topic_specific = input('if you want topic specific search, type 1, else print 0') #get input for number of specific topics
if(int(topic_specific)==1):#if it is specific search
    num_specific_topics = input('number of specific_topics you want??') #get input for number of specific topics
    for i in range(int(num_specific_topics)):
        a = input('type topic_id for topic specific search:')
        if (int(a) not in topics) : 
            topics.append(int(a))
    print(topics)
    iter_num = input('iterations??:') #get input for number of iteration to run until r converges
    iter_num = int(iter_num)

    for i in range(iter_num):
    #calculate total rank of all nodes which are topic_specific
        newranks = dict();#will store new ranks of all nodes after calculation
        total = 0.0#variable to store total sum of old ranks of all nodes
        for (node, oldrank) in list(oldranks.items()):
            if (int(node) in topics):
                total = total + oldrank  
            newranks[node] = 0.0

        for (nodeid, oldrank) in list(oldranks.items()):

            end2_ids = list()#variable to store all page ids that particular page is pointing to
            for (start_id, end_id) in edges:
                if start_id != nodeid : continue
                end2_ids.append(end_id)
            if(len(end2_ids)==0): continue
            amount = beta*(oldrank / len(end2_ids))#value that node with id nodeid will add to nodes it is pointing to
        
            for id in end2_ids:# add rank that node with id nodeid adds
                newranks[id] += amount
        
        newtot = 0#variable to store total sum of new ranks of all nodes
        for (node, newrank) in list(newranks.items()):
            if(node in topics):
                newtot = newtot + newrank
        leak = (total - newtot) / len(topics)#leaked PageRank(1-s/|s|)

        for oo in newranks:#re-insert the leaked PageRank(1-s/N) to nodes thatare topic specific
            if(oo in topics):
                newranks[oo] = newranks[oo] + leak

        newtot = 0#variable to store total sum of new ranks of all nodes
        for (node, newrank) in list(newranks.items()):
            newtot = newtot + newrank

        totdiff = 0#variable to store sum of difference of new ranks and old ranks of all nodes
        for (node, oldrank) in list(oldranks.items()):
            newrank = newranks[node]
            diff = abs(oldrank-newrank)
            totdiff = totdiff + diff

        avediff = totdiff / len(oldranks)
        print(i,avediff)
        oldranks = newranks#re-initialize newranks to oldranks for next loop


    print(list(newranks.items()))
    #now update value of old and new ranks in node table after desired iterations
    cur.execute('''UPDATE nodes SET orank=nrank''')
    for (id, newrank) in list(newranks.items()) :
        cur.execute('''UPDATE nodes SET nrank=? WHERE id=?''', (newrank, id))
    conn.commit()#save changes in database
    cur.close()#close database
    elapsed = timeit.default_timer() - start_time
    print("Time Elapsed:")
    print(elapsed)
if(int(topic_specific)==0):#if not specific search
    
    iter_num = input('iterations??:') #get input for number of iteration to run until r converges
    iter_num = int(iter_num)

    for i in range(iter_num):
    #calculate total rank of all nodes which are topic_specific
        newranks = dict();#will store new ranks of all nodes after calculation
        total = 0.0#variable to store total sum of old ranks of all nodes
        for (node, oldrank) in list(oldranks.items()):
            total = total + oldrank  
            newranks[node] = 0.0

        for (nodeid, oldrank) in list(oldranks.items()):
            amount=0
            end2_ids = list()#variable to store all page ids that particular page is pointing to
            for (start_id, end_id) in edges:
                if start_id != nodeid : continue
                end2_ids.append(end_id)
            if(len(end2_ids)==0): continue
            amount = beta*(oldrank / len(end2_ids))#value that node with id nodeid will add to nodes it is pointing to
        
            for id in end2_ids:# add rank that node with id nodeid adds
                newranks[id] += amount
        
        newtot = 0#variable to store total sum of new ranks of all nodes
        for (node, newrank) in list(newranks.items()):
            newtot = newtot + newrank
        leak = (total - newtot) / len(newranks)#leaked PageRank(1-s/|s|)

        for oo in newranks:#re-insert the leaked PageRank(1-s/N) to nodes thatare topic specific
            newranks[oo] = newranks[oo] + leak

        newtot = 0#variable to store total sum of new ranks of all nodes
        for (node, newrank) in list(newranks.items()):
            newtot = newtot + newrank

        totdiff = 0#variable to store sum of difference of new ranks and old ranks of all nodes
        for (node, oldrank) in list(oldranks.items()):
            newrank = newranks[node]
            diff = abs(oldrank-newrank)
            totdiff = totdiff + diff

        avediff = totdiff / len(oldranks)
        print(i,avediff)
        oldranks = newranks#re-initialize newranks to oldranks for next loop


    print(list(newranks.items()))
    #now update value of old and new ranks in node table after desired iterations
    cur.execute('''UPDATE nodes SET orank=nrank''')
    for (id, newrank) in list(newranks.items()) :
        cur.execute('''UPDATE nodes SET nrank=? WHERE id=?''', (newrank, id))
    conn.commit()#save changes in database
    cur.close()#close database
    elapsed = timeit.default_timer() - start_time
    print("Time Elapsed:")
    print(elapsed)
