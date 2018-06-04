# SFSpider
#     - A spider using urllib and BeautifulSoup module to get all the tags from SegmentFault
# Author: LuRenJia https://untitled.pw/
# Time: 2018-06-04

# Import some necessary packages
from urllib import request
from bs4 import BeautifulSoup as soup
import ssl
import time
import os
import csv

# Define some variables
counter = 0
sleepTime = 3

# Avoid the error message caused by unauthorized ssl certificate
sslContext = ssl._create_unverified_context()


def scratchTag(page, fileName):
    global counter

    # Start scratching
    response = request.urlopen("https://segmentfault.com/tags/all?page=" + page, context=sslContext)
    html = response.read().decode("utf-8")

    # Initialize the BeautifulSoup package
    soupObj = soup(html, "html.parser")

    # Open a file
    with open("./" + fileName, "a+", encoding="utf-8") as f:
        for each in soupObj.select("div.widget-tag h2 a"):
            fieldnames = ["id", "zh-cn", "en-us"]
            eachRow = {"id": str(counter + 1), "zh-cn": each.get_text(), "en-us": each.get_text()}
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(eachRow)
            print("- Data No." + str(counter) + ":")
            for key, value in eachRow.items():
                print("\t" + key + " - " + value)
            counter += 1

    return counter


def portal():
    answer = {}
    result = 0

    print("\t\t\t\t\t\t\t\t****** SFSpider ******\n"
          + "\t- A spider using urllib and BeautifulSoup module to get all the tags from SegmentFault\n"
          + "\t\t\t\t\t\t- Author: LuRenJia https://untitled.pw/\n"
          + "\t\t\t\t\t\t\t\t- Time: 2018-06-04")

    time.sleep(1)

    answer["sleepTime"] = int(input("Please input the interval between each query (seconds): "))
    answer["pages"] = int(input("How many pages do you want to scratch: "))
    answer["fileName"] = str(input("Please input the specified filename you want to save (default is tags.csv): "))

    if answer["fileName"] == "":
        answer["fileName"] = "tags.csv"

    # If the file exists, clear it
    testFile = os.path.isfile(answer["fileName"])
    if testFile is True:
        fileObj = open(answer["fileName"], "w")
        fileObj.close()

    sleepTime = answer["sleepTime"]

    for i in range(int(answer["pages"])):
        print("\n\nStart the No." + str(i + 1) + " of " + answer["pages"] + " scratch......\n")
        time.sleep(sleepTime)
        result = scratchTag(str(i + 1), answer["fileName"])
        print("--------------------")
        print(str(result) + " tags get, sleep " + str(sleepTime) + " seconds\n")
        time.sleep(sleepTime)

    print("\n\n-----------Scratch Complete!-----------\n\n")
    print("Statistics: " + str(result) + "tags get, saved in ./" + answer["fileName"])


if __name__ == "__main__":
    portal()