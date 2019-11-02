import praw
import pandas as pd
import datetime as dt
from datetime import date
from praw.models import MoreComments

'''
Configure for Reddit
'''

def run():
    # Reddit configuration
    reddit = praw.Reddit(client_id='JMcVbrWG15uP1g', \
                         client_secret='5XD3GKXJT3E-ZO0rUKoH1J8tKHQ', \
                         user_agent='IS434_Testing', \
                         username='nmmmym123456', \
                         password='pastword')

    # Search for subreddit Singapore
    subreddit = reddit.subreddit('singapore')

    # Set headers
    topics_dict = { "author": [],
                "title":[],
                "score":[],
                "id":[], "url":[],
                "comms_num": [],
                "created": [],
                "body":[]}
    
    # Get 1000 results
    for submission in subreddit.search('toilet', limit = 1000):
        topics_dict["author"].append(submission.author)
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)
    
    '''
    Python dictionaries, however, are not very easy for us humans to read.
    This is where the Pandas module comes in handy.
    We’ll finally use it to put the data into something that
    looks like a spreadsheet — in Pandas, we call those Data Frames.
    '''
    topics_data = pd.DataFrame(topics_dict)

    for index, row in topics_data.iterrows():
        if 'toilet' not in row['title']:
            topics_data.drop(index, inplace = True)
            
    '''
    Fixing the date column

    Reddit uses UNIX timestamps to format date and time. 
    Instead of manually converting all those entries, or using a site like 
    www.unixtimestamp.com, we can easily write up a function in Python to automate that process.

    We define it, call it, and join the new column to dataset with the following code:
    '''

    def get_date(created):
        return dt.datetime.fromtimestamp(created)

    _timestamp = topics_data["created"].apply(get_date)

    topics_data = topics_data.assign(timestamp = _timestamp)
    
    '''
    For each of the reddit post, extract the comments and the author

    '''

    def get_top_level_comment_body(uniqId):
        submission = reddit.submission(id=uniqId)
        submission.comments.replace_more(limit=None)
        comments = ""
        for comment in submission.comments.list():
            author = "\n=== Author: " + str(comment.author) + "===\n"
            comments += author + comment.body + "\n"
        return comments


    _bodyContent = topics_data["id"].apply(get_top_level_comment_body)
    _bodyContent = _bodyContent.replace(',', '')
    topics_data = topics_data.assign(top_main_comment = _bodyContent)

    #Export as CSV results

    today = date.today()
    d1 = today.strftime("%d_%m_%Y")
    filename = 'toilet_Reddit_output_test_' + d1 + '.csv'
    topics_data.to_csv(filename, index=False) 


run()