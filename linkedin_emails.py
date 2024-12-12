import sys
import time
import argparse
import re
import math
import unicodedata
import time
import requests
from urllib.request import urlopen
import string
from bs4 import BeautifulSoup
import urllib.parse
import collections


requests.packages.urllib3.disable_warnings()


def argparser():
    cookie = '' #hardcode me

    parser = argparse.ArgumentParser(description="Selenium LinkedIn Scraper >:D")
    parser.add_argument("-p", "--proxy", help="The proxy ip in format {127.0.0.1}.", default='127.0.0.1')
    parser.add_argument("-pp", "--proxy_port", help="The proxy port in format {8080}.", default='8080')
    parser.add_argument('-c', action='store', dest='cookie', nargs='?', default=cookie, const=cookie,
                        help='LinkedIn li_at session cookie. [AQEDAR1hbLMFawzeAAABd5bk........CQBPcCMRrTC5t55shATUJv]')
    parser.add_argument('-m', action='store_true', dest='multiple',
                        help='If multiple first names exist, it will generate an email for each first name (e.g. john.smith@test.com and dan.smith@test.com).')
    parser.add_argument('-fi', action='store_true', dest='first_initial',
                        help='Save first name as first initial.')
    parser.add_argument('-li', action='store_true', dest='last_initial',
                        help='Save last name as last initial.')
    parser.add_argument('-f', action='store_true', dest='first_name',
                        help='Save first name.')
    parser.add_argument('-l', action='store_true', dest='last_name',
                        help='Save last name.')
    parser.add_argument('-e', action='store', dest='email', nargs='?', default=None, const=None,
                        help='Append a domain to each name.')
    parser.add_argument('-d', action='store', dest='delimiter', nargs='?', default='', const='',
                        help='Delimiter to split between first and last name.')
    parser.add_argument('-i', action='store', dest='company_id', nargs='?', default=None, const=None,
                        help='Company ID found in URL of LinkedIn business page. [XXXXXXX]')
    parser.add_argument('-o', action='store', dest='log_file', nargs='?', default='output.txt', const='output.txt',
                        help='Output list to file.')
    return parser.parse_args()

def find_names(): # search for names in loaded page
    raw_names = []

    def remove_accents(input_str):
        # Normalize string to decompose characters (NFD)
        nfkd_form = unicodedata.normalize('NFD', input_str)
        # Remove diacritics by excluding combining marks
        return ''.join(char for char in nfkd_form if not unicodedata.category(char).startswith('M'))

    # Convert the content to ASCII-equivalent by removing accents
    ascii_content = remove_accents(respdata)

    # Regular expression to match names in the format: View <Name>’s profile
    name_pattern1 = r'&quot;View\s([A-Za-z\s\-]+(?: [A-Z]\.)?)’s\sprofile&quot;'
    name_pattern2 = r'&quot;View\s([A-Za-z\s\-]+(?: [A-Z]\.)?)’\sprofile&quot;'

    # Extract all matching names
    names1 = re.findall(name_pattern1, ascii_content)
    names2 = re.findall(name_pattern2, ascii_content)
    combined_matches = list(set(names1 + names2))

    # Output the names found
    print("Names found:", combined_matches)
    raw_names.extend(combined_matches)

    return raw_names

def login():
    if len(args.cookie) <= 0:
        sys.exit('[-] You haven\'t hardcoded or entered your li_at cookie yet d3rp.')

    print('[+] Logging in')
    url = f'https://www.linkedin.com/search/results/people/?currentCompany=["{args.company_id}"]&origin=COMPANY_PAGE_CANNED_SEARCH&page=1'
    s = requests.Session()
    headers = ""
    cookie_name = "li_at"
    cookies = {cookie_name: args.cookie}
    if args.proxy is not None:
        r = requests.get(url, cookies=cookies, headers=headers, verify=False)
    else:
        r = requests.get(url, cookies=cookies, headers=headers, proxies=proxies, verify=False)

    content = r.content.decode('utf-8')

    return content

def get_pages():
    print("[+] Waiting for hidden elements to unhide.")
    time.sleep(5)
    results_pattern = r'&quot;(\d+)\sresults&quot;'
    pages = None
    match = re.search(results_pattern, respdata)
    if match:
        total_results = int(match.group(1))
        print(f"Total results: {total_results}")

        # Calculate the number of pages (10 results per page)
        results_per_page = 10
        pages = math.ceil(total_results / results_per_page)
        print(f"Total pages: {pages}")
    else:
        print("No results found.")
    return pages

def prompt(name):
    fix_name = input('[-] Fix me ['+name+']: ')
    return fix_name

def name_format(name):
    first_name = name.split(' ')[0]
    last_name = name.split(' ')[-1]
    f_init = name.split(' ')[0][0]
    l_init = name.split(' ')[1][0]
    delimiter = args.delimiter
    if args.email is not None:
        email = '@' + args.email
    else: email = ''
    if args.first_initial and args.last_initial:
        name = f_init + delimiter + l_init + email; return name
    elif args.first_initial:
        name = f_init + delimiter + last_name + email; return name
    elif args.last_initial:
        name = first_name + delimiter + l_init + email; return name


    elif args.first_name and args.last_name:
        name = first_name + delimiter + last_name + email; return name
    elif args.first_name:
        name = first_name + email; return name
    elif args.last_name:
        name = last_name + email; return name
    else:
        return first_name + delimiter + last_name + email

def log_names():
    global good; good = list(set(good))
    global bad; bad = list(set(bad))
    log_file = open(args.log_file, 'w')
    print('[+] Scraped (saved) '+str(len(good))+' names!')


    for name in good:
        count_names = len(name.split(" "))
        if count_names > 2 and args.multiple:
            old_name = name
            name = name_format(name)
            log_file.write(name); log_file.write('\n')
            second_name = old_name.split(" ",1)[1]
            second_name = name_format(second_name)
            log_file.write(second_name); log_file.write('\n')
        else:    
            name = name_format(name)
            log_file.write(name); log_file.write('\n')


    print('[-] Names to fix [Enter to skip] ctrl+c if UDGAF: '+str(len(bad)))
    for name in bad:
        new_name = prompt(name)
        if new_name == '':
            pass
        else:
            count_names = len(new_name.split(" "))
            if count_names > 2  and args.multiple:
                old_name = new_name
                new_name = name_format(new_name)
                log_file.write(new_name); log_file.write('\n')
                second_name = old_name.split(" ",1)[1]
                second_name = name_format(second_name)
                log_file.write(second_name); log_file.write('\n')
            else:    
                new_name = name_format(new_name)
                log_file.write(new_name); log_file.write('\n')


    log_file2 = open("names_" + args.log_file, 'w')
    log_file2.write("\n".join(good)); log_file2.write('\n')
    log_file2.write("\n".join(bad)); log_file2.write('\n')
    print('')
    print('[+] Emails saved to ' + str(args.log_file))
    print('[+] Names saved to ' + str("names_" + args.log_file))

def filter_names(prospects):
    for name in prospects:
        if not name.replace(' ', '').isalpha(): bad.append(name)
        else: good.append(name)

if __name__ == '__main__':
    url = 'https://www.linkedin.com/'

    all_names = []
    good = []
    bad = []
    try:
        args = argparser()
        http_proxy  = "http://" + args.proxy + ":" + args.proxy_port
        https_proxy  = "http://" + args.proxy + ":" + args.proxy_port
        proxies = {
              "http"  : http_proxy,
              "https" : https_proxy
            }
        respdata = login()
        pages = get_pages()
        for page in range(1, pages+1):
            url = f'https://www.linkedin.com/search/results/people/?currentCompany=["{args.company_id}"]&origin=COMPANY_PAGE_CANNED_SEARCH&page={page}'
            if page != 1:
                # print(url)
                headers = ""
                cookie_name = "li_at"
                cookies = {cookie_name: args.cookie}
                if args.proxy is not None:
                    r = requests.get(url, cookies=cookies, headers=headers, verify=False)
                else:
                    r = requests.get(url, cookies=cookies, headers=headers, proxies=proxies, verify=False)
                respdata = r.content.decode('utf-8')
                time.sleep(4)
            try:
                entries = find_names()
            except Exception as e:
                break
            try:
                filter_names(entries)
            except Exception as e:
                break
            print("[+] Scraping page " + str(page) + " Good:" + str(len(good)) + " Bad:" + str(len(bad)))
        log_names()
        sys.exit()
    except KeyboardInterrupt:
        sys.exit('\n[-] Exiting')
