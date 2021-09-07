import pandas as pd
import streamlit as st
import warnings
import tweepy
from datetime import timedelta
import requests
from multiapps import MultiApp
import key
from word import word_express


warnings.filterwarnings('ignore')
app = MultiApp()

# APIの認証
auth = tweepy.OAuthHandler(key.CK, key.CS)
auth.set_access_token(key.AK, key.AS)
api = tweepy.API(auth)


news_list = []
tag_list = []

Account_dict = {"TechCrunchJapan": "jptechcrunch",
                "Info_AI": "InfoAI4",
                "ITmedia Top": "topitmedia",
                "日経クロステックIT": "nikkeibpITpro",
                "人工知能・機械学習ニュース": "A_I_News",
                "ITmedia NEWS":"itmedia_news"
                }
account = list(Account_dict.keys())
newsapi_dic = {"最新ニュース": "headline",
               "キーワード": "keyword"
               }
newsapi_list = list(newsapi_dic.keys())


# 取得したいユーザーのユーザーIDを代入
def get_tweet():
    st.title("IT News")
    tweet_form = st.form(key="get-form")
    choice = tweet_form.selectbox("アカウント検索かキーワード検索か選んでください",["アカウント検索","キーワード検索"])
    select_account = tweet_form.selectbox("好きなアカウントを選んでください", account)
    keyword = tweet_form.text_input(label='検索したいキーワードを入力してください(アカウントは無視されます)')
    select_value = tweet_form.number_input(label="表示件数を選んでください", value=10)
    if select_value > 20:
        st.error('一度に表示できるのは最大20件です')
    appear = tweet_form.form_submit_button("表示")
    if appear:
        if choice=="アカウント検索":
            tweets = api.user_timeline(Account_dict[select_account], count=select_value, page=1)
            for tweet in tweets:
                news_list.append({
                    "time": tweet.created_at,
                    "title": tweet.text,
                    "retweet":tweet.retweet_count,
                    "favorite":tweet.favorite_count
                })
                news_sort_list = sorted(news_list, key=lambda x: x['time'], reverse=True)

            st.markdown(f'## {select_account}の最新ニュース')
            tech_df = pd.DataFrame(news_sort_list)
            for time, title,retweet,favorite in zip(tech_df["time"], tech_df["title"],tech_df["retweet"],tech_df["favorite"]):
                st.write("time:" + str(time + timedelta(hours=+9)))
                st.write("title:" + title)
                st.write("retweet_count:" + str(retweet))
                st.write("favorite_count:" + str(favorite))
                st.write("---")
        else:
            st.markdown(f'## {keyword}に関する最近の投稿')
            q = f"{keyword} -filter:retweets"
            tweets = api.search(
                q=q,
                count=select_value,
                tweet_mode="extended",
                locale="ja",
                lang="ja",
                include_entities=False,
            )
            tweets_df = pd.DataFrame(
                columns=[
                    "user_name",
                    "tweet_full_text",
                    "tweet_favorite_count",
                    "tweet_created_at",
                ]
            )
            for tweet in tweets:
                tweets_df = tweets_df.append(
                    {
                        "user_name": tweet.user.name,
                        "tweet_full_text": tweet.full_text,
                        "retweet": tweet.retweet_count,
                        "tweet_favorite_count": tweet.favorite_count,
                        "tweet_created_at": tweet.created_at + timedelta(hours=+9),
                    },
                    ignore_index=True,
                )
            for time, user_name, text,retweet ,favorite in zip(tweets_df["tweet_created_at"], tweets_df["user_name"],
                                                       tweets_df["tweet_full_text"],tweets_df["retweet"] ,tweets_df["tweet_favorite_count"]):
                st.write("time:" + str(time))
                st.write("user_name:" + user_name)
                st.write("text:" + text)
                st.write("retweet:" + str(retweet))
                st.write("favorite:" + str(favorite))
                st.write("---")





def news_search():
    st.title("ITニュース検索")
    news_form = st.form(key="news-form")
    head_every = news_form.selectbox("最新のニュースかキーワード検索を選択してください", newsapi_list)
    keyword = news_form.text_input(label="検索するキーワードを入力してください(キーワード検索の場合のみ)")
    select_value = news_form.number_input(label="表示件数を選んでください", value=50)
    news = news_form.form_submit_button("表示")
    if news:
        if newsapi_dic[head_every] == "headline":
            main_url = 'https://newsapi.org/v2/top-headlines?'
            query_params = {
                "category": "technology",
                "country": "jp",
                "apiKey": key.NW,
                "sort_by": 'publishedAt',
                "page_size": select_value
            }
        else:
            main_url = 'https://newsapi.org/v2/everything?'
            query_params = {
                "q": keyword,
                "apiKey": key.NW,
                "sort_by": 'publishedAt',
                "page_size": select_value
            }
        res = requests.get(main_url, params=query_params)
        it_news = res.json()
        it_news_articles = it_news["articles"]
        news_df = pd.DataFrame(columns=["title", "description", "url"])
        for article in it_news_articles:
            news_df = news_df.append(
                {
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"]
                },
                ignore_index=True,
            )
        for title, description, url in zip(news_df["title"], news_df["description"],
                                                   news_df["url"]):
            st.write("title:" + title)
            st.write("description:" + str(description))
            st.write("url:" + url)
            st.write("---")
app.add_app("ツイート表示", get_tweet)
app.add_app("ニュース表示", news_search)
app.add_app("頻出単語調査", word_express)

app.run()
