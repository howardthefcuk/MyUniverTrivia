"""
This class is an object based wrapper for MoyUniver API
"""
import requests

class Question:
    def __init__(self):
        self.answer_strings = list()
        # self.button_strings = list()
        self.answer_ids = list()
        self.question_text = ""
        self.right_answer = ""
        self.question_id = ""
        self.question_type = ""
        self.question_session_id = ""

    def __str__(self):
        strrepr = "Q:{}\nAs:\n-{}\n\n{}".format(self.question_text, "\n-".join(self.answer_strings),
                                              "\n".join(self.answer_ids))
        return strrepr


class Test:
    appid = "306"
    appsgn = "d8629af695839ba5481757a519e57fb1"

    def __init__(self, test_id, **credentials):
        self.test_id = test_id
        self.session_id = 0
        self.questions = dict()  # TODO: populate
        self.current_id = 0
        self.questions_left = len(self.questions)
        self.member_id = self.login()
        self.test_id = test_id
        self.question_ids = list()
        # init the test
        query = "http://dev.moyuniver.ru/api/php/v03/api_runevent.php?eid={}&memberid={}&" \
                "appid={}&appsgn={}&appcode=&os=&ver=&width=&height=".format(
            self.test_id, self.member_id, self.appid, self.appsgn
        )
        r = requests.get(query)
        r.encoding = 'utf-8'
        assert r.status_code == 200
        test_text = r.text.strip()

        for line in test_text.split("\n"):
            line = line.strip()
            fields = line.split("#")
            if fields:
                question_type = fields[2]
                question_id = fields[1]
                question_session_id = fields[6]
                question_text = fields[3]
                answer_text = fields[5]
                answer_id = fields[4]
                if fields[1] not in self.questions:
                    self.question_ids.append(question_id)
                    self.questions[question_id] = Question()
                    self.questions[question_id].question_text = question_text
                    self.questions[question_id].question_session_id = question_session_id
                    self.questions[question_id].question_type = question_type
                self.questions[question_id].answer_strings.append(answer_text)
                self.questions[question_id].answer_ids.append(answer_id)
        self.session_id = fields[0]

    def login(self):
        query = "http://dev.moyuniver.ru/api/php/v03/api_login.php?login=guest&pass=guest" \
                "&memberid=&phoneid=&appid=306&appsgn=d8629af695839ba5481757a519e57fb1" \
                "&appcode=&os=&ver=&width=&height="
        r = requests.get(query)
        return r.text.split("#")[0]

    def validate_answer(self, answer_index):
        """

        :return: {right: bool, right_answer: str, next_button: str}
        """
        query = "http://dev.moyuniver.ru/api/php/v03/api_asheet_mod.php?tid={}&appid=306" \
                "&appsgn=d8629af695839ba5481757a519e57fb1&tsid={}&memberid={}&qtype={}&qid={}&a={}"
        last_id = self.current_id - 1
        question = self.questions[self.question_ids[last_id]]
        answer_id = question.answer_ids[answer_index]

        query = query.format(self.session_id, question.question_session_id, self.member_id,
                             question.question_type, question.question_id, answer_id)

        r = requests.get(query)
        right = bool(int(r.text))
        return right


    def get_next_question(self):
        """

        :param qui:
        :return: {'id': list question + 4 answers}
        """
        assert self.current_id < len(self.question_ids)
        question = self.questions[self.question_ids[self.current_id]]
        self.current_id += 1
        return question

    def advert(self):
        return "Купи наше приложение, там больше вопросов, БОЛЬШЕ ВОПРОСОВ!"

    def terminate(self):
        pass


t = Test("15692")
while True:
    try:
        input()
        q = t.get_next_question()
        print(str(q))
        res = t.validate_answer(int(input()))
        if res:
            print("Ok")
        else:
            print("/\\ox!")

    except:
        print("Кончились вопросы")
        break

