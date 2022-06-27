import sys
import pymorphy2
import re

from PyQt5 import uic
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QFileDialog


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_font_families()
        self.setBackground()
        self.load()

    def load(self):
        uic.loadUi('designer/main.ui', self)

        self.load_button.clicked.connect(self.loadFile)
        self.analysis.clicked.connect(self.analyzer)

        self.setStyleForMainLabel(self.main_label)

        self.setStyleForText(self.text)

        self.setStyleForButton(self.load_button)
        self.setStyleForButton(self.analysis)

    def load_font_families(self):
        QFontDatabase.addApplicationFont("fonts/Old.ttf")

    def setBackground(self):
        self.setStyleSheet("background-color: #B19E7C")

    def setStyleForMainLabel(self, label):
        label.setFont(QFont("Old Standard TT", 26))
        label.setStyleSheet("color: #E2DA9C;"
                            "background-color: #564333;"
                            "border: 2px solid #E2DA9C")

    def setStyleForText(self, widget):
        widget.setFont(QFont("Old Standard TT", 12))
        widget.setStyleSheet("color: #E2DA9C;"
                            "background-color: #564333;"
                            "border: 2px solid #E2DA9C")

    def setStyleForButton(self, button):
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

    def analyzer(self):
        if not self.text.toPlainText():
            return

        morph = pymorphy2.MorphAnalyzer()

        text = self.text.toPlainText()
        # "Чистка" текста с помощью библиотеки re
        filtered_text = re.sub("[^А-Яа-я0-9]", " ", text).lower().split()

        out_dict = {"Имя существительное": 0, "Имя прилагательное": 0, "Глагол": 0, "Причастие": 0,
                    "Деепричастие": 0, "Числительное": 0, "Наречие": 0, "Предлог": 0, "Союз": 0, "Частица": 0}

        noun = {}
        adjf = {}
        verb = {}
        prtf = {}
        grnd = {}
        numr = {}
        advb = {}
        prep = {}
        conj = {}
        prcl = {}

        most_popular_words = {}

        for word in filtered_text:
            result = morph.parse(word)[0]
            normal_form = result.normal_form
            result_tag = result.tag
            if "NOUN" in result_tag:
                out_dict["Имя существительное"] += 1
                if word not in noun:
                    noun[word] = 0
                noun[word] += 1
            elif "ADJF" in result_tag or "ADJS" in result_tag:
                out_dict["Имя прилагательное"] += 1
                if word not in adjf:
                    adjf[word] = 0
                adjf[word] += 1
            elif "VERB" in result_tag or "INFN" in result_tag:
                out_dict["Глагол"] += 1
                if word not in verb:
                    verb[word] = 0
                verb[word] = 0
            elif "PRTF" in result_tag or "PRTS" in result_tag:
                out_dict["Причастие"] += 1
                if word not in prtf:
                    prtf[word] = 0
                prtf[word] += 1
            elif "GRND" in result_tag:
                out_dict["Деепричастие"] += 1
                if word not in grnd:
                    grnd[word] = 0
                grnd[word] = 1
            elif "NUMR" in result_tag:
                out_dict["Числительное"] += 1
                if word not in numr:
                    numr[word] = 0
                numr[word] += 1
            elif "ADVB" in result_tag:
                out_dict["Наречие"] += 1
                if word not in advb:
                    advb[word] = 0
                advb[word] = 0
            elif "PREP" in result_tag:
                out_dict["Предлог"] += 1
                if word not in prep:
                    prep[word] = 0
                prep[word] += 1
            elif "CONJ" in result_tag:
                out_dict["Союз"] += 1
                if word not in conj:
                    conj[word] = 0
                conj[word] += 1
            elif "PRCL" in result_tag:
                out_dict["Частица"] += 1
                if word not in prcl:
                    prcl[word] = 0
                prcl[word] += 1

            if normal_form not in most_popular_words:
                most_popular_words[normal_form] = 0
            most_popular_words[normal_form] += 1

        sorted_popular_words = sorted(most_popular_words.items(), key=lambda item: item[1], reverse=True)
        popular_noun = sorted(noun.items(), key=lambda item: item[1], reverse=True)
        popular_adjf = sorted(adjf.items(), key=lambda item: item[1], reverse=True)
        popular_verb = sorted(verb.items(), key=lambda item: item[1], reverse=True)
        popular_prtf = sorted(prtf.items(), key=lambda item: item[1], reverse=True)
        popular_grnd = sorted(grnd.items(), key=lambda item: item[1], reverse=True)
        popular_numr = sorted(numr.items(), key=lambda item: item[1], reverse=True)
        popular_advb = sorted(advb.items(), key=lambda item: item[1], reverse=True)
        popular_prep = sorted(prep.items(), key=lambda item: item[1], reverse=True)
        popular_conj = sorted(conj.items(), key=lambda item: item[1], reverse=True)
        popular_prcl = sorted(prcl.items(), key=lambda item: item[1], reverse=True)

        popular_part_of_speech = [popular_noun, popular_adjf, popular_verb, popular_prtf, popular_grnd,
                                  popular_numr, popular_advb, popular_prep, popular_conj, popular_prcl]

        try:
            self.information = Information()
            self.information.set_part_of_speech(out_dict)
            self.information.set_most_popular_words(sorted_popular_words)
            self.information.set_popular_part_of_speech(popular_part_of_speech)
            self.information.show()
        except Exception:
            pass


class Information(Main):
    def load(self):
        uic.loadUi('designer/show_information.ui', self)

        self.setStyleForTitleLabel(self.count_label)
        self.setStyleForTitleLabel(self.popular_words_label)
        self.setStyleForTitleLabel(self.popular_words)

        self.setStyleForText(self.list_popular_words)
        self.setStyleForText(self.noun_list)
        self.setStyleForText(self.adjf_list)
        self.setStyleForText(self.verb_list)
        self.setStyleForText(self.prtf_list)
        self.setStyleForText(self.grnd_list)
        self.setStyleForText(self.numr_list)
        self.setStyleForText(self.advb_list)
        self.setStyleForText(self.prep_list)
        self.setStyleForText(self.conj_list)
        self.setStyleForText(self.prcl_list)

        self.setStyleForLabel(self.noun_label)
        self.setStyleForLabel(self.adjf_label)
        self.setStyleForLabel(self.verb_label)
        self.setStyleForLabel(self.prtf_label)
        self.setStyleForLabel(self.grnd_label)
        self.setStyleForLabel(self.numr_label)
        self.setStyleForLabel(self.advb_label)
        self.setStyleForLabel(self.prep_label)
        self.setStyleForLabel(self.conj_label)
        self.setStyleForLabel(self.prcl_label)
        self.setStyleForLabel(self.noun_label_2)
        self.setStyleForLabel(self.adjf_label_2)
        self.setStyleForLabel(self.verb_label_2)
        self.setStyleForLabel(self.prtf_label_2)
        self.setStyleForLabel(self.grnd_label_2)
        self.setStyleForLabel(self.numr_label_2)
        self.setStyleForLabel(self.advb_label_2)
        self.setStyleForLabel(self.prep_label_2)
        self.setStyleForLabel(self.conj_label_2)
        self.setStyleForLabel(self.prcl_label_2)

    def setStyleForTitleLabel(self, label):
        label.setFont(QFont("Old Standard TT", 14))
        label.setStyleSheet("color: #E2DA9C;"
                            "background-color: #564333;"
                            "border: 2px solid #E2DA9C")

    def setStyleForLabel(self, label):
        label.setFont(QFont("Old Standard TT", 8))
        label.setStyleSheet("color: #E2DA9C;"
                            "background-color: #564333;"
                            "border: 2px solid #E2DA9C")

    def set_part_of_speech(self, part_of_speech):
        self.noun_label.setText(f'{self.noun_label.text()} {str(part_of_speech["Имя существительное"])}')
        self.adjf_label.setText(f'{self.adjf_label.text()} {str(part_of_speech["Имя прилагательное"])}')
        self.verb_label.setText(f'{self.verb_label.text()} {str(part_of_speech["Глагол"])}')
        self.prtf_label.setText(f'{self.prtf_label.text()} {str(part_of_speech["Причастие"])}')
        self.grnd_label.setText(f'{self.grnd_label.text()} {str(part_of_speech["Деепричастие"])}')
        self.numr_label.setText(f'{self.numr_label.text()} {str(part_of_speech["Числительное"])}')
        self.advb_label.setText(f'{self.advb_label.text()} {str(part_of_speech["Наречие"])}')
        self.prep_label.setText(f'{self.prep_label.text()} {str(part_of_speech["Предлог"])}')
        self.conj_label.setText(f'{self.conj_label.text()} {str(part_of_speech["Союз"])}')
        self.prcl_label.setText(f'{self.prcl_label.text()} {str(part_of_speech["Частица"])}')

    def set_most_popular_words(self, most_popular_words):
        for i in range(min(len(most_popular_words), 10)):
            self.list_popular_words.addItem(most_popular_words[i][0])

    def set_popular_part_of_speech(self, list_part_of_speech):
        for element in list_part_of_speech:
            for i in range(min(len(element), 5)):
                if list_part_of_speech.index(element) == 0:
                    self.noun_list.addItem(element[i][0])
                elif list_part_of_speech.index(element) == 1:
                    self.adjf_list.addItem(element[i][0])
                elif list_part_of_speech.index(element) == 2:
                    self.verb_list.addItem(element[i][0])
                elif list_part_of_speech.index(element) == 3:
                    self.prtf_list.addItem(element[i][0])
                elif list_part_of_speech.index(element) == 4:
                    self.grnd_list.addItem(element[i][0])
                elif list_part_of_speech.index(element) == 5:
                    self.numr_list.addItem(element[i][0])
                elif list_part_of_speech.index(element) == 6:
                    self.advb_list.addItem(element[i][0])
                elif list_part_of_speech.index(element) == 7:
                    self.prep_list.addItem(element[i][0])
                elif list_part_of_speech.index(element) == 8:
                    self.conj_list.addItem(element[i][0])
                else:
                    self.prcl_list.addItem(element[i][0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())