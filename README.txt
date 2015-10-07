a) Students:
	Robert Dadashi-Tazehozi, UNI: rd2669
	Sakhar Alkhereyf       , UNI: sa3147

b) List of files:
	i.  “main.py"
		a python script for the project
	ii.  “transcript_musk.txt”
		the transcript for query ‘musk’ with 0.9 precision@10
	iii. “transcript_gates.txt”
		the transcript for query ‘gates’ with 0.9 precision@10
	iv.  “transcript_taj_mahal.txt”
		the transcript for query ‘taj mahal’ with 0.9 precision@10
	v.   “README”
		this file

c) Usage: python main.py <query> <precision>
	<query> should be in single quotes and <precision> a real number
 	between 0 - 1 
example: python main.py \'bills gates\' 0.6

d)
 i. class Document()
	ADT to store the information for a given document returned from Bing.

 ii. parse_entry(entry)
	a function to parse entry (tag of the xml file returned from Bing)
 	and fill information (ID, Title, Description, DisplayUrl, Url) in an
	object of Document type.
 iii. calc_tf_idf(relevant, nonrel)
	a function to calculate tf-idf values for tokens in relevant
        documents marked by the user
 iv. expand_order_query(query, relevant, nonrel)
	a function to expand the query from the previous iteration
        with a single word and order the new query
 v. run(query, target_precision)
	a function to iterate until target precision reached
            Call Bing API
            Ask user to mark relevant documents
	this function will be called by the main call
e) At each iteration, we ask the user to mark which documents are relevant and which are not. Then we store relevant and non relevant documents in two different lists; these lists are expanding at each iteration, so we keep documents from the previous iterations.
Then we calculate tf-idf for every term in the relevant documents and pick the term with the highest tf-idf value.
We add that term to the previous query string, then we reorder words according to their average position of first appearance in the relevant documents.
At the end of each iteration, we check if we reached the targeted precision, if so then terminate or continue to the next iteration. If our precision is zero or the number of returned documents from Bing < 10 we just terminate.

f) XfbHf/vIn9YQOGFXSYwPnxOOmIWdeM95n39nD5s4FxI

g) We tried many techniques and methods, such as chi2 to extract the most important features (i.e. terms) but we found that tf-idf works better than other feature extraction methods.