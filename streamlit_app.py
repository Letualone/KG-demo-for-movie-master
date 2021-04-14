# encoding=utf-8


import streamlit as st

from kg_demo_movie.KB_query.query_main import QAInterface


@st.cache(allow_output_mutation=True)
def get_interface():
    interface = QAInterface()
    return interface


def title():
    st.title("电影KBQA ")
    st.text_area('支持的问题类型', """    1. 某演员演了什么电影
    2. 某电影有哪些演员出演
    3. 演员A和演员B合作出演了哪些电影
    4. 某演员参演的评分大于X的电影有哪些
    5. 某演员出演过哪些类型的电影
    6. 某演员出演的XX类型电影有哪些。
    7. 某演员出演了多少部电影。
    8. 某演员是喜剧演员吗。
    9. 某演员的生日/出生地/英文名/简介
    10. 某电影的简介/上映日期/评分
    Q1. 演员XX出演的电影
    Q2. 演员XX评分前10的电影(电影评分排行)
    Q3. 演员XXX出演过哪些类型的电影
    Q4. 电影有哪些类型
    Q5. 电影排行榜
    Q6. 最新上映的电影""", height=420)


# 1. 演员周星驰出演的电影
def actor_movie(movies):
    # movies = qa_interface.answer(question).split('、')
    for m in movies:
        # st.info('片名：《' + m + '》')
        st.success('片名：《' + m + '》')
        bio2 = qa_interface.answer(m + '上映日期').split('、')[0]
        if bio2.__len__() < 10:
            bio2 = '😕暂无详细信息...'
        st.write('上映日期:   ' + bio2)
        # '上映日期: ', bio2.split('、')[0]

        bio3 = qa_interface.answer(m + '评分')
        if bio3.__len__() < 1:
            bio3 = '😕暂无详细信息...'
        # st.write('评分:' + bio3)
        '评  分: ', bio3.split('、')[0][0:3]

        bio4 = qa_interface.answer(m + '演员')
        if bio4 == '':
            bio4 = '😕暂无详细信息...'
        # st.write('主演:   ' + bio4)
        '主  演: ', bio4[0:20] + '...'

        bio1 = qa_interface.answer(m + '简介')
        if bio1 == '':
            bio1 = '😕暂无详细信息...'
        # st.write(' 简介:\n' + bio1[0:100] + '...')
        '简  介: ', bio1[0:100].replace('　　', '') + '...'


# 2. 演员周星驰评分前10的电影(电影评分排行)
def rank_movie(movies):
    rank_dic = {}
    for m in movies:
        rank = qa_interface.answer(m + '评分')[0:3]
        if rank == '不知道':
            rank = '0'
        if float(rank) > 5:
            rank_dic.setdefault(m, rank)
        # st.info(rank + ans)
    rank_dic = dict(sorted(rank_dic.items(), key=lambda x: x[1], reverse=True))
    num = 0
    for k in rank_dic:
        bio = qa_interface.answer(k + '简介')[0:100]
        if bio.__len__() > 10:
            num += 1
            if num <= 10:
                st.info('No.' + str(num) + '  《' + k + '》 -----评分： ' + rank_dic[k])
                st.write('简介： ' + bio + '...')


# 最新上映的电影
def data_movie(ms):
    data_dic = {}
    for m in ms:
        if qa_interface.answer(m + '简介').__len__() > 10:
            data_list = qa_interface.answer(m + '上映日期').split('、')
            data = max(d for d in data_list)
            data_dic.setdefault(m, data)
        data_dic = dict(sorted(data_dic.items(), key=lambda x: x[1], reverse=True))
    count = 0
    for k in data_dic:
        count += 1
        st.info('No.' + str(count) + ' ' + k + '------上映日期：' + data_dic[k])
        st.write('简介：' + qa_interface.answer(k + '简介'))


# 3. 演员周星驰出演过哪些类型的电影
def actor_kind_movie(question):
    kind = qa_interface.answer(question).split('、')
    for k in kind:
        movies = qa_interface.answer(question.replace('类型', k + '类型')).split('、')
        st.info(k)
        for m in movies:
            st.subheader(m)
            st.write('简介：' + qa_interface.answer(m + '简介')[0:100] + '...')


# 4. 演员基本信息
def actor_info(actors):
    for a in actors:
        st.info(a)
        name_en = qa_interface.answer(a + '英文名')
        if name_en == '':
            name_en = '😕暂无详细信息...'
        '英文名: ', name_en
        bio2 = qa_interface.answer(a + '生日')
        if bio2 == '':
            bio2 = '😕暂无详细信息...'
        st.write('生  日:   ' + bio2)

        bio2 = qa_interface.answer(a + '出生地')
        if bio2 == '':
            bio2 = '😕暂无详细信息...'
        '出生地: ', bio2
        bio2 = qa_interface.answer(a + '简介')
        if bio2 == '':
            bio2 = '😕暂无详细信息...'
        '简  介: ', bio2[0:100] + '...'


if __name__ == '__main__':
    qa_interface = get_interface()

    with open(r'actor.txt', 'r', encoding='utf-8') as a:
        actor_list = a.readlines()
    with open(r'movie.txt', 'r', encoding='utf-8') as m:
        movie_list = m.readlines()

    ANS_list_actor = qa_interface.answer('所有演员周星驰').split('、')
    ANS_list_movie = qa_interface.answer('所有电影功夫').split('、')
    home_btn = st.sidebar.button('问答KBQA')
    actor_btn = st.sidebar.button('演员')
    movie_btn = st.sidebar.button('电影')
    actor_inp = st.sidebar.text_input('演员', key='I1')
    movie_inp = st.sidebar.text_input('电影', key='I2')
    index = 3
    if actor_inp:
        index = 4
    if movie_inp:
        index = 5
    if movie_inp and actor_inp:
        index = 6
    if actor_btn or index == 1:
        st.header('所有演员基本信息')
        for actor in ANS_list_actor:
            st.info(actor)
            bio = qa_interface.answer(actor + '简介')[0:100] + '...'
            if bio.__len__() > 10:
                st.write(bio)
            else:
                st.write('😕该演员比较神秘，暂无更多信息...')
        index = 1
    if movie_btn or index == 2:
        st.header('所有电影基本简介')
        for movie in ANS_list_movie[0:500]:
            # st.info('片名：《' + movie + '》')
            bio = qa_interface.answer(movie + '简介')[0:100] + '...'
            if bio.__len__() > 10:
                st.info('片名：《' + movie + '》')
                st.write('简介：' + bio)
            # else:
            #     st.write('该电影比较神秘，暂无更多信息，欲知更多内容，敬请百度......')
        index = 2
    if home_btn or index == 3:
        movie_inp = ''
        actor_inp = ''
        key_word = ['演员', '电影', '排名', '排行', '类型', '评分']
        index = 3
        title()
        question = st.text_input("请输入你的问题：", key='Q1')

        # st.write(qa_interface.answer(question))

        # T1、以 演员 开头查询 电影
        if question[0:2] == '演员':
            question.replace('演员', '')
            # RES = qa_interface.answer(question).split('、')
            # 3. 演员周星驰出演的电影类型
            if question.__contains__('类型'):
                actor_kind_movie(question)
            # 2. 演员周星驰评分前10的电影
            if question.__contains__('评分'):
                question.replace('评分', '')
                movies = qa_interface.answer(question).split('、')
                rank_movie(movies)
            # 1. 演员周星驰出演的电影
            else:
                movies = qa_interface.answer(question).split('、')
                actor_movie(movies)
        # T2、以 电影 开头查询 演员
        elif question[0:2] == '电影':
            kind = ['冒险', '奇幻', '动画', '剧情', '恐怖', '动作', '喜剧', '历史', '西部', '惊悚', '犯罪', '纪录', '科幻', '悬疑', '音乐', '爱情',
                    '家庭', '战争', '电视电影']
            # 1. 电影类型
            if question.__contains__('类型'):
                for k in kind:
                    st.info(k)
                    if k == '电视电影':
                        k = '电视'
                    question = k + '电影'
                    movies = qa_interface.answer(question).split('、')[0:50]
                    count = 0
                    for m in movies:
                        if count <= 5:
                            bio = qa_interface.answer(m + '简介')[0:100]
                            if bio.__len__() > 10:
                                st.subheader(m)
                                st.write('简介：' + bio + '...')
                                count += 1
            if question.__contains__('排行'):
                top_movie = ['Holy Weapon', 'Qing Cheng Zhi Lei', '兔毫520', 'War of the Under World',
                             'The Love That is Wrong', 'Color of the Game', '上身', 'Muk lau hung gwong', '新难兄难弟', '邮差',
                             '何以笙箫默', '旺角风云', 'JACKY CHEUNG WORLD TOUR 07 HK', '打开我天空', 'Good Take!', '大唐玄奘', '殭尸叔叔',
                             'Qin Song', 'The Monkey King: Uproar in Heaven', '阳光灿烂的日子', '牯岭街少年杀人事件', '东宫西宫',
                             'Forrest Gump', '麻将', '西游记大结局之仙履奇缘', '二十四城记', '半生缘', '百年好合', '独立时代', 'Working Class',
                             'Keung gaan 3: Ol yau waak', '梦中人', 'Wan Zhu', '飞虎', 'Saving Mother Robot', '哺乳期的女人',
                             '龙在边缘', 'Hong deng qu', '色情男女', '杜拉拉追婚记', '十七岁 / 5 yue yi hao', '双城计中计',
                             'Jacky Cheung Private Corner', '不夜城', '半支烟', '王牌', '莫欺少年穷', '相爱相亲']
                rank_movie(top_movie)
        # T3、其他开头：最新上映的电影（20）
        elif question[0:2] == '最新':
            movies = ['Godzilla vs. Kong', 'Ex', 'Baghdad', 'Godzilla: King of Monsters', '江湖儿女',
                      'Escape Plan 2: Hades', 'Ip Man 4', 'Shadow', '地球最后的夜晚', '西游记·女儿国',
                      'Bing Feng : Yong Heng Zhi Men', 'Untitled Cloverfield Movie', 'Early Man', 'Dead Pigs', '无问西东',
                      'Journey to China: The Iron Mask Mystery', '红海行动', '妖铃铃', '妖猫传', 'Bleeding Steel', '血观音', '追捕',
                      'Gong Shou Dao', '新永不消逝的电波', '以青春的名义', 'Harry Potter ', ' A History Of Magic', '相爱相亲',
                      '24 Hours to Live', '常在你左右', 'The Golden Monk', 'S.M.A.R.T. Chase', '追龙', 'The Foreigner',
                      'The LEGO Ninjago Movie', 'Meditation Park', '西谎极落: 太爆‧太子‧太空舱', '二次初恋', 'Color of the Game',
                      '破·局', 'The Nut Job 2: Nutty by Nature', 'The Adventurers', '鲛珠传', '角色于我', '建军大业 ',
                      ' Jiànjūn Dàyè', 'Get Action', '喵星人', 'Come Across Love', '京城81号II', '抢红', '明月几时有',
                      '反转人生', '仙球大战', 'Zombiology: Enjoy Yourself Tonight', 'Youth Dinner', '原谅他77次', '荡寇风云', '美好的意外',
                      '29+1', '脱皮爸爸', '春娇救志明', '神秘家族']
            data_movie(movies)
        else:
            if question:
                st.write(qa_interface.answer(question))

        # if question != "":
        #     # st.text(qa_interface.answer(question))
        #
        #     # 1.所有
        #     if question.__contains__('所有'):
        #         # 1.某演员所有电影信息/某电影所有演员信息
        #         ans_list = qa_interface.answer(question).split('、')
        #         name_en = qa_interface.answer(ans_list[0] + '英文名')
        #         # if question[0] == '所':
        #         if name_en == '暂无...':
        #             for ans in ans_list:
        #                 st.info(ans)
        #                 bio2 = qa_interface.answer(ans + '上映日期').split('、')[0]
        #                 if bio2 == '':
        #                     bio2 = '暂无详细信息...'
        #                 st.write('上映日期:   ' + bio2)
        #                 # '上映日期: ', bio2.split('、')[0]
        #
        #                 bio3 = qa_interface.answer(ans + '评分')
        #                 if bio3 == '':
        #                     bio3 = '暂无详细信息...'
        #                 # st.write('评分:' + bio3)
        #                 '评  分: ', bio3.split('、')[0]
        #
        #                 bio4 = qa_interface.answer(ans + '演员')
        #                 if bio4 == '':
        #                     bio4 = '暂无详细信息...'
        #                 # st.write('主演:   ' + bio4)
        #                 '主  演: ', bio4
        #
        #                 bio1 = qa_interface.answer(ans + '简介')
        #                 if bio1 == '':
        #                     bio1 = '暂无详细信息...'
        #                 # st.write(' 简介:\n' + bio1[0:100] + '...')
        #                 '简  介: ', bio1[0:100].replace('　　', '') + '...'
        #         if name_en != '暂无...':
        #             for ans in ans_list:
        #                 st.info(ans)
        #                 name_en = qa_interface.answer(ans + '英文名')
        #                 if name_en == '':
        #                     name_en = '暂无详细信息...'
        #                 '英文名: ', name_en
        #                 bio2 = qa_interface.answer(ans + '生日')
        #                 if bio2 == '':
        #                     bio2 = '暂无详细信息...'
        #                 st.write('生  日:   ' + bio2)
        #
        #                 bio2 = qa_interface.answer(ans + '出生地')
        #                 if bio2 == '':
        #                     bio2 = '暂无详细信息...'
        #                 '出生地: ', bio2
        #                 bio2 = qa_interface.answer(ans + '简介')
        #                 if bio2 == '':
        #                     bio2 = '暂无详细信息...'
        #                 '简  介: ', bio2[0:100] + '...'
        #
        #     # 2.某演员的电影评分排行
        #     if question.__contains__('排'):
        #         # question = question.replace('排行', '')
        #         ans_list = qa_interface.answer(question).split('、')
        #         if question.__contains__('所有'):
        #             ans_list = ANS_list3
        #
        #         if ans_list.__len__() > 10:
        #             ans_list = ans_list[0:15]
        #         else:
        #             rank_dic = {}
        #             for ans in ans_list:
        #                 rank = qa_interface.answer(ans + '评分').split('、')[0]
        #                 if rank == '暂无...':
        #                     rank = '0'
        #                 rank_dic.setdefault(ans, rank)
        #                 # st.info(rank + ans)
        #             rank_dic = dict(sorted(rank_dic.items(), key=lambda x: x[1], reverse=True))
        #             num = 0
        #             for k in rank_dic:
        #                 num += 1
        #                 st.info('No.' + str(num) + '  ' + k + ' -----评分： ' + rank_dic[k])
        #                 st.write('简介： ' + qa_interface.answer(k + '简介')[0:100] + '...')
    if index == 4:
        for actor in actor_list:
            if actor_inp.__contains__(actor.replace('\n', '')):
                st.success('演员：' + actor)
                st.write('英文名：' + qa_interface.answer(actor + '英文名'))
                st.write('出生日期：' + qa_interface.answer(actor + '生日'))
                st.write('出生地：' + qa_interface.answer(actor + '出生地'))
                st.write('个人简介：' + qa_interface.answer(actor + '简介'))
                movies = qa_interface.answer(actor + '电影').split('、')
                actor_movie(movies)

        # st.info(actor_inp)
    if index == 5:
        for movie in movie_list:
            if movie_inp.__contains__(movie.replace('\n', '')):
                # st.success('电影信息')
                actor_movie([movie])
                actors = qa_interface.answer(movie + '演员').split('、')
                st.header('演员介绍')
                actor_info(actors)

    if index == 6:
        # question = st.text_input('请输入查询', value=actor_inp + movie_inp)
        st.success(actor_inp)
        st.write('简介：' + qa_interface.answer(actor_inp + '简介'))
        movies = qa_interface.answer(actor_inp + '电影').split('、')
        # for m in movies:
        #     st.write()
        st.success('《' + movie_inp + '》')
        st.write('简介：' + qa_interface.answer(movie_inp + '简介'))
        st.write('主演：' + qa_interface.answer(movie_inp + '演员'))
