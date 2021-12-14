from typing import ClassVar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

import os

import json


query_text = "multi%20agent%20systems"

csv_file = f"{query_text.replace('%20','_')}.csv"
os.remove(csv_file)

json_file = f"{query_text.replace('%20','_')}.json"


with open(csv_file, "a") as f:

    f.write("num,title,num_citations,abstract\n")

    papers=[]
    j=1
    for num_paper in range(1,50):

        driver = webdriver.Firefox()

        link4pagenum = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={query_text}&highlight=true&returnType=SEARCH&matchPubs=true&pageNumber={num_paper}&returnFacets=ALL"  

        driver.get(link4pagenum)

        element_index=3
        
        while True:
            try:
                time.sleep(5)

                a = driver.find_element(By.XPATH,f"/html/body/div[5]/div/div/div/div[3]/div/xpl-root/div/xpl-search-results/main/div[2]/div[2]/xpl-results-list/div[{element_index}]/xpl-results-item/div[1]/div[1]/div[2]/h2/a")
  
                try:
                    num_citations=driver.find_element(By.XPATH,f"/html/body/div[5]/div/div/div/div[3]/div/xpl-root/div/xpl-search-results/main/div[2]/div[2]/xpl-results-list/div[{element_index}]/xpl-results-item/div[1]/div[1]/div[2]/div/div[2]/span/a")
                    num_citations_text=num_citations.text
                except:
                    num_citations_text="Papers (0)"

                driver4abstract = webdriver.Firefox()

                link_abstract = a.get_attribute("href")
                driver4abstract.get(link_abstract)

                time.sleep(5)

                b = driver4abstract.find_element(By.XPATH,"/html/body/div[5]/div/div/div/div[3]/div/xpl-root/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[3]/div[1]/div/div/div")

                element_index+=1
                
                papers.append({"id":str(j), "title":a.text, "num_citations":num_citations_text, "abstract":b.text})
                f.write(f'{j},{a.text},{num_citations_text},{b.text}\n')
                print(f"Article num {num_paper}, {j} has been reached successfully!")
                
                j+=1
                driver4abstract.close()

            except:
                break
            
            driver.close()

with open(json_file, 'w') as f:
    json.dump(papers, f)