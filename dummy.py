import requests

theme = "multi agent systems"

page_num = 89

headers = {
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://ieeexplore.ieee.org",
    "Content-Type": "application/json",
}
payload = {
    "newsearch": True,
    "queryText": theme,
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

record = pd[24]

try: # try to request abstract link and to get the abstract 
    abstract_link = f"{headers['Origin']}{record['documentLink']}"
    print(abstract_link)
    abstract = requests.get(abstract_link).text
    
    with open("dummyArticle.html","w") as f:
        f.write(abstract) # writes the obtained html page, which includes the whole abstract

    authors = ", ".join([f"{record['authors'][i]['preferredName']}" for i in range(len(record['authors']))]) if "authors" in record.keys() else "null"

    print(authors)

    # get the abstract substring out of the html page
    abstract = abstract.split('"twitter:description" content="',1)[1].split('" />', 1)[0].replace("&#039;","'")

    if abstract.count("\n") > 0: # this is necessary for words that appear in scientific notations and such
        abstract = abstract.split("\n")
        abstract = [line.replace("&lt;/sub&gt;","")[-1] if line.endswith("&lt;/sub&gt;") else line.replace("&lt;/sup&gt;","")[-1] if line.endswith("&lt;/sup&gt;") else line for line in abstract]
        abstract = " ".join(abstract)

    with open(f"dummyAbstract.txt","w") as f:
        f.write(abstract)

except:
    f.write("null\n")
    print("Abstract could not be extracted...")
