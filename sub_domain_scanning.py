try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")
from urllib.parse import urlparse
import argparse

parser = argparse.ArgumentParser(description='Finding subdomains using Google Dork.')
parser.add_argument('-d', '--domain', type=str, help='Domain to get subdomains', required=True)
parser.add_argument('-a', '--amount', type=int, help='Amount of the results', required=False)
args = parser.parse_args()

def get_subdomain(domain):
    subdomain_lists = []
    subdomain_lists.append(domain+'.*')
    subdomain_lists.append("*."+domain)
    subdomain_lists.append("*.*."+domain)
    subdomain_lists.append("*.*.*"+domain)
    subdomain_lists.append("*.*.*.*"+domain)
    return subdomain_lists

def get_subdomain_from_gg(domain,amount):
    subdomain_list = get_subdomain(domain)
    total_urls_lists = []

    if amount == 0:
        stop = 10
    else:
        stop = amount

    for url in subdomain_list:
        query = "site:DOMAIN"
        query = query.replace("DOMAIN", url)
        urls_list = list(search(query=query, num=10,stop=stop,pause=2))
        total_urls_lists.extend(urls_list)
    
    subdomain_results = []
    for url in total_urls_lists:
        subdomain_results.append(urlparse(url).netloc)

    subdomain_results = list(set(subdomain_results)) 
    return subdomain_results

def main():
    subdomains_result = get_subdomain_from_gg(args.domain, args.amount)
    print(f"---RESULTS SCANNING SUBDOMAIN FROM DOMAIN \"{args.domain}\"-----")
    for subdomain in subdomains_result:
        print(subdomain)
    
if __name__=='__main__':
    main()