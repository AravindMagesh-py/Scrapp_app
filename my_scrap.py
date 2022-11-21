from bs4 import BeautifulSoup
from openpyxl import load_workbook
import requests
import pandas as pd
import os
import camelot

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import warnings

warnings.filterwarnings("ignore")

disable_warnings(InsecureRequestWarning)


class WebScrapper:
    """
    Web Scraping Class
    """

    def __init__(self, search_string):

        self.search_string = search_string
        self.pdf_name = None
        self.excel_file = os.path.join(os.getcwd(), "excel_files", f'{self.search_string}.xlsx')
        pd.DataFrame({"URL": [], "Title": [], "Text": []}).to_excel(self.excel_file, sheet_name="Info",
                                                                    index=False)  # To create the excel
        self.excel_writer = load_workbook(self.excel_file)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/103.0.0.0 Safari/537.36 "
        }
        self.error_log = None

    def save_to_excel(self, df):
        writer = pd.ExcelWriter(self.excel_file, engine='openpyxl', mode="a", if_sheet_exists='replace')
        try:
            writer.book = self.excel_writer
            df.to_excel(writer, sheet_name=self.pdf_name, index=False)
        except Exception as error:
            self.error_log = "Error in save_to_excel %s" % error
        finally:
            writer.save()
            writer.close()

    def save_to_pdf(self, link):
        """
        To save the pdf and extract tables
        :param link:
        :return:
        """
        try:
            self.pdf_name = link.split('/')[-1]
        except IndexError:
            self.pdf_name = "%s_%s" % (
                self.search_string, len([file for file in os.listdir() if file.startswith(self.search_string)]))
        try:
            with open(os.path.join(os.getcwd(), "pdf_files", self.pdf_name), "wb") as pdf_opener:
                pdf_opener.write(requests.get(link, headers=self.headers, verify=False).content)

            for table in camelot.read_pdf(os.path.join(os.getcwd(), "pdf_files", self.pdf_name)):
                self.save_to_excel(table.df)
        except Exception as error:
            self.error_log = "Error in save_to_pdf %s" % error

    def google_scrap(self):
        """
        Main scrap of Google
        :return:
        """
        params = {
            "q": self.search_string,
            "hl": "en",
            "start": 0,
            "filter": 0
        }
        page_num = 0

        try:
            df = pd.DataFrame({"URL": [], "Title": [], "Text": []})
            while True:
                page_num += 1
                print(f"{page_num} page:")

                html = requests.get("https://www.google.com/search", params=params, headers=self.headers, timeout=30)
                soup = BeautifulSoup(html.text, 'lxml')

                for result in soup.select(".tF2Cxc"):
                    title = result.select_one("h3").text
                    link = result.find("a")["href"]
                    try:
                        description = result.select_one(".VwiC3b").text
                    except AttributeError:
                        description = None
                    if link.endswith(".pdf"):
                        self.save_to_pdf(link)
                    df.loc[len(df.index)] = [link, title, description]
                    print("Title: %s\n Link -> %s\n Desc: %s" % (title, link, description), end="\n\n")
                if soup.select_one('.d6cvqb a[id=pnnext]'):
                    params["start"] += 10
                else:
                    self.save_to_excel(df)
                    break
            return self.excel_file
        except Exception as error:
            self.error_log = "Error in google_scrap %s" % error
        finally:
            print("Error check for %s : %s" % (
                self.search_string, self.error_log))  # As of now to check Error in Console
