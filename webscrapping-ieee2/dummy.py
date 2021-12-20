import requests

search_term = "multi agent systems"

with open(f"dummy.html","w") as f:

    page_num = 2

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
    
    pd = page_data["records"]

    try: 
        abstract_link = f"{headers['Origin']}{pd[8]['documentLink']}"
        abstract = requests.get(abstract_link).text.split('"twitter:description" content="',1)[1].split('" />', 1)[0].replace("&#039;","'")

        if abstract.count("\n") > 0: # this is necessary for words that appear in scientific notations and such
            abstract = abstract.split("\n")

            abstract = [line.replace("&lt;/sub&gt;","")[-1] if line.endswith("&lt;/sub&gt;") else line.replace("&lt;/sup&gt;","")[-1] if line.endswith("&lt;/sup&gt;") else line for line in abstract]

            abstract = " ".join(abstract)

        f.write(abstract)
    except:
        f.write("null\n")
        print("Abstract could not be extracted...")

