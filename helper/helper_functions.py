from textblob import TextBlob
from collections import Counter
import praw
import datetime as dt
from pytrends.request import TrendReq
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download("punkt")
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

reddit = praw.Reddit(
    client_id="DySfO6Rh7G5ZSr2gufGHiA",
    client_secret="x6-dYCAad6hGS2L34LKYHaT77_5vxQ",
    user_agent="MyAPI/0.0.1",
    username="FabStyle7",
    password="pallav99sharma",
)


def market_sentiment_helper(keywords_list):
    posts = []
    for term in keywords_list:
        # Search for posts containing the search term
        # extracting two posts for each of the keyword
        search_results = reddit.subreddit('all').search(term, sort='relevance', limit=4, time_filter="year")

        for post in search_results:
            # Create a dictionary with relevant post information
            post_data = {
                'title': post.title,#blocked
                'description': post.selftext,
                'date_posted': dt.datetime.fromtimestamp(post.created_utc).strftime(
                    '%Y-%m-%d %H:%M:%S')
            }
            posts.append(post_data)

    # Initialize sentiment counters
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    mixed_count = 0

    # Analyze sentiment for each array element
    for post in posts:
        combined_text = post["title"] + " " + post["description"]
        sentiment = TextBlob(combined_text).sentiment.polarity

        # Categorize sentiment
        if sentiment > 0.1:
            positive_count += 1
        elif sentiment < -0.1:
            negative_count += 1
        elif sentiment == 0:
            neutral_count += 1
        else:
            mixed_count += 1

    # Calculate percentages
    total_posts = len(posts)
    positive_percentage = (positive_count / total_posts) * 100
    negative_percentage = (negative_count / total_posts) * 100
    neutral_percentage = (neutral_count / total_posts) * 100
    mixed_percentage = (mixed_count / total_posts) * 100

    # Print percentages in numbered line format
    # print("1. Positive: {:.2f}%".format(positive_percentage))
    # print("2. Negative: {:.2f}%".format(negative_percentage))
    # print("3. Neutral: {:.2f}%".format(neutral_percentage))
    # print("4. Mixed: {:.2f}%".format(mixed_percentage))
    return {'positive': positive_percentage, 'negative': negative_percentage, 'neutral': neutral_percentage,
            'mixed': mixed_percentage}


def market_sentiment(keywords_list):
  ans=market_sentiment_helper(keywords_list)
  return ans


def important_conversations_helper(keywords_list):
    posts = []
    for term in keywords_list:
        # Search for posts containing the search term
        # extracting two posts for each of the keyword
        search_results = reddit.subreddit('all').search(term, sort='relevance', limit=2, time_filter="year")

        for post in search_results:
            # Create a dictionary with relevant post information
            post_data = {
                'title': post.title,
                'description': post.selftext,
                'date_posted': dt.datetime.fromtimestamp(post.created_utc).strftime(
                    '%Y-%m-%d %H:%M:%S')
            }
            posts.append(post_data)
    return {'posts': posts}



def important_conversations(keywords_list):
  return important_conversations_helper(keywords_list)



def latest_conversations_helper(keywords_list):
    posts = []
    for term in keywords_list:
        # Search for posts containing the search term
        # extracting two posts for each of the keyword
        search_results = reddit.subreddit('all').search(term, sort='new', limit=2, time_filter="year")

        for post in search_results:
            # Create a dictionary with relevant post information
            post_data = {
                'title': post.title,
                'description': post.selftext,
                'date_posted': dt.datetime.fromtimestamp(post.created_utc).strftime(
                    '%Y-%m-%d %H:%M:%S')
            }
            posts.append(post_data)
    return {'posts': posts}



def latest_conversations(keywords_list):
  return latest_conversations_helper(keywords_list)


def calculate_keyword_correlations(correlation_matrix, target_keyword):
    correlations = {}

    target_column = correlation_matrix[target_keyword]
    for keyword, correlation in target_column.items():
        if keyword != target_keyword:
            correlations[keyword] = int(correlation)

    return correlations

def analyze_interrelatedness(search_terms, timeframe):
    # Set up pytrends client
    pytrends = TrendReq(hl='en-US', tz=360)

    # Initialize an empty DataFrame to store the results
    combined_df = None

    # Iterate through each keyword and retrieve interest over time data
    for keyword in search_terms:
        pytrends.build_payload(kw_list=[keyword], timeframe=timeframe)
        interest_over_time_df = pytrends.interest_over_time()

        # Remove the 'isPartial' column
        interest_over_time_df.drop(columns=['isPartial'], inplace=True)

        # Combine the dataframes for each keyword
        if combined_df is None:
            combined_df = interest_over_time_df
        else:
            combined_df = pd.concat([combined_df, interest_over_time_df], axis=1)

    # Calculate correlation matrix
    correlation_matrix = combined_df.corr()

    # Multiply correlation matrix entries by 100
    correlation_matrix *= 100
    # Display correlation matrix
    print("Correlation Matrix:")
    print(correlation_matrix)
    return correlation_matrix


def correlated_keywords_helper(keywords):
    # Initialize a Counter for global word frequencies
    global_word_count = Counter()

    # Process and analyze posts for each keyword
    for keyword in keywords:
        search_results = reddit.subreddit("all").search(keyword, sort='hot', limit=10,
                                                        time_filter="year")  # Adjust the limit as needed

        for post in search_results:
            words = nltk.word_tokenize(post.title.lower() + " " + post.selftext.lower())
            words = [word for word in words if word.isalnum() and word not in stop_words]
            global_word_count.update(words)

    # Sort words by frequency in descending order
    sorted_words = sorted(global_word_count.items(), key=lambda x: x[1], reverse=True)

    print(sorted_words)
    # Print the sorted word frequencies
    top_nine_keywords = []
    for i in range(0, 9):
        top_nine_keywords.append(sorted_words[i][0])

    print(top_nine_keywords)
    search_terms = top_nine_keywords
    timeframe = 'today 12-m'

    correlation_matrix = analyze_interrelatedness(search_terms, timeframe)
    result = calculate_keyword_correlations(correlation_matrix, top_nine_keywords[0])

    ans = []
    for key, value in result.items():
        ans.append({'keyword': key, 'correlation_score': value})

    return {'posts': ans}


def correlated_keywords(keywords):
  return correlated_keywords_helper(keywords)
