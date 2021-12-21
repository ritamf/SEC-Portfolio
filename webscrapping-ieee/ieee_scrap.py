from selenium import webdriver
from selenium.webdriver.common.by import By
import time

f=open('paperScraping2.csv','w')
papers={}
j=1
for i in range(1,105):
    
    driver = webdriver.Firefox()
    if i==1:
        driver.get("https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=5g%20wave%20propagation")
    else:
        driver.get("https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=5g%20wave%20propagation&highlight=true&returnType=SEARCH&matchPubs=true&pageNumber="+str(i)+"&returnFacets=ALL")
    element=3
    while True:
        try:
            papers[j]={}
            time.sleep(15)

            a = driver.find_element(By.XPATH,"/html/body/div[5]/div/div/div/div[3]/div/xpl-root/div/xpl-search-results/main/div[2]/div[2]/xpl-results-list/div["+str(element)+"]/xpl-results-item/div[1]/div[1]/div[2]/h2/a")
            papers[j]['title']=a.text
            print(j)
            print('title:'+a.text)
            link_abstract=a.get_attribute('href')
            
            try:
                nCit=driver.find_element(By.XPATH,"/html/body/div[5]/div/div/div/div[3]/div/xpl-root/div/xpl-search-results/main/div[2]/div[2]/xpl-results-list/div["+str(element)+"]/xpl-results-item/div[1]/div[1]/div[2]/div/div[2]/span/a")

                papers[j]['nCit']=nCit.text
            except:
                papers[j]['nCit']="Papers (0)"
            print(papers[j]['nCit'])

            year = driver.find_elements(By.XPATH,"/html/body/div[5]/div/div/div/div[3]/div/xpl-root/div/xpl-search-results/main/div[2]/div[2]/xpl-results-list/div["+str(element)+"]/xpl-results-item/div[1]/div[1]/div[2]/div/div/span/")
            print(year)


            driver2 = webdriver.Firefox()

            driver2.get(link_abstract)

            time.sleep(15)

            b = driver2.find_element(By.XPATH,"/html/body/div[5]/div/div/div/div[3]/div/xpl-root/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[3]/div[1]/div/div/div")
            papers[j]['abstract']=b.text
            print('abstract:'+b.text)
            
            
            
            element+=1
            
            f.write("{}|{}|{}|{}\n".format(j,papers[j]['title'],papers[j]['nCit'],papers[j]['abstract']))
            j+=1
            driver2.close()
        except:
            break
        
        driver.close()



