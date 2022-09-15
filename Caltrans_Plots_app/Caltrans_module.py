# imports
import bs4
import urllib
from bs4 import BeautifulSoup
from urllib.request import urlopen
import lxml
import re
import string
from csv import writer

# reading html and collecting data from the California government procurement page
url = "https://dot.ca.gov/programs/procurement-and-contracts/contracts-out-for-bid"

page = urlopen(url)

htmltext = page.read().decode("utf-8")

soup = BeautifulSoup(htmltext, "html.parser")

# Webscraper module class definition
class Caltrans_scraper:
    
    # method to return one string, one dict, one string and one list for header display informations
    def headers_lists(self):
        
        title_info = soup.title.string

        meta = soup.find_all("meta", attrs={"content":"State of California"})
        meta_name = meta[0]["content"]
        meta_name_author = meta[1]["name"]
        meta_name_description = meta[2]["name"]

        meta_owner = soup.find("meta", attrs={"name":"Keywords"})
        site_owner_name = meta_owner["content"]

        logo = soup.find("div", attrs={"class":"header-cagov-logo"})
        logo_text = logo.get_text()
        logo_link = logo.contents[0]["href"]
        
        page_info_dict = {"logo_text": logo_text,
        "logo_link": logo_link,
        meta_name_description: meta_name,
        meta_name_author: meta_name,
        "site_owner_name": site_owner_name}

        somepara = soup.select("p")
        somepara[1].contents[1]["href"]

        paratext = ""
        for x in somepara:
            paratext = paratext + x.get_text() + "\n"

        newparatext = re.sub("visit", "visit "+ somepara[1].contents[1]["href"], paratext)

        heading = soup.find_all("ol")
        heading_list = [c.get_text() for c in heading[0].contents[1:3]]

        return title_info, page_info_dict, newparatext, heading_list
    
    # method to return 4 lists, one dict and one string on campaign programs and footer display social media links and copyright info
    def programsInfo_and_footer(self):

        text = soup.find_all("li")
        textlist = [x.contents[0] for x in text]

        list1 = [tag["href"] for tag in textlist[10:]]
        campaigns_programs_links = list1[:19]

        support_cal_gov = [[x] for x in list1[23:]]

        list2 = [tag.get_text() for tag in textlist[10:]]
        campaign_programs = list2[:19]

        support_link_text = list2[23:]

        support_links_dict = dict(zip(support_link_text, support_cal_gov))

        scale = [(soup.h2).get_text() for x in range(20)]

        sno = [x for x in range(1,20)]

        mylist = (soup.get_text("\n", strip = True)).split("\n")
        copyright_statement = mylist[117]

        return sno, campaign_programs, campaigns_programs_links, scale, support_links_dict, copyright_statement
    
    # method to return 6 lists on contracts events information
    def contracts_info(self):

        eventtext = soup.find_all("td")
        eventlist = [x.get_text().strip() for x in eventtext]

        i=0
        eventids = []
        while i < len(eventlist):
            eventids.append(eventlist[i])
            i+=3

        j=1
        eventnames = []
        while j < len(eventlist):
            eventnames.append(eventlist[j])
            j+=3

        k=2
        eventdates = []
        eventtimes = []
        while k < len(eventlist):
            eventdates.append((eventlist[k].split("-"))[0])
            eventtimes.append((eventlist[k].split("-"))[1])
            k+=3

        eventdates = [date.rstrip() for date in eventdates]

        eventtimes = [time.lstrip() for time in eventtimes]

        mylinks = soup.find_all("a")
        myhrefs = [tag["href"] for tag in mylinks]
        eventlinks = myhrefs[16:32]
        index = [x for x in range(1,16)]

        return index, eventids, eventnames, eventdates, eventtimes, eventlinks

# defining campaign_csv() functions to create Campaign_Programs.csv 
def campaign_csv(sno, campaign_programs, campaigns_programs_links, scale):
    with open("Campaign_Programs.csv", "w", encoding="utf-8", newline="") as file:
        thewriter = writer(file)
        header = ["SNo.", "Campaign Program", "Campaign Program link", "Scale"]
        thewriter.writerow(header)
        for item in zip(sno, campaign_programs, campaigns_programs_links, scale):
            thewriter.writerow(item)

# defining contracts_csv() functions to create Caltrans_Contracts_Events.csv
def contracts_csv(index, eventids, eventnames, eventdates, eventtimes, eventlinks):
    with open("Caltrans_Contracts_Events.csv", "w", encoding="utf-8", newline="") as file:
        thewriter = writer(file)
        header = ["#", "Event Ids", "Event Names", "Event Dates", "Event Times", "Event Links"]
        thewriter.writerow(header)
        for item in zip(index, eventids, eventnames, eventdates, eventtimes, eventlinks):
            thewriter.writerow(item)

# calling class Caltrans_scraper() and storing lists and strings in variables needed in other applications
scraper = Caltrans_scraper()
title_info, page_info_dict, newparatext, heading_list = scraper.headers_lists()
sno, campaign_programs, campaigns_programs_links, scale, support_links_dict, copyright_statement = scraper.programsInfo_and_footer()
index, eventids, eventnames, eventdates, eventtimes, eventlinks = scraper.contracts_info()

#----End of Caltrans_module.py file----------------------------------------------------------------
# Coder: Swati Mishra
