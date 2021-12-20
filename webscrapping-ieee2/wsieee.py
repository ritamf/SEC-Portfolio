import requests

search_term = "multi agent systems"

with open(f"{search_term}.csv","w") as f:

    f.write("page_num|art_num|type|year|author|title|abstract\n")

    for page_num in range(1,1000):

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://ieeexplore.ieee.org",
            "Content-Type": "application/json",
        }
        payload = {
            "newsearch": True,
            "queryText": search_term,
            "highlight": True,
            "returnFacets": ["ALL"],
            "returnType": "SEARCH",
            "pageNumber": page_num
        }
        r = requests.post(
                f"{headers['Origin']}/rest/search",
                json=payload,
                headers=headers
            )

        page_data = r.json()
        
        for record in page_data["records"]:

            year = "null" if "publicationYear" not in record.keys() else f"{record['publicationYear']}"
            author = "null" if "authors" not in record.keys() else f"{record['authors'][0]['preferredName']}"

            f.write(f"{page_num}|{record['articleNumber']}|{record['displayContentType']}|{year}|{author}|{record['articleTitle']}|")

            try: 
                abstract_link = f"{headers['Origin']}{record['documentLink']}"
                abstract = requests.get(abstract_link).text.split('"twitter:description" content="',1)[1].split('" />', 1)[0].replace("&#039;","'")

                if abstract.count("\n") > 0: # this is necessary for words that appear in scientific notations and such
                    abstract = abstract.split("\n")

                    abstract = [line.replace("&lt;/sub&gt;","")[-1] if line.endswith("&lt;/sub&gt;") else line.replace("&lt;/sup&gt;","")[-1] if line.endswith("&lt;/sup&gt;") else line for line in abstract]

                    abstract = " ".join(abstract)

                f.write(f"{abstract}\n")
            except:
                f.write("null\n")
                print("Abstract could not be extracted...")