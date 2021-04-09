import requests
import json
from bs4 import BeautifulSoup




class ZAUBACORP:
    def __init__(self, url):
        self.url = url
        self.products = []
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.90 Safari/537.36',
        }

    def getPageParser(self, url):
        page = requests.get(url, headers=self.headers)
        return BeautifulSoup(page.text, "html5lib")

    def scrape(self):
        page = self.getPageParser(self.url)
        company_details = page.findAll("div", {"class": "col-lg-12 col-md-12 col-sm-12 col-xs-12"})
        directors_details = []
        for company_detail in company_details:
            h4 = company_detail.find("h4", {"class": "company-data"})
            if str(h4.get_text()).strip() == "Director Details":
                directors = company_detail.findAll('tr', {"class": "accordion-toggle main-row"})
                other_directorships = company_detail.findAll('td', {"class": "hiddenRow"})
                for index, director in enumerate(directors):
                    details = director.findAll('td')
                    other_directorship_details = other_directorships[index]
                    other_directorship_details = other_directorship_details.findAll("tbody")[0]
                    other_details = []
                    for row in other_directorship_details.findAll('tr'):
                        data = row.findAll('td')
                        other_details.append({
                            'CompanyName': data[0].find('a').get_text(),
                            'CompanyDetailsLink': data[0].find('a',  href=True)['href'],
                            'Designation': data[1].find('p').get_text(),
                            'AppointmentDate': data[2].find('p').get_text(),
                        })
                    d_details = {
                        'DIN': details[0].find('p').get_text(),
                        'DirectorName': details[1].find('a').get_text(),
                        'DirectorDetailsLink': details[1].find('a',  href=True)['href'],
                        'Designation': details[2].find('p').get_text(),
                        'AppointmentDate': details[3].find('p').get_text(),
                        'OtherDirectorships': other_details
                    }
                    directors_details.append(d_details)
                break
        return directors_details


if __name__ == '__main__':
    url = "https://www.zaubacorp.com/company/SAAKSHEE-VANIJYA-LLP/AAO-5868"
    zau = ZAUBACORP(url)
    print(zau.scrape())
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps(zau.scrape(), indent=3)
    # }
