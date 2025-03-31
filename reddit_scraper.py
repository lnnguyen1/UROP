#py -m pip install praw
import praw
# py -m pip install openai
from openai import OpenAI
#import os

client = OpenAI(
    api_key="my_key"
    # api_key=os.environ.get("OPENAI_API_KEY")
)

# authenticate with the Reddit API
reddit = praw.Reddit(
    client_id="L60RZl-KqUZ7ZWYoVKEHFA",
    client_secret="TA1gdFkJsf5ft7s-ZFBhsYfY3mvvUw",
    user_agent="RedditScraper:v1.0 (by/u/lnguyenn)"
)

# test connection, prints current username based on the client ids
print("Authenticaed as: ", reddit.user.me())

#input the subreddit name, no limit, I want to process all the posts in the subreddit and scrape based on keywords
def scrapePosts(subredditName):
    subreddit = reddit.subreddit(subredditName)
    #make empty list to hold valid subreddit posts
    allPosts = []
    for currPost in subreddit.hot(limit=None):
        allPosts.append(currPost.title + " " + currPost.selftext)
    #f-string to allow embedded expressions
    #len(allPosts) returns the length of the list of postsin the subreddit
    print(f"Scraped {len(allPosts)} posts.")
    return allPosts

#filter posts
def filter_posts(posts, keywords, matchesLimit = 100):
    filtered = []
    for post in posts:
        if any(keyword.lower() in post.lower() for keyword in keywords):
            filtered.append(post)
        if len(filtered) >= matchesLimit:
            break
    print(f"Filtered {len(filtered)} posts with keywords.")
    return filtered

def chatGBTSentiment(text):
    try:
        response = client.responses.create(
            model="gpt-4o",  # Adjust the model version if required
            instructions="You are a sentiment analysis tool.",
            input=f"Analyze the sentiment of the following response and identify the sentiment as Positive, Negative, or Neutral: {text}"
        )
        return response.output_text  # Return the generated text
    except Exception as e:
        print(f"Error with sentiment analysis: {e}")
        return None

def main():
    subredditName = "callcentres"
    keywords = ["emergency"]
    posts = scrapePosts(subredditName)
    #print(f"Fetched {len(posts)} posts.")
    filteredPosts = filter_posts(posts, keywords, matchesLimit=100)
    #print(f"Fetched {len(posts)} posts.")
    if not filteredPosts:
        print("No posts matched the filter criteria.\n")
        return
    # Perform sentiment analysis and display results
    print("Performing sentiment analysis on valid posts: \n")
    for post in filteredPosts:
        sentiment = chatGBTSentiment(post)
        if sentiment:
            print(f"Post: {post}\nSentiment: {sentiment}\n")
        else:
            print(f"Error analyzing sentiment.")

#call main function
if __name__ == "__main__":
    main()
