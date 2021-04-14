# encoding=utf-8


import streamlit as st

from kg_demo_movie.KB_query.query_main import QAInterface


@st.cache(allow_output_mutation=True)
def get_interface():
    interface = QAInterface()
    return interface


qa_interface = get_interface()

ans_list2 = qa_interface.answer('所有演员周星驰').split('、')
ans_list3 = qa_interface.answer('所有电影功夫').split('、')
home_btn = st.sidebar.button('问答KBQA')
actor_btn = st.sidebar.button('演员')
movie_btn = st.sidebar.button('电影')
actor_inp = st.sidebar.text_input('演员', key='I1')
movie_inp = st.sidebar.text_input('电影', key='I2')
index = 3
if movie_inp:
    index = 2
if actor_inp:
    index = 1
if movie_inp and actor_inp:
    index = 3
if actor_btn or index == 1:
    for actor in ans_list2:
        st.button(actor)
        bio = qa_interface.answer(actor + '简介')
        if bio == '':
            bio = '暂无详细信息'
        st.info(bio)
    # st.selectbox('所有演员', options=ans_list2)
    index = 1
if movie_btn or index == 2:
    for movie in ans_list3[0:500]:
        st.write(movie)
        bio = qa_interface.answer(movie + '简介')
        if bio == '':
            bio = '暂无详细信息'
        st.info(bio)
    index = 2

if home_btn or index == 3:
    st.title("电影KBQA Demo")
    st.text_area('Demo支持的问题类型', """1. 某演员演了什么电影
    2. 某电影有哪些演员出演
    3. 演员A和演员B合作出演了哪些电影
    4. 某演员参演的评分大于X的电影有哪些
    5. 某演员出演过哪些类型的电影
    6. 某演员出演的XX类型电影有哪些。
    7. 某演员出演了多少部电影。
    8. 某演员是喜剧演员吗。
    9. 某演员的生日/出生地/英文名/简介
    10. 某电影的简介/上映日期/评分""", height=270)

    question = st.text_input("请输入你的问题：", key='Q1')
    if question != "":
        # st.text(qa_interface.answer(question))
        ans_list = qa_interface.answer(question).split('、')
        name_en = qa_interface.answer(ans_list[0] + '英文名')
        if name_en == '暂无...':
            for ans in ans_list:
                st.info(ans)
                bio2 = qa_interface.answer(ans + '上映日期').split('、')[0]
                if bio2 == '':
                    bio2 = '暂无详细信息...'
                st.write('上映日期:   ' + bio2)
                # '上映日期: ', bio2.split('、')[0]

                bio3 = qa_interface.answer(ans + '评分')
                if bio3 == '':
                    bio3 = '暂无详细信息...'
                # st.write('评分:' + bio3)
                '评  分: ', bio3.split('、')[0]

                bio4 = qa_interface.answer(ans + '演员')
                if bio4 == '':
                    bio4 = '暂无详细信息...'
                # st.write('主演:   ' + bio4)
                '主  演: ', bio4

                bio1 = qa_interface.answer(ans + '简介')
                if bio1 == '':
                    bio1 = '暂无详细信息...'
                # st.write(' 简介:\n' + bio1[0:100] + '...')
                '简  介: ', bio1[0:100].replace('　　', '') + '...'
        if name_en != '暂无...':
            for ans in ans_list:
                st.info(ans)
                name_en = qa_interface.answer(ans + '英文名')
                if name_en == '':
                    name_en = '暂无详细信息...'
                '英文名: ', name_en
                bio2 = qa_interface.answer(ans + '生日')
                if bio2 == '':
                    bio2 = '暂无详细信息...'
                st.write('生  日:   ' + bio2)

                bio2 = qa_interface.answer(ans + '出生地')
                if bio2 == '':
                    bio2 = '暂无详细信息...'
                '出生地: ', bio2
                bio2 = qa_interface.answer(ans + '简介')
                if bio2 == '':
                    bio2 = '暂无详细信息...'
                '简  介: ', bio2[0:100] + '...'
        index = 3
