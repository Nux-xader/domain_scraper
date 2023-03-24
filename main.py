import os
import time
import requests
from threading import Thread
from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36"}


def parse(url:str, saveto:str, cookie:str):
    print(url)
    try:
        headers["cookie"] = cookie
        content = requests.get(url, headers=headers).text
    except Exception as e:
        print(f" [-] Failed {e}")
        return
    
    open("a.html", "w").write(content)
    print(BeautifulSoup(content, "html.parser").find_all("td", {"class": "field_domain"}))

    domains = "\n".join(tuple(map(lambda i: i.text, BeautifulSoup(content, "html.parser").find_all("td", {"class": "field_domain"}))))
    open(saveto, "a").write(domains+"\n\n")
    print(" [+] Scraped", len(domains.split("\n")), "domains")

def scrap(url:str):
    cookie = input(" [*] Enter cookie: ")

    while True:
        saveto = input(" [*] Enter save to file name: ")
        if os.path.isfile(saveto):
            print(" [+] File already exists")
            continue
        break

    # with ThreadPoolExecutor(max_workers=200) as pool:
    for i in range(10000):
        # pool.submit(parse, url+str(i), saveto, cookie)
        Thread(target=parse, args=(url+str(i), saveto, cookie)).start()
        time.sleep(0.4)
    
    print(" [+] Saved to", saveto)


def main():
    print(""" Menu: 
 [1] godaddy traffic domains
 [2] make offer domains
 [3] expired domains
 [0] Exit
 """)
    while True:
        choice = input(" [*] Enter your choice: ")
        if choice == "1":
            scrap("https://www.godaddy.com/domains/traffic-domains/")
        elif choice == "2":
            scrap("https://member.expireddomains.net/domains/sedomakeoffer/?start=")
        elif choice == "3":
            scrap("https://www.expireddomains.net/expired-domains/")
        elif choice == "0":
            break
        else:
            print(" [*] Invalid choice")
            continue
        break

    print(" [+] Bot finished")


if __name__ == "__main__":
    main()