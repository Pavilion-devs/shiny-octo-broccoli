import requests
from app.utils import get_retriever
import os
from dotenv import load_dotenv
load_dotenv()

# Lazy-loaded retriever to allow app to start quickly
_retriever = None

def get_lazy_retriever():
    global _retriever
    if _retriever is None:
        print("Initializing retriever (first request)...")
        _retriever = get_retriever()
    return _retriever

class LazyRetriever:
    """Proxy class that delays retriever initialization until first use"""
    def invoke(self, *args, **kwargs):
        return get_lazy_retriever().invoke(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(get_lazy_retriever(), name)

retriever = LazyRetriever()

def brave_search_results(query:str,count:int=5):
    """Direct Brave search API call"""
    api_key=os.getenv("BRAVE_API_KEY")
    url="https://api.search.brave.com/res/v1/web/search"
    headers={
        "Accept":"application/json",
        "Accept-Encoding":"gzip",
        "X-Subscription-Token":api_key
    }
    params={"q":query,"count":count}
    response=requests.get(url,headers=headers,params=params)
    response.raise_for_status()
    data=response.json()
    results=[]
    for item in data.get("web",{}).get("results",[]):
        results.append(
            {
                "title":item.get("title",""),
                "link":item.get("url",""),
                "snippet":item.get("description","")
            }
        )
    return results

__all__ = ["retriever","brave_search_results"]



