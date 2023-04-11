#----------------------------------------------------------------------------------------------------
#### HV : THÁI THANH PHONG
#### SN : 14/03/1968
#### ĐỒ ÁN TỐT NGHIỆP : Project 1 Data Prepreocessing
#### MÔN HỌC : Data science
#----------------------------------------------------------------------------------------------------
import streamlit as st
# import random
# import pandas as pd
# import numpy as np
# from fuzzywuzzy import process
# import pickle
# from sklearn.metrics.pairwise import cosine_similarity
# from collections import defaultdict
# from surprise import Reader, Dataset
# from surprise.model_selection import train_test_split
# from utils import *

st.set_page_config(page_title="Recommendation app", page_icon="https://www.analyticsvidhya.com/wp-content/uploads/2016/03/ri1.png")
st.title('RECOMMENNDATION SYSTEM APP')

# Load data
# df_show_prod = df_show_prod()
# df_user = df_user()
#
# # Load model content base
# cosine_sim_matrix = load_tfidf()
# # Load model SVD CF
# SVD_model = load_SVD()

recommend_engine = st.sidebar.radio("Chọn loại recommend",('Content base', 'CF'))
if recommend_engine == "Content base":
    col1, col2 = st.columns((1, 4))
    select_other = col1.button("Lựa chọn ngẫu nhiên sản phẩm")
    text_input = col2.text_input("Nhập từ khoá tìm kiếm", value="")
    if select_other:
    # get prod image and title
        prod_rand_lst = [random.randint(0, df_show_prod.shape[0]) for i in range(12)] # show 12 random prod image + title
        filteredImages = df_show_prod.iloc[prod_rand_lst]["link_product_image_clean"].tolist()
        caption = df_show_prod.iloc[prod_rand_lst]["product_title"].tolist()
        st.image(filteredImages, width=150, caption=caption)

    else:
        choices = list(df_show_prod['product_title'])
        extracted = process.extract(text_input, choices, limit=12)
        extracted = [x[0] for x in extracted]
        # st.text(extracted)
        df_extracted = df_show_prod.loc[df_show_prod["product_title"].isin(extracted)]
        filteredImages = df_extracted["link_product_image_clean"].tolist()
        caption = df_extracted["product_title"].tolist()
        prod_rand_lst = df_extracted.index.values.tolist()
        st.image(filteredImages, width=150, caption=caption)

    # Show selected prod
    option = st.sidebar.selectbox('Select your product', caption)
    st.header("CÁC SẢN PHẨM LIÊN QUAN")
    choose_index = caption.index(option)    
    prod_index = prod_rand_lst[choose_index]

    # cal sim score
    df_return_cosin = cal_sim_score(cosine_sim_matrix, df_show_prod, prod_index)
    filteredImages_recom = df_return_cosin["link_product_image_clean"].tolist()
    caption_recom = df_return_cosin["product_title"].tolist()
    st.image(filteredImages_recom, width=150, caption=caption_recom)
    # st.dataframe(df_return_cosin)   

# recommend CF
else:
    df_user_unique = pd.Series(df_user["user_ID"].unique())
    user_rand_lst = [random.randint(0, df_user_unique.shape[0]) for i in range(30)] # show 10 rand user id
    user_random = df_user_unique.iloc[user_rand_lst].tolist()
    user_selected = st.sidebar.selectbox("Chọn user ID", options = user_random) # sample 2211818709 có 5 sp recom
    text_input = st.sidebar.text_input("Nhập User ID", value="")

    predictions = SVD_model.test(df_user[['user_ID', 'product_ID', 'review_star']].loc[df_user.user_ID == user_selected].values.tolist())
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:5]
    recomend_CF_prod_ID = [top_n[user_selected][i][0] for i in range(len(top_n[user_selected]))]
    recomend_CF_df = df_show_prod.loc[df_show_prod.product_ID.isin(recomend_CF_prod_ID)]
    filteredImages_CF = recomend_CF_df["link_product_image_clean"].tolist()
    caption_CF = recomend_CF_df["product_title"].tolist()
    st.text("CÓ THỂ BẠN CŨNG THÍCH")
    st.image(filteredImages_CF, width=150, caption=caption_CF)
    # st.dataframe(recomend_CF_df)
