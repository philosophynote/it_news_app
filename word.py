import tweepy
import re
import plotly.express as px
import pandas as pd
from janome.tokenizer import Tokenizer
from collections import Counter
import key
import streamlit as st


def word_count():
    auth = tweepy.OAuthHandler(key.CK, key.CS)
    auth.set_access_token(key.AK, key.AS)
    api = tweepy.API(auth)

    jptechcrunch=[]
    infoAI4=[]
    topitmedia=[]
    nikkeibpITpro=[]
    A_I_News=[]
    itmedia_news=[]
    account_dict={"jptechcrunch":jptechcrunch,
                  "InfoAI4":infoAI4,
                  "topitmedia":topitmedia,
                  "nikkeibpITpro":nikkeibpITpro,
                  "A_I_News":A_I_News,
                  "itmedia_news":itmedia_news
                 }
    for account in account_dict.keys():
        if account == "jptechcrunch":
            tweets = api.user_timeline(account, count=150, page=1)
            for tweet in tweets:
                clean_Tweet=re.match('(.*?)http.*?\s?(.*?)', tweet.text)
                if clean_Tweet==None:
                    pass
                else:
                    account_dict[account].append(clean_Tweet.group(1))
        elif account == "InfoAI4":
            tweets = api.user_timeline(account, count=150, page=1)
            for tweet in tweets:
                clean_Tweet=re.match('(.*?)http.*?\s?(.*?)', tweet.text)
                if clean_Tweet==None:
                    pass
                else:
                    split_text=clean_Tweet.group(1).split("-")[0]
                    account_dict[account].append(split_text)
        elif account == "topitmedia":
            tweets = api.user_timeline(account, count=150, page=1)
            for tweet in tweets:
                rep=tweet.text.replace("［https://t.co/GODG5vBTED］","")
                clean_Tweet=re.match('(.*?)http.*?\s?(.*?)', rep)
                if clean_Tweet==None:
                    pass
                else:
                    split_text = ''.join(clean_Tweet.group(1).split())
                    account_dict[account].append(split_text)
        elif account == "nikkeibpITpro":
            tweets = api.user_timeline(account, count=150, page=1)
            for tweet in tweets:
                account_dict[account].append(tweet.text.split("#")[0])
        elif account == "A_I_News":
            tweets = api.user_timeline(account, count=150, page=1)
            for tweet in tweets:
                account_dict[account].append(tweet.text.split("-")[0])
        else:
            tweets = api.user_timeline("itmedia_news", count=150, page=1)
            for tweet in tweets:
                if "RT" in tweet.text:
                    pass
                else:
                    split_text = ''.join(tweet.text.split())
                    clean_Tweet=re.match('(.*?)http.*?\s?(.*?)', split_text)
                    if clean_Tweet is None:
                        continue
                    account_dict[account].append(clean_Tweet.group(1))
    news_list = jptechcrunch + infoAI4 + topitmedia + nikkeibpITpro + A_I_News + itmedia_news
    return news_list

def news_express(news_list):
    news_df = pd.DataFrame(news_list, columns=["text"])
    news_df = news_df.drop_duplicates()
    texts = ''.join(news_df["text"])
    t = Tokenizer()
    tokens = t.tokenize(texts)
    word_list = []
    for token in tokens:
        word = token.surface
        partOfSpeech = token.part_of_speech.split(',')[0]
        partOfSpeech2 = token.part_of_speech.split(',')[1]

        if partOfSpeech == "名詞":
            if (partOfSpeech2 != "非自立") and (partOfSpeech2 != "代名詞") and (partOfSpeech2 != "数") and (
                    partOfSpeech2 != "接尾"):
                word_list.append(word)
    word_df = pd.DataFrame(columns=["word", "count"])
    stop_words = ["年", "化", "活用", "月", "性", "者",
                  "対応", "|", "人", "G", "開始", "開発",
                  "データ", "企業", "システム", "情報", "技術"
        , "提供", "サービス", "デジタル", "検索", "発売"
        , "無料", "予約", "公開", "AI", "発表", "コラム", "導入", "/", "スタート", "ニュース",
                  "最新", "プラン", "サイト", "連携", "学習",
                  "機械", "研究", "搭載",
                  "可能", "利用", "体験", "多様", "評価", "業界"
        , "未来", "成長", "重要", "IT", "調達", "分野",
                  "商品", "方法", "個人", "問題", "市場", "向上", "配信"
        , "公表", "採用", "投資", "世界", "調査", "委員", "人気"
        , "実験", "実証", "おすすめ", "オンライン", "結果", "理由",
                  "計算", "実現", "独自", "現状", "効果", "画面"
        , "開催", "推進", "運用", "講座", "課題", ".", "エンジニア"
        , "対策", "専用", "機能", "政府", "(", ")", "支援", "教育"
        , "コード", "ランキング", "大手", "影響", "ユーザー"
        , "映画", "リリース", "分析", "作成", " スイッチ", "育成"
        , "提携", "国立", "モデル", "社長", "通信", "販売"
        , "事業", "操作", "入門", "by", "規模", "実力", "国内"
        , "実績", "停止", "ツール", "原因", "設計", "狙い"
        , "前", "実力", "アプリ", "新型", ":", "～", "~"]
    new_word_list = [word for word in word_list if word not in stop_words]
    # words_wakati = " ".join(new_word_list)
    # wordcloud = WordCloud(
    #     font_path=path.join(getcwd(), ".fonts/Osaka.TTC"),
    #     # font_path='./.fonts/Osaka.TTC',
    #     width=900, height=600,  # default width=400, height=200
    #     background_color="white",  # default=”black”
    #     max_words=500,  # default=200
    #     min_font_size=4,  # default=4
    #     collocations=False  # default = True
    # ).generate(words_wakati)
    # image = wordcloud.to_image()
    # image.save(f"/tmp/wordcloud2.png", format="png", optimize=True)
    # image = Image.open("/tmp/wordcloud2.png")
    # st.image(image, caption='Word Cloud')
    counter = Counter(new_word_list)
    for word, count in counter.most_common():
        word_df = word_df.append({
            "word": word,
            "count": count
        }, ignore_index=True, )
    header=word_df.head(20).sort_values('count', ascending=True)
    st.write(px.bar(x=header["word"],y=header["count"]))


def word_express():
    st.title("頻出単語調査")
    st.text("こちらの画面では次の6つのアカウントの最新150ツイートを読み込み、")
    st.text("ツイートに含まれる単語のwordcloudと上位20単語の棒グラフを表示します。")
    st.text("◯ TechCrunch Japan")
    st.text("◯ Info_AI")
    st.text("◯ ITmedia Top")
    st.text("◯ 日経クロステックIT")
    st.text("◯ 人工知能・機械学習ニュース")
    st.text("◯ ITmedia NEWS")
    if st.button("データ読み込み"):
        array=word_count()
        news_express(array)