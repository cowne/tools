import requests
import urllib3
import argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="Checking available URL")
parser.add_argument('-l','--list', type=str, help='List of URL',required=True)
parser.add_argument('-o', '--output', type=str, help='Output file contain list available URL')
args = parser.parse_args()

def getURL(file):
    urls = []
    with open(file, 'r') as url_lists:
        for url in url_lists:
            urls.append(url.strip('\n'))
    return urls

def write_to_file(urls,file):
    with open(file, 'a') as file:
        for url in urls:
            file.write(url+'\n')
        file.close()

def check_url(urls):
    url_alive = []
    url_death = {}
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            url_death.update({url: type(e)})
        else:
            url_alive.append(url)

    return url_alive, url_death

def main():
    urls = getURL(args.list)
    url_alive, url_death = check_url(urls)

    if args.output:
        write_to_file(url_alive, args.output)
        print(f'[!] The reports save in {args.output}.\n')

    print('\n------------URL AVAILABLE--------------------')
    print(f'[!] Totals URL available: {len(url_alive)}.\n')
    for url in url_alive:
        print(f'[+] {url}')

    print('\n-------------URL DEATH-------------------')
    print(f'[!] Totals URL not available:  {len(url_death)}.\n')
    for url,error in url_death.items():
        print(f'[-] {url}: {error}')

if __name__ == '__main__':
    main()
    print('\n[!] DONE THE PROCESS. PLEASE CHECK THE RESULTS.')