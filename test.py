# -*- coding: utf-8 -*-
"""
__mktime__ = '2020/12/9'
__author__ = 'Letu'
__filename__ = 'test'
"""

if __name__ == "__main__":

    s1 = '''反转人生
仙球大战
Zombiology: Enjoy Yourself Tonight
Youth Dinner
原谅他77次
荡寇风云
美好的意外
29+1
脱皮爸爸
春娇救志明
神秘家族'''
    # s1 = s1.replace('\n', '-').replace('    ', '')
    # print(s1.split('-'))
    # print('2017-10-28' < '2017-11-28')
    with open(r'actor.txt', 'r', encoding='utf-8') as a:
        actor_list = a.readlines()
    print(actor_list)