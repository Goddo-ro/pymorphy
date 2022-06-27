import sys
import pymorphy2
import re
import sqlite3

from PyQt5 import uic
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import (QFileDialog, QTableWidget, QTableWidgetItem,
    QLabel, QAbstractItemView, QHeaderView, QWidget, QPushButton, QMessageBox)


class Main(QMainWindow):
    try:
        db = "db/main.db"
        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        def __init__(self):
            super().__init__()
            self.load_font_families()
            self.setBackground()
            self.load()

        def load(self):
            uic.loadUi('designer/main2.ui', self)

            self.load_button.clicked.connect(self.loadFile)
            self.analysis.clicked.connect(self.analyzer)
            self.save_file.clicked.connect(self.saver)

            self.setStyleForMainLabel(self.main_label)

            self.setStyleForText(self.text)

            self.setStyleForButton(self.load_button)
            self.setStyleForButton(self.analysis)
            self.setStyleForButton(self.save_file)

        def load_font_families(self):
            QFontDatabase.addApplicationFont("fonts/Old.ttf")

        def setBackground(self):
            self.setStyleSheet("background-color: #B19E7C")

        def setStyleForMainLabel(self, label: QLabel) -> None:
            label.setFont(QFont("Old Standard TT", 26))
            label.setStyleSheet("color: #E2DA9C;"
                                "background-color: #564333;"
                                "border: 2px solid #E2DA9C")

        def setStyleForText(self, widget: QWidget) -> None:
            widget.setFont(QFont("Old Standard TT", 12))
            widget.setStyleSheet("color: #E2DA9C;"
                                "background-color: #564333;"
                                "border: 2px solid #E2DA9C")

        def setStyleForButton(self, button: QPushButton) -> None:
            # Установка шрифта для кнопки
            button.setFont(QFont("Old Standard TT", 16))
            # Установка стилей QSS
            button.setStyleSheet("QPushButton {"
                                     "background-color: #564333;"
                                     "color: #E2DA9C;"
                                     "border: 2px solid #E2DA9C;}"
    
                                 "QPushButton::hover{"
                                     "background-color : #222222;"
                                     "color: #D1A961;}")

        def loadFile(self):
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]

            if not fname:
                return

            with open(fname, 'r', encoding="utf-8") as file:
                data = file.read()

                self.text.setText(data)

        def check_word_in_db(self, word: str, cursor: sqlite3.Cursor) -> bool:
            select = "SELECT 1 FROM words WHERE title = '{}'".format(word)
            result = cursor.execute(select).fetchone()
            if result:
                return True
            return False

        def analyzer(self):
            try:
                if not self.text.toPlainText():
                    return

                cursor = self.cursor

                # Обновление автоинкремента id и чистка базы данных
                deletes = ["delete from words", "delete from aspect", "delete from cas",
                           "delete from gender", "delete from number", "delete from person",
                           "delete from pos", "delete from tense", "delete from sqlite_sequence where name IN "
                                                                   "('aspect', 'cas', 'gender', 'number', "
                                                                   "'person', 'pos', 'tense', 'words')"]

                for delete in deletes:
                    cursor.execute(delete)

                morph = pymorphy2.MorphAnalyzer()

                text = self.text.toPlainText()
                words = re.sub("[^А-Яа-я0-9]", " ", text).lower().split()

                result = cursor.execute("SELECT title FROM pos").fetchall()
                pos = [element[0] for element in result]

                result = cursor.execute("SELECT title FROM gender").fetchall()
                gender = [element[0] for element in result]

                result = cursor.execute("SELECT title FROM number").fetchall()
                number = [element[0] for element in result]

                result = cursor.execute("SELECT title FROM person").fetchall()
                person = [element[0] for element in result]

                result = cursor.execute("SELECT title FROM tense").fetchall()
                tense = [element[0] for element in result]

                result = cursor.execute("SELECT title FROM aspect").fetchall()
                aspect = [element[0] for element in result]

                result = cursor.execute("SELECT title FROM cas").fetchall()
                case = [element[0] for element in result]

                for word in words:
                    result = morph.parse(word)[0]
                    tag = result.tag
                    if self.check_word_in_db(word, cursor):
                        update = """UPDATE words
                                    SET count = count + 1
                                    WHERE title = '{}'""".format(word)
                        cursor.execute(update)
                    else:
                        aspect_value = str(tag.aspect)
                        tense_value = str(tag.tense)
                        person_value = str(tag.person)
                        number_value = str(tag.number)
                        gender_value = str(tag.gender)
                        pos_value = str(tag.POS)
                        case_value = str(tag.case)
                        if aspect_value and aspect_value not in aspect:
                            insert = "INSERT INTO aspect (title) VALUES ('{}')".format(aspect_value)
                            cursor.execute(insert)
                            aspect.append(aspect_value)
                        if tense_value and tense_value not in tense:
                            insert = "INSERT INTO tense (title) VALUES ('{}')".format(tense_value)
                            cursor.execute(insert)
                            tense.append(tense_value)
                        if person_value and person_value not in person:
                            insert = "INSERT INTO person (title) VALUES ('{}')".format(person_value)
                            cursor.execute(insert)
                            person.append(person_value)
                        if number_value and number_value not in number:
                            insert = "INSERT INTO number (title) VALUES ('{}')".format(number_value)
                            cursor.execute(insert)
                            number.append(number_value)
                        if gender_value and gender_value not in gender:
                            insert = "INSERT INTO gender (title) VALUES ('{}')".format(gender_value)
                            cursor.execute(insert)
                            gender.append(gender_value)
                        if pos_value and pos_value not in pos:
                            insert = "INSERT INTO pos (title) VALUES ('{}')".format(pos_value)
                            cursor.execute(insert)
                            pos.append(pos_value)
                        if case_value and case_value not in case:
                            insert = "INSERT INTO cas (title) VALUES ('{}')".format(case_value)
                            cursor.execute(insert)
                            case.append(case_value)
                        grammems_for_word = [('pos', pos_value), ('gender', gender_value),
                                             ('number', number_value), ('person', person_value),
                                             ('tense', tense_value), ('aspect', aspect_value),
                                             ('cas', case_value)]
                        select = "SELECT id FROM {} WHERE title = '{}'"
                        result_id = []
                        for grammem in grammems_for_word:
                            result_id.append(cursor.execute(select.format(grammem[0], grammem[1])).fetchone()[0])
                        insert = "INSERT INTO words (title, pos, gender, number, " \
                                 "person, tense, aspect, cas, count) VALUES " \
                                 "('{}', {}, {}, {}, {}, {}, {}, {}, 1)".format(word, *result_id)
                        cursor.execute(insert)
                self.connection.commit()

                self.informator = Information()
                self.informator.show()
            except Exception as Er:
                print(Er)

        def saver(self):
            options = QFileDialog.Option()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                      "Text Files (*.txt)", options=options)

            if fileName:
                try:
                    if len(fileName) < 4 or fileName[-4:] != ".txt":
                        fileName += '.txt'
                    with open(fileName, 'w', encoding="utf-8") as writing_file:
                        writing_file.write(self.text.toPlainText())

                    self.showDialog("Файл успешно сохранен")
                except Exception as Er:
                    print(Er)

        def showDialog(self, message):
            msgBox = QMessageBox()
            self.setStyleForButton(msgBox)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(message)
            msgBox.setWindowTitle("Ответ")
            msgBox.setStandardButtons(QMessageBox.Ok)

            returnValue = msgBox.exec()
            if returnValue:
                return

    except Exception as Er:
        print(Er)


class Information(Main):
    def load(self):
        uic.loadUi('designer/show_information2.ui', self)
        self.select_for_table = """SELECT words.title, pos.title, person.title, tense.title,
                                        aspect.title, gender.title, number.title, cas.title, count FROM words
                                    JOIN pos ON words.pos = pos.id
                                    JOIN person ON words.person = person.id
                                    JOIN tense ON words.tense = tense.id
                                    JOIN aspect ON words.aspect = aspect.id
                                    JOIN gender ON words.gender = gender.id
                                    JOIN number ON words.number = number.id
                                    JOIN cas ON words.cas = cas.id 
                                    {}
                                    ORDER BY words.count DESC"""

        self.setStyleForTitleLabel(self.popular_words_label)
        self.setStyleForTitleLabel(self.most_popular_words)
        self.setStyleForTitleLabel(self.information)

        self.setStyleForButton(self.noun)
        self.setStyleForButton(self.adjf)
        self.setStyleForButton(self.verb)
        self.setStyleForButton(self.prtf)
        self.setStyleForButton(self.grnd)
        self.setStyleForButton(self.numr)
        self.setStyleForButton(self.advb)
        self.setStyleForButton(self.prep)
        self.setStyleForButton(self.conj)
        self.setStyleForButton(self.prcl)

        self.setStyleForButton(self.save)

        self.noun.clicked.connect(self.get_noun_info)
        self.adjf.clicked.connect(self.get_adjf_info)
        self.verb.clicked.connect(self.get_verb_info)
        self.prtf.clicked.connect(self.get_prtf_info)
        self.grnd.clicked.connect(self.get_grnd_info)
        self.numr.clicked.connect(self.get_numr_info)
        self.advb.clicked.connect(self.get_advb_info)
        self.prep.clicked.connect(self.get_prep_info)
        self.conj.clicked.connect(self.get_conj_info)
        self.prcl.clicked.connect(self.get_prcl_info)

        self.save.clicked.connect(self.saver)

        self.setMostPopularWords()

    def setMostPopularWords(self, get=False):
        result = self.cursor.execute(self.select_for_table.format('')).fetchall()
        result = self.get_normal_titles(result)

        if get:
            return result

        self.show_table(result, (790, 670), self.most_popular_words)

    def setStyleForTitleLabel(self, label: QWidget) -> None:
        label.setFont(QFont("Old Standard TT", 14))
        label.setStyleSheet("color: #E2DA9C;"
                            "background-color: #564333;"
                            "border: 2px solid #E2DA9C")

    def setStyleForLabel(self, label: QWidget) -> None:
        label.setFont(QFont("Old Standard TT", 10))
        label.setStyleSheet("color: #E2DA9C;"
                            "background-color: #564333;"
                            "border: 2px solid #E2DA9C")

    def show_table(self, items, size=(820, 500), table=False) -> None:
        try:
            if items:
                self.table = table
                if not table:
                    self.table = QTableWidget()
                self.setStyleForLabel(self.table)
                self.table.resize(*size)
                self.table.setRowCount(0)
                self.table.setColumnCount(len(items[0]))
                for i, item in enumerate(items):
                    self.table.setRowCount(self.table.rowCount() + 1)
                    for j, element in enumerate(item):
                        self.table.setItem(i, j, QTableWidgetItem(str(element)))
                self.table.setHorizontalHeaderLabels(["Слово", "Часть речи", "Лицо", "Время", "Вид",
                                                      "Род", "Число", "Падеж", "Колличество повторов"])
                header = self.table.horizontalHeader()
                for i in range(self.table.columnCount()):
                    header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
                self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.table.show()
            else:
                self.nothing = QLabel("Ничего не найдено")
                self.nothing.resize(250, 50)
                self.setStyleForLabel(self.nothing)
                self.nothing.show()
        except Exception as Er:
            print(Er)

    def get_normal_titles(self, items: list) -> list:
        out_list = []
        for item in items:
            out_item = []
            for i, element in enumerate(item):
                if i == 1:
                    if element == 'NOUN':
                        out_item.append("Имя существительное")
                    elif element == 'ADJF' or element == "ADJS":
                        out_item.append("Имя прилагательное")
                    elif element == 'COMP':
                        out_item.append("Сомпатив")
                    elif element == 'VERB' or element == 'INFN':
                        out_item.append("Глагол")
                    elif element == 'PRTF' or element == 'PRTS':
                        out_item.append("Причастие")
                    elif element == 'GRND':
                        out_item.append("Деепричастие")
                    elif element == 'NUMR':
                        out_item.append("Числительное")
                    elif element == 'ADVB':
                        out_item.append("Наречие")
                    elif element == 'PREP':
                        out_item.append("Предлог")
                    elif element == 'CONJ':
                        out_item.append("Союз")
                    elif element == "PRCL":
                        out_item.append("Частица")
                    elif element == "INTJ":
                        out_item.append("Междометие")
                    else:
                        out_item.append("Не определено")
                elif i == 2:
                    if element == '1per':
                        out_item.append("1 лицо")
                    elif element == '2per':
                        out_item.append("2 лицо")
                    elif element == '3per':
                        out_item.append("3 лицо")
                    else:
                        out_item.append("Не определено")
                elif i == 3:
                    if element == 'pres':
                        out_item.append('Настоящее')
                    elif element == 'past':
                        out_item.append('Прошедшее')
                    elif element == 'futr':
                        out_item.append('Будущее')
                    else:
                        out_item.append("Не определено")
                elif i == 4:
                    if element == 'perf':
                        out_item.append('Совершенный')
                    elif element == 'impf':
                        out_item.append('Несовершенный')
                    else:
                        out_item.append("Не определено")
                elif i == 5:
                    if element == 'masc':
                        out_item.append('Мужской')
                    elif element == 'femn':
                        out_item.append('Женский')
                    elif element == 'neut':
                        out_item.append('Средний')
                    else:
                        out_item.append("Не определено")
                elif i == 6:
                    if element == 'sing':
                        out_item.append('Единственное')
                    elif element == 'plur':
                        out_item.append('Множественное')
                    else:
                        out_item.append("Не определено")
                elif i == 7:
                    if element == 'nomn':
                        out_item.append('Именительный')
                    elif element == 'gent':
                        out_item.append('Родительный')
                    elif element == 'datv':
                        out_item.append('Дательный')
                    elif element == 'accs':
                        out_item.append('Винительный')
                    elif element == 'ablt':
                        out_item.append('Творительный')
                    elif element == 'loct':
                        out_item.append('Предложный')
                    elif element == 'voct':
                        out_item.append('Звательный')
                    else:
                        out_item.append("Не определено")
                else:
                    out_item.append(element.capitalize() if type(element) == str else element)
            out_list.append(out_item)
        return out_list

    def get_noun_info(self, get=False):
        result = self.cursor.execute(self.select_for_table.format("WHERE pos.title = 'NOUN'"))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            fetchall()
        result = self.get_normal_titles(result)

        if get:
            return result

        self.show_table(result)

    def get_adjf_info(self, get=False):
        result = self.cursor.execute(self.select_for_table.format("WHERE pos.title = 'ADJF' "
                                                                  "OR pos.title = 'ADJS'")).fetchall()
        result = self.get_normal_titles(result)

        if get:
            return result

        self.show_table(result)

    def get_verb_info(self, get=False):
        result = self.cursor.execute(self.select_for_table.format("WHERE pos.title = 'VERB' "
                                                                  "OR pos.title = 'INFN'")).fetchall()
        result = self.get_normal_titles(result)

        if get:
            return result

        self.show_table(result)

    def get_prtf_info(self, get=False):
        result = self.cursor.execute(self.select_for_table.format("WHERE pos.title = 'PRTF' OR "
                                                                  "pos.title = 'PRTS'")).fetchall()
        result = self.get_normal_titles(result)

        if get:
            return result

        self.show_table(result)

    def get_grnd_info(self, get=False):
        result = self.cursor.execute(self.select_for_table.format("WHERE pos.title = 'GRND'")).fetchall()
        result = self.get_normal_titles(result)

        if get:
            return result

        self.show_table(result)

    def get_numr_info(self, get=False):
        result = self.cursor.execute(self.select_for_table.format("WHERE pos.title = 'NUMR'")).fetchall()
        result = self.get_normal_titles(result)

        if get:
            return result

        self.show_table(result)

    def get_advb_info(self, get=False):
        result = self.cursor.execute(self.select_for_table.format("WHERE pos.title = 'ADVB'")).fetchall()
        result = self.get_normal_titles(result)

        if get:
            return result

        self.show_table(result)

    def get_prep_info(self, get=False):
        result = self.cursor.execute(self.select_for_table.format("WHERE pos.title = 'PREP'")).fetchall()
        result = self.get_normal_titles(result)

        if get:
            return result

        self.show_table(result)

    def get_conj_info(self, get=False):
        result = self.cursor.execute(self.select_for_table.format("WHERE pos.title = 'CONJ'")).fetchall()
        result = self.get_normal_titles(result)

        if get:
            return result

        self.show_table(result)

    def get_prcl_info(self, get=False):
        result = self.cursor.execute(self.select_for_table.format("WHERE pos.title = 'PRCL'")).fetchall()
        result = self.get_normal_titles(result)

        if get:
            return result

        self.show_table(result)

    def saver(self):
        options = QFileDialog.Option()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Text Files (*.txt)", options=options)

        if fileName:
            try:
                if len(fileName) < 4 or fileName[-4:] != ".txt":
                    fileName += '.txt'
                popular_words = self.setMostPopularWords(True)
                noun = self.get_noun_info(True) # Существительное
                adjf = self.get_adjf_info(True) # Прилагательное
                verb = self.get_verb_info(True) # Глагол
                prtf = self.get_prtf_info(True) # Причастие
                grnd = self.get_grnd_info(True) # Деепричастие
                numr = self.get_numr_info(True) # Числительное
                advb = self.get_advb_info(True) # Наречие
                prep = self.get_prep_info(True) # Предлог
                conj = self.get_conj_info(True) # Союз
                prcl = self.get_prcl_info(True) # Частица

                def write_words(file, words):
                    for word in words:
                        file.write('\t' + ', '.join([str(element) for element in word]) + '\n')

                with open(fileName, 'w', encoding="Utf-8") as file:
                    file.write("Слова, упорядоченные по числу встреч:\n")
                    write_words(file, popular_words)
                    file.write('\n\nСамые популярные существительные:\n')
                    write_words(file, noun)
                    if not noun:
                        file.write('\t' + "Ничего не найдено\n")
                    file.write('\n\nСамые популярные прилагательные:\n')
                    write_words(file, adjf)
                    if not adjf:
                        file.write('\t' + "Ничего не найдено\n")
                    file.write('\n\nСамые популярные глаголы:\n')
                    write_words(file, verb)
                    if not verb:
                        file.write('\t' + "Ничего не найдено\n")
                    file.write('\n\nСамые популярные причастия:\n')
                    write_words(file, prtf)
                    if not prtf:
                        file.write('\t' + "Ничего не найдено\n")
                    file.write('\n\nСамые популярные деепричастия:\n')
                    write_words(file, grnd)
                    if not grnd:
                        file.write('\t' + "Ничего не найдено\n")
                    file.write('\n\nСамые популярные числительные:\n')
                    write_words(file, numr)
                    if not numr:
                        file.write('\t' + "Ничего не найдено\n")
                    file.write('\n\nСамые популярные наречия:\n')
                    write_words(file, advb)
                    if not advb:
                        file.write('\t' + "Ничего не найдено\n")
                    file.write('\n\nСамые популярные предлоги:\n')
                    write_words(file, prep)
                    if not prep:
                        file.write('\t' + "Ничего не найдено\n")
                    file.write('\n\nСамые популярные союзы:\n')
                    write_words(file, conj)
                    if not conj:
                        file.write('\t' + "Ничего не найдено\n")
                    file.write('\n\nСамые популярные частицы:\n')
                    write_words(file, prcl)
                    if not prcl:
                        file.write('\t' + "Ничего не найдено\n")

                    self.showDialog("Файл успешно сохранен")
            except Exception as Er:
                print(Er)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())