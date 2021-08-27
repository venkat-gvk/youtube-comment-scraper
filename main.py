from Scraper import Scraper
from GenerateReport import GenerateReport
import sys

SEARCH_LINK = ''

def start():
    global SEARCH_LINK
    SEARCH_LINK = input('Enter youtube link: ').strip()

    if SEARCH_LINK.find('youtube') == -1:
        print("invalid youtube link")
        print('exiting...')

        sys.exit()


if __name__ == '__main__':
    start()
    youtube = Scraper(SEARCH_LINK)
    commentsAndReplies = youtube.run()
    
    GenerateReport(youtube.channelName, youtube.current_url,
               youtube.channelComments, commentsAndReplies)

