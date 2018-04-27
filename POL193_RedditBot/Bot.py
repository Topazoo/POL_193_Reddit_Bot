#!/usr/bin/python

""" Author: Peter Swanson
            pswanson@ucdavis.edu

    Description: A class to contain, organize, and analyze Reddit data

    Version: Python 2.7
    Requirements: Spreadsheet.py, Reddit.py and openpyxl """

import praw

from Reddit import Subreddit, Post
from Spreadsheet import Spreadsheet

class Bot(object):
    """ Class to contain highest-order program operations """

    def __init__(self):
        # Open spreadsheets for inputs and results
        self.input_sheet = Spreadsheet("input/subreddits.xlsx")
        self.output_sheet = Spreadsheet("output/results.xlsx", False)

        self.reddit = praw.Reddit('193bot')

        # Create a list of subreddits
        self.subreddits = []

    def get_subreddits(self):
        """ Get info from the spreadsheet """

        # Get subreddit names
        subreddits_column = self.input_sheet.read_column(1)

        # Get subreddit ideologies
        ideology_column = self.input_sheet.read_column(1)

        # Zip and store combined information
        subreddits = zip(subreddits_column.values()[0], ideology_column.values()[0])

        for subreddit in subreddits:
            subreddit_obj = Subreddit(subreddit[0], subreddit[1])
            subreddit_obj.feed = self.reddit.subreddit(subreddit[0][2:])
            subreddit_obj.users = subreddit_obj.feed.subscribers
            self.subreddits.append(subreddit_obj)

    def get_posts(self, limit=30, range='year'):
        """ Get a number (limit) of top posts ranging back a range.
            @Params:
             limit - number of posts to collect
             range - range of time to get posts from """

        # For all subreddits, collect valid posts
        for subreddit in self.subreddits:
            for post in subreddit.feed.top(range, limit=limit):
                post_object = Post(post)
                if post_object.title and post_object.poster:
                    subreddit.top_posts.append(post_object)

    def create_output(self):
        """ Create the output file """

        # Create sheets
        init_sheet = self.output_sheet.file['Sheet']
        init_sheet.title = 'Subreddits'
        self.output_sheet.create_sheets([repr(x)[2:] for x in self.subreddits])

        # Create legends
        self.output_sheet.write_column(1, [repr(x) for x in self.subreddits], start_row=2, italics=True)
        self.output_sheet.write_row(1, [str(x) for x in self.subreddits[0].__dict__.keys() if x != "feed" and x != "top_posts"],
                                       start_col=2, bold=True)
        for sheet in self.output_sheet.file.worksheets:
            if str(sheet.title) != "Subreddits":
                self.output_sheet.sheet = sheet
                self.output_sheet.write_row(1,[str(x).title() for x in self.subreddits[0].top_posts[0].__dict__.keys() if x != "post"],
                                            start_col=1, bold=True)

    def get_users(self):
        # Most active now
        ## Last 100 posts and the users posting in the comments
        # Most active a year ago
        # Moderators
        test = "test"