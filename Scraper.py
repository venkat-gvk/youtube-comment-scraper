from selenium import webdriver
from sys import exit
import time


def init():
    options = webdriver.ChromeOptions()
    return webdriver.Chrome("./chromedriver", options=options)


class Scraper:
    def __init__(self, url):
        self.url = url
        self.driver = init()

    # Get info about the comment count and is turned off or not

    def getCommentInfo(self):
        print('Looking for comments')
        self.driver.execute_script("window.scrollTo(0, 570)")
        time.sleep(2)

        isComment = self.driver.find_element_by_xpath(
            "//ytd-comments/ytd-item-section-renderer/div[1]")

        if isComment.text:
            commentInfo = self.driver.find_element_by_xpath(
                '//*[@id="count"]/yt-formatted-string').text.split()

            if commentInfo[0] == "0":
                print("No comments available for this video. count: 0")
                self.quit()
                exit()

            return commentInfo

        else:
            print("Comments are turned off for this video")
            self.quit()
            exit()

    def loadNestedReplies(self, el, reply):
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);arguments[0].click()", reply)
        time.sleep(0.8)

        cont = el.find_element_by_xpath('//*[@id="continuation"]').text
        if cont:
            reply = el.find_element_by_xpath(
                '//*[@id="continuation"]/yt-next-continuation/paper-button')
            self.loadNestedReplies(el, idx, el, reply)

    # get nested replies

    def getNestedReplies(self, headings, replies):
        result = []
        for (heading, reply) in zip(headings, replies):
            reply = self.driver.execute_script(
                "return arguments[0].textContent", reply).strip()

            if not reply:
                reply = False
            if not heading.text:
                result.append((self.channelName.upper(), reply))
            else:
                result.append(('Shikai', reply))

        return result

    def extractReplies(self, container):
        print('Extracting replies...')
        all = []
        for i, el in enumerate(container):
            reply = el.find_element_by_xpath(
                f'//ytd-comment-thread-renderer[{i + 1}]/div').text

            if reply and reply.find(self.channelName) != -1:
                reply = el.find_element_by_xpath(
                    f'//ytd-comment-thread-renderer[{i + 1}]/div//div[1]/ytd-button-renderer[1]/a/paper-button'
                )
                comment = self.getIndividualComment(i + 1, el)

                self.loadNestedReplies(el, reply)

                headings = el.find_elements_by_xpath(
                    f'//ytd-comment-thread-renderer[{i + 1}]//div/ytd-comment-renderer//div[1]/div[2]/a'
                )
                replies = el.find_elements_by_xpath(
                    f'//ytd-comment-thread-renderer[{i + 1}]//div/ytd-comment-renderer//ytd-expander/div'
                )
                result = self.getNestedReplies(headings, replies)
                all.append({
                    'ch.name': 'Bankai',
                    'comment': comment,
                    'replies': result
                })

        return all

    # get every comment that has replies on top level

    def getIndividualComment(self, idx, el):
        result = el.find_element_by_xpath(
            f'//ytd-comment-thread-renderer[{idx}]/ytd-comment-renderer/div[1]/div[2]/ytd-expander/div'
        )
        result = self.driver.execute_script("return arguments[0].textContent",
                                            result)

        return result.strip()

    # get top level comment from Channel

    def getPinnedComments(self, container):
        print(
            f'Looking for any pinned comment or comment without any reply from {self.channelName}'
        )

        self.channelComments = []

        for i, el in enumerate(container):
            ch = el.find_element_by_xpath(
                f'//ytd-comment-thread-renderer[{i + 1}]/ytd-comment-renderer/div[1]/div[2]/div[1]/div[2]/a'
            ).text

            if not ch:
                reply = el.find_element_by_xpath(
                    f'//ytd-comment-thread-renderer[{i + 1}]/div').text
                if not reply or reply.find(self.channelName) == -1:
                    comment = self.getIndividualComment(i + 1, el)
                    self.channelComments.append((self.channelName, comment))

        if not self.channelComments:
            print(
                f'No pinned comment or any top level comment from {self.channelName}'
            )
            self.channelComments = None

    # load the page till end and get all links for the comment

    def getLinks(self, commentLength):
        count = 0
        end = int(commentLength)
        step = 1000

        for i in range(0, end):
            self.driver.execute_script(f"window.scrollTo(0, {step})")
            step = step + 500
            self.driver.find_elements_by_css_selector(
                'ytd-comment-thread-renderer.ytd-item-section-renderer')

        container = self.driver.find_elements_by_css_selector(
            'ytd-comment-thread-renderer.ytd-item-section-renderer')

        self.getPinnedComments(container)
        return self.extractReplies(container)

    # Initialize Scrape...

    def run(self):
        print("Starting...")
        self.driver.get(self.url)
        self.driver.implicitly_wait(15)

        video_title = self.driver.find_element_by_xpath(
            '//*[@id="container"]/h1/yt-formatted-string')
        time.sleep(1.5)

        if not video_title:
            print("title not found")
            self.quit()
            return

        self.video_title = video_title.text

        self.current_url = self.driver.current_url
        commentInfo = self.getCommentInfo()

        print('Getting channel name')
        self.channelName = self.driver.find_element_by_xpath(
            '//*[@id="text"]/a').text

        all = self.getLinks(commentInfo[0])

        print('Done')
        self.quit()

        return all

    # Quit Scraping and close the browser

    def quit(self):
        print("Stopping...")
        self.driver.quit()
