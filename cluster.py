import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def clustering():
    st.title("ツイッターの単語をベクトル表示する")
    uploaded_file = st.file_uploader("csvファイルをアップロードしてください")

    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.dataframe(dataframe)
        cluster_form = st.form(key="cluster-form")
        cluster = cluster_form.selectbox("表示するクラスターを選んでください",[0,1,2,3,4,5,6,7,8,9])
        appear = cluster_form.form_submit_button("表示")
        if appear:
            cl_df=dataframe[dataframe["cluster"]==cluster]
            fig = go.Figure(data=[go.Table(header=dict(values=["word","cluster"],fill_color='paleturquoise',align='left'),
                             cells=dict(values=[cl_df.word, cl_df.cluster],
                            fill_color='lavender',align='left'))])
            st.plotly_chart(fig)
        fig = px.scatter_3d(dataframe,x="0",y="1",z="2",text="word",color='cluster')
        st.plotly_chart(fig)