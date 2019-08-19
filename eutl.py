import requests , reprlib
from bs4 import BeautifulSoup
from urllib.request import urlopen 
from itertools import groupby 

# Current date
import datetime
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day

# Name and date of csv
daname = "eutl.csv"
daname = str(year)+"-"+str(month)+"-"+str(day)+"-"+daname
outFile = open(daname, 'w', newline='', encoding='utf8')

# Add header to csv with variable names
myhead = ["tid", "type", "date", "status", "transreg", "acctype", "accid", "accho", "aqreg", "aqacctype", "aqaccid", "aqaccho", "nounits"]
myhead = ";".join(myhead)
outFile.write(myhead)

### Add the number of max. pages to search here
maxpage = 44168

# Loop over html pages
for pagenumber in range(0,maxpage-1):
    try:
        # URL to search
        # http://ec.europa.eu/environment/ets/transaction.do?languageCode=en&startDate=&endDate=&transactionStatus=4&fromCompletionDate=&toCompletionDate=&transactionID=&transactionType=-1&suppTransactionType=-1&originatingRegistry=-1&destinationRegistry=-1&originatingAccountType=-1&destinationAccountType=-1&originatingAccountIdentifier=&destinationAccountIdentifier=&originatingAccountHolder=&destinationAccountHolder=&search=Search&currentSortSettings=&resultList.currentPageNumber=1
        url1 = "http://ec.europa.eu/environment/ets/transaction.do?languageCode=en&startDate=&endDate=&transactionStatus=4&fromCompletionDate=&toCompletionDate=&transactionID=&transactionType=-1&suppTransactionType=-1&originatingRegistry=-1&destinationRegistry=-1&originatingAccountType=-1&destinationAccountType=-1&originatingAccountIdentifier=&destinationAccountIdentifier=&originatingAccountHolder=&destinationAccountHolder=&currentSortSettings=&resultList.currentPageNumber="
        url2 = "&nextList=Next%3E"
        url = url1 + str(pagenumber) + url2

        # Feedback on current stage
        progress = ((pagenumber+1)/(maxpage))*100
        print("  Loading page %i of %i: Progress is %.1f percent" %(pagenumber+1, maxpage, progress), end="\r")

        # Generate empty list to store this pages content
        mylist=[]
        # Get entire HTML content 
        soup = BeautifulSoup(urlopen(url), "lxml") # Homepage wird als soup gelade
        # Get table content        
        tablecontent = soup.find('table', {'id':'tblTransactionSearchResult'})
        # Get row content for each row   
        rows = tablecontent.find_all('tr')
        for row in rows:
            # Get cell content for each cell in row
            cells = row.find_all('td',{'class':'bgcelllist'})
            for cell in cells:
                # Request text content of cell
                celltext=cell.text.strip()
                # Write cell to list
                mylist.append(str(celltext).rstrip())
                # Write csv delimiter
                mylist.append(";")
            # Linebreak
            mylist.append("\n")

        # Remove consecutive duplicates in list (i.e. "\n")
        mylist =  [x[0] for x in groupby(mylist)]   
        # Append mylist to csv-file
        for element in mylist:
            outFile.write(element)

    # Exeption/error message if page download fails
    except Exception as e:
        print("Error in loop %s" %(pagenumber))

# Close output file
outFile.close()

# Print end statement including time needed since start
end = datetime.datetime.now()
print("Finish. Time needed to download %i pages (h/m/s): %.7s " %(maxpage, end-now))
