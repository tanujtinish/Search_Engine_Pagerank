Python Page Ranker

This is a set of programs that emulate some of the functions of a search engine.  They store their data in a SQLITE3 database named 'data.sqlite'. 
You should install the SQLite browser to view and modify  the databases from.

1st command to run:-                                                                                                                                          python make_data.py
this will 
1. create table named nodes with attributes id(for storing page id), orank(for storing previous rank of page), and nrank(for storing current rank of page)
2. create table nmaed edges with attributes startpage(for storing id for page from where edge startrs), finalpage(for storing id for page that egde is pointing to)
3. create file data.sqlite containg all these table information

Once you have a data in the database, you can run Page Rank on the data using command:-             
python calculate_rankmatrix.py 
then it will ask us to input r= number of iterations we want to calculate rank                                                   

How many iterations:??
For each iteration of the page rank algorithm it prints the average change per page of the page rank. The network initially is quite  unbalanced and so the individual page ranks are changing wildly. But in a few short iterations, the page rank converges. You  should input iterations large enough such that the page ranks converge.
You can run calculate_rankmatrix.py as many times as you like and it will simply refine the page rank the more times you run it.

If you want to restart the Page Rank calculations, 
run command :-                                                                               
python reset_rankmatrix.py 
It re-initializes all pages and set to a rank of 1.0/N. Then prints message "All pages set to a rank of 1.0" on completion

If you want to visualize the current top pages in terms of page rank,                                                              
run command :-                                                                                                                                                                     
python make_graph.py
