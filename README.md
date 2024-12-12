# LinkedIn Username/Email scrapper

This script will scrape LinkedIn based on company IDs and will return names and emails.

## linkedin_email_scraper.py usage:
```
usage: browser_dev_linkedin.py [-h] [-p PROXY] [-pp PROXY_PORT] [-c [COOKIE]] [-fi] [-li] [-f] [-l] [-e [EMAIL]] [-d [DELIMITER]] [-i [COMPANY_ID]] [-o [LOG_FILE]]

Selenium LinkedIn Scraper >:D

optional arguments:
  -h, --help            show this help message and exit
  -p PROXY, --proxy PROXY
                        The proxy ip in format {127.0.0.1}.
  -pp PROXY_PORT, --proxy_port PROXY_PORT
                        The proxy port in format {8080}.
  -c [COOKIE]           LinkedIn li_at session cookie. [AQEDAR1hbLMFawzeAAABd5bk........CQBPcCMRrTC5t55shATUJv]
  -m                    If multiple first names exist, it will generate an email for each first name (e.g. john.smith@test.com and dan.smith@test.com).
  -fi                   Save first name as first initial.
  -li                   Save last name as last initial.
  -f                    Save first name.
  -l                    Save last name.
  -e [EMAIL]            Append a domain to each name.
  -d [DELIMITER]        Delimiter to split between first and last name.
  -i [COMPANY_ID]       Company ID found in URL of LinkedIn business page. [XXXXXXX]
  -o [LOG_FILE]         Output list to file.
```
   Basic usage of script:
   
    python3 linkedin_email_scraper.py -d " " -i 123456 -c AQEDAR1hbLMFawzeAAABd5bk........CQBPcCMRrTC5t55shATUJv
    
   Hardcoded li_at cookie [line 35] in script:
   
    python3 linkedin_email_scraper.py -i 123456
    
   Advanced usage of linkedin_email_scraper.py:
   
    $ python3 linkedin_email_scraper.py -p 127.0.0.1 -pp 8080 -d "." -e microsoft.com -fi -l -o microsoft.txt
    [+] Scraping page 1 Good:12 Bad:1
    [+] Scraping page 2 Good:21 Bad:1
    [+] Scraping page 3 Good:28 Bad:3
    [+] Scraping page 4 Good:36 Bad:4
    [+] Scraping page 5 Good:44 Bad:4
    [+] Scraped (saved) 43 names!
    [-] Names to fix [Enter to skip] ctrl+c if UDGAF: 4
    [-] Fix me [Angela M.]: 
    [-] Fix me [Ryan D.]: 
    [-] Fix me [Yuri Diogenes, M.S. Cybersecurity]: Yuri Diogenes
    [-] Fix me [Nina K.]: 
    [+] Saved to microsoft.txt
    
   Example output of microsoft.txt:
   
    M.Russinovich@microsoft.com
    S.Oneeta@microsoft.com
    J.Tiplitsky@microsoft.com
    B.Arsenault@microsoft.com
    A.Patil@microsoft.com
    D.Weston@microsoft.com
    D.Taylor@microsoft.com
    S.Lieu@microsoft.com
    K.Kennebrew@microsoft.com
    J.Victorino@microsoft.com
    Y.Diogenes@microsoft.com
   
