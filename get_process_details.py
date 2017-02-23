__author__ = 'tousif'
#!/usr/bin/python


from lxml import html
import lxml.html.clean as clean
from time import sleep
import requests
import re
import csv


inputfile=open('process_list_with_one_result.csv', 'rU')
outputfile=open('process_info_details.csv','wb')
try:
    reader=csv.DictReader(inputfile)
    fieldnames=['process_value_name', 'security_flag', 'process_detail_name', 'application_name', 'recommended', 'link']
    writer=csv.DictWriter(outputfile, fieldnames=fieldnames)

    writer.writeheader()

    safe_count=0
    for i,row in enumerate(reader):

        sleep(5)
        url = "http://www.processlibrary.com/en/search/?q="+row['process_name'].replace(" ", "+");

        process_library_page=requests.get(url)
        tree=html.fromstring(process_library_page.text)
        result=tree.xpath('//div[@class="padding-tl-20"]//text()')
        link=tree.xpath('//div[@class="row"]//a[@class="break-line"]/text()')
        security_flag=tree.xpath('//div[@class="search-security"]//text()')
        process_flag=security_flag[0].strip().split()[-1]
        title=tree.xpath('//div[@class="row"]//a[@class="link-underline"]/text()')

        if title[0].lower()==row['process_name'].lower():
            if process_flag=="safe":
                safe_count+=1

            newpage=requests.get(link[0])
            newtree=html.fromstring(newpage.text)
            newtree=clean.clean_html(newtree)
            info =newtree.xpath('//div[@class="bottom"]//div[@class="ten columns"]//text()')

            process_detail_name=""
            application=""
            recommended=""
            for j,inner_row in enumerate(info):

                inner_row=inner_row.strip()

                #print row
                if(inner_row!=""):
                    if(inner_row=="Process name:"):
                        #print info[j+1].strip()
                        process_detail_name=info[j+1].strip()

                    if(inner_row=="Application using this process:"):
                        application= info[j+1].strip()

                    if(inner_row=="Recommended:"):
                        recommended= info[j+1].strip()


            print  str(i)+": file:"+ row['process_name']+", Total Safe: "+str(safe_count)
            #print application.encode('ascii','ignore')

            writer.writerow({'process_value_name': row['process_name'], 'security_flag':process_flag,
                             'process_detail_name':process_detail_name.encode('ascii','ignore'),
                             'application_name': application.encode('ascii','ignore'),
                             'recommended':recommended.encode('ascii','ignore'), 'link': link[0]})

    print "Total Safe: "+str(safe_count)
finally:
    inputfile.close()
    outputfile.close()

#with open('process_list.csv', 'rb') as csvfile:
   # reader = csv.DictReader(csvfile)
    #for row in reader:
       # url = "http://www.processlibrary.com/en/search/?q="+row['executable_value'].replace(" ", "+");
        #print url;
       # url= "http://pcpitstop.com/libraries/process/detail.asp?fn="+row['executable_value'].replace(" ", "%20")+".html";

       # print url;



#page1=requests.get('http://www.processlibrary.com/en/search/?q=Agent.exe')
#page2=requests.get('http://pcpitstop.com/libraries/process/detail.asp?fn=smss.exe.html')
#page=requests.get('http://econpy.pythonanywhere.com/ex/001.html')
#tree= html.fromstring(page.text)
#tree2=html.fromstring(page2.text)
#tree1=html.fromstring(page1.text)

#This will create a list of buyers:
#buyers = tree.xpath('//div[@title="buyer-name"]/text()')
#This will create a list of prices
#prices = tree.xpath('//span[@class="item-price"]/text()')

#vendors= tree2.xpath('//table[@id="vendorInfo"]/text()')
#vendors= tree2.xpath('//tr/td//text()')

#all= tree1.xpath('//div[@class="padding-tl-20"]//text()')

#print vendors[1]
