__author__ = 'tousif'


import requests
import json
from time import sleep
import urllib
from lxml import html
import csv
import unicodedata

inputfile=open('process_list.csv', 'rt')

# Output Files
outputfile=open('complete_process_list_with_number_of_results.csv','wt')
oneresultfile= open('process_list_with_one_result.csv','wt')
noresultfile= open('process_list_output_with_noresult.csv','wt')
mtoneresultfile= open('process_list_output_with_morethanone_result.csv','wt')

try:
    reader=csv.DictReader(inputfile)

    # Fieldnames for different output files
    fieldnames=['process_name','no_of_results']
    fieldnames_results=['process_name','no_of_results','Title' ,'url']
    fieldnames_more_results=['index','process_name','estimated_results_count','Title' ,'url']
    writer=csv.DictWriter(outputfile, fieldnames=fieldnames)
    writer_for_one= csv.DictWriter(oneresultfile, fieldnames=fieldnames_results)
    writer_for_no= csv.DictWriter(noresultfile, fieldnames=fieldnames)
    writer_for_mtone= csv.DictWriter(mtoneresultfile, fieldnames=fieldnames_more_results)

    writer.writeheader()
    writer_for_mtone.writeheader()
    writer_for_no.writeheader()
    writer_for_one.writeheader()

    # counters 
    total_1=0
    total_mt1=0
    total_0=0
    total_found=0

    for i,row in enumerate(reader):
        sleep(120) # Waiting time between each call. Otherwise Google will Block you
        
        # Search Query
        query = '"'+row["executable_value"]+'" site:shouldiremoveit.com'

        #NB. add 'start=3' to the query string to move to later results
        r = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + query)

        # JSON object
        theJson = r.content
        theObject = json.loads(theJson)

        # results with no results
        if len(theObject['responseData']['results'])==0:
            total_found=0
            total_0=total_0+1
            writer_for_no.writerow({'process_name': row['executable_value'], 'no_of_results':total_found})

        else:
        # Print it all out

            total_found= len(theObject['responseData']['results'])

            # processes with one results
            if total_found==1:
                total_1=total_1+1
                for index,result in enumerate(theObject['responseData']['results']):
                       # print str(index+1) + ") " + result['titleNoFormatting']
                       # print result['url']
                        writer_for_one.writerow({'process_name': row['executable_value'], 'no_of_results':total_found,
                                                 'Title': result['titleNoFormatting'], 'url': result['url']})
            else:
                #processes with multiple results
                total_mt1=total_mt1+1
                total_found=theObject['responseData']['cursor']['estimatedResultCount']
                for index,result in enumerate(theObject['responseData']['results']):
                        title=result['titleNoFormatting']
                        writer_for_mtone.writerow({'index': i, 'process_name': row['executable_value'], 'estimated_results_count':theObject['responseData']['cursor']['estimatedResultCount'],
                                                   'Title': title.encode('utf8'), 'url': result['url']})
    
        print str(i)+ ": file:"+ row['executable_value']+\
              ", Results: "+str(total_found)+", total 0:"+ str(total_0)+ ", total_1: "+ str(total_1)+ ", MT: "+ str(total_mt1)

        writer.writerow({'process_name': row['executable_value'], 'no_of_results':total_found})

    print "Total Unknown: "+str(total_0)+" , Total Known: "+ str(total_1) + "Total confusing: "+ str(total_mt1)
finally:
    inputfile.close()
    outputfile.close()
    oneresultfile.close()
    noresultfile.close()
    mtoneresultfile.close()



