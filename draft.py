import pymorphy2
import re
import sqlite3
from pprint import pprint


# def check_including(result, object):
#     for element in result:
#         if object in element:
#             return True
#     return False
#
#
# def analyzeWord(tag, cursor: sqlite3.Cursor) -> None:
#     if tag.aspect and tag.aspect not in aspect:
#         insert = "INSERT INTO aspect (title) VALUES ('{}')".format(tag.aspect)
#         cursor.execute(insert)
#         aspect.append(tag.aspect)
#     if tag.tense and tag.tense not in tense:
#         insert = "INSERT INTO tense (title) VALUES ('{}')".format(tag.tense)
#         cursor.execute(insert)
#         tense.append(tag.tense)
#     if tag.person and tag.person not in person:
#         insert = "INSERT INTO person (title) VALUES ('{}')".format(tag.person)
#         cursor.execute(insert)
#         person.append(tag.person)
#     if tag.number and tag.number not in number:
#         insert = "INSERT INTO number (title) VALUES ('{}')".format(tag.number)
#         cursor.execute(insert)
#         number.append(tag.number)
#     if tag.gender and tag.gender not in gender:
#         insert = "INSERT INTO gender (title) VALUES ('{}')".format(tag.gender)
#         cursor.execute(insert)
#         gender.append(tag.gender)
#     if tag.POS and tag.POS not in pos:
#         insert = "INSERT INTO pos (title) VALUES ('{}')".format(tag.POS)
#         cursor.execute(insert)
#         pos.append(tag.POS)
#     if tag.case and tag.case not in case:
#         insert = "INSERT INTO cas (title) VALUES ('{}')".format(tag.case)
#         cursor.execute(insert)
#         case.append(tag.case)
#
#
# def check_word_in_db(word, cursor: sqlite3.Cursor):
#     select = "SELECT 1 FROM words WHERE title = '{}'".format(word)
#     result = cursor.execute(select).fetchone()
#     if result:
#         return True
#     return False
#
#
# with open("file.txt", 'r', encoding="utf-8") as f:
#     morph = pymorphy2.MorphAnalyzer()
#     text = f.read()
#     words = re.sub("[^А-Яа-я0-9]", " ", text).lower().split()
#
#     connection = sqlite3.connect("db/first.db")
#     cursor = connection.cursor()
#
#     result = cursor.execute("SELECT title FROM pos").fetchall()
#     pos = [element[0] for element in result if element[0] != "None"]
#
#     result = cursor.execute("SELECT title FROM gender").fetchall()
#     gender = [element[0] for element in result if element[0] != "None"]
#
#     result = cursor.execute("SELECT title FROM number").fetchall()
#     number = [element[0] for element in result if element[0] != "None"]
#
#     result = cursor.execute("SELECT title FROM person").fetchall()
#     person = [element[0] for element in result if element[0] != "None"]
#
#     result = cursor.execute("SELECT title FROM tense").fetchall()
#     tense = [element[0] for element in result if element[0] != "None"]
#
#     result = cursor.execute("SELECT title FROM aspect").fetchall()
#     aspect = [element[0] for element in result if element[0] != "None"]
#
#     result = cursor.execute("SELECT title FROM cas").fetchall()
#     case = [element[0] for element in result if element[0] != "None"]
#
#     for word in words:
#         result = morph.parse(word)[0]
#         tag = result.tag
#
#         if check_word_in_db(word, cursor):
#             update = """UPDATE words
#                         SET count = count + 1
#                         WHERE title = '{}'""".format(word)
#             cursor.execute(update)
#         else:
#             analyzeWord(tag, cursor)
#             grammems_for_word = [('pos', tag.POS), ('gender', tag.gender),
#                                  ('number', tag.number), ('person', tag.person),
#                                  ('tense', tag.tense), ('aspect', tag.aspect),
#                                  ('cas', tag.case)]
#             select = "SELECT id FROM {} WHERE title = '{}'"
#             result_id = []
#             for grammem in grammems_for_word:
#                 result_id.append(cursor.execute(select.format(grammem[0], grammem[1])).fetchone()[0])
#             insert = "INSERT INTO words (title, pos, gender, number, " \
#                      "person, tense, aspect, cas, count) VALUES " \
#                      "('{}', {}, {}, {}, {}, {}, {}, {}, 1)".format(word, *result_id)
#             cursor.execute(insert)
#
#
#     connection.commit()



# connection = sqlite3.connect("db/main.db")
# cursor = connection.cursor()
#
# result = cursor.execute("""SELECT words.title, pos.title, person.title, tense.title,
#                                 aspect.title, gender.title, number.title, cas.title FROM words
#                             JOIN pos ON words.pos = pos.id
#                             JOIN person ON words.person = person.id
#                             JOIN tense ON words.tense = tense.id
#                             JOIN aspect ON words.aspect = aspect.id
#                             JOIN gender ON words.gender = gender.id
#                             JOIN number ON words.number = number.id
#                             JOIN cas ON words.cas = cas.id
#                             WHERE pos.title = 'NOUN'""").fetchall()
# pprint(result)



with open("file.txt", 'r', encoding="utf-8") as f:
    morph = pymorphy2.MorphAnalyzer()
    text = f.read()
    words = re.sub("[^А-Яа-я0-9]", " ", text).lower().split()

    result = morph.parse(words[0])[0]

    print(words[0], result.normal_form)
