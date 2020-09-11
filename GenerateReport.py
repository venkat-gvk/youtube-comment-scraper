import json
from datetime import datetime


class GenerateReport:
    def __init__(self, channelName, current_url, channelComments,
                 commentsAndReplies):
        print('Generating Report...')
        self.current_url = current_url
        self.channelName = channelName
        self.channelComments = channelComments
        self.commentsAndReplies = commentsAndReplies
        date_time = GenerateReport.getDateAndTime()

        if not self.commentsAndReplies:
            self.commentsAndReplies = None

        report = {
            'date && time': date_time,
            'pinned or from channeluser': self.channelComments,
            'comments and replies': self.commentsAndReplies
        }

        file = open("report.json", 'w', encoding='utf-8')
        json.dump(report, file)
        file.close()
        print('Report Generated')
        print('Finished')

    @staticmethod
    def getDateAndTime():
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        return date_time
