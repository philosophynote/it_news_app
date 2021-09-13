# it_news_app
- ITニュースを表示するサイトです。
- APIを活用してTwitterなどからITニュースを自動収集・表示してくれます。
- 自然言語処理を活用することでニュースのキーワードの数がわかります。
<img width="1635" alt="スクリーンショット 2021-09-13 14 39 36" src="https://user-images.githubusercontent.com/78991083/133029672-cb956571-10b1-432c-9c4b-a701fd2b630f.png">

# 使用技術
- Python 3.8.8(主な使用ライブラリ：streamlit,pandas,janome,plotly)
- Twitter API
- News API
- 自然言語処理

# 機能一覧
- 次のTwitterのアカウントのツイートを表示
  - TechCrunchJapan(@jptechcrunch)
  - Info_AI(@InfoAI4)
  - ITmedia Top(@topitmedia)
  - 日経クロステックIT(@nikkeibpITpro)
  - 人工知能・機械学習ニュース(@A_I_News)
  - ITmedia NEWS(@itmedia_news)
  - 検索機能
- News APIにより最新のITNewsを自動表示
  - 　検索機能
- 上記6つのアカウントで使用されている用語数を棒グラフで表示
