from Scraper import Scraper
from GenerateReport import GenerateReport

youtube = Scraper("https://www.youtube.com/watch?v=aJRbPG0aSHc")
commentsAndReplies = youtube.run()

GenerateReport(youtube.channelName, youtube.current_url,
               youtube.channelComments, commentsAndReplies)

