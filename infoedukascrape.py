#---------------------------------------#
# Infoeduka Scraper CLI Variant         #
# By Luka Cafuka                        #
# Info can be found at z.com.hr         #
#---------------------------------------#
import argparse
from infoedukascrape_gui import *


def main():
    parser = argparse.ArgumentParser(
        prog='Infoeduka Scraper',
        description='Scrape study materials from Infoeduka',
    )

    parser.add_argument('-p', '--path', help='the path to where the files will be downloaded', required=True)
    parser.add_argument('-a', '--automatic-cookies', help=argparse.SUPPRESS, metavar='', type=bool, default=1, required=False)
    parser.add_argument('-s', '--show-cookie', help='print the cookie in the console when fetched', action='store_true', required=False)
    parser.add_argument('-c', '--cookie', help='manual cookie specification' , required=False)



    args = parser.parse_args()

    if args.cookie:
        args.automatic_cookies = False

    if args.show_cookie:
        args.show_cookie = True
    else:
        args.show_cookie = False

    q = queue.Queue()


    startScrape(q, args.path, args.automatic_cookies, args.cookie, args.show_cookie)


if __name__ == '__main__':
    main()