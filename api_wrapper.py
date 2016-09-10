import requests

class Question:
    def __init__(self):
        self.answer_strings = list()
        self.button_strings = list()
        self.answer_ids = list()
        self.question_text = ""
        self.right_answer = ""


class Test:
    def __init__(self, test_id, **credentials):
        self.test_id = test_id
        self.session_id = 0
        self.questions = dict()  # TODO: populate
        self.last_id = 0
        self.questions_left = len(self.questions)

    appid = "306"
    appsgn = "d8629af695839ba5481757a519e57fb1"

    def login(self):
        query = "http://dev.moyuniver.ru/api/php/v03/api_login.php?login=guest&pass=guest" \
                "&memberid=&phoneid=&appid=306&appsgn=d8629af695839ba5481757a519e57fb1" \
                "&appcode=&os=&ver=&width=&height="
        r = requests.get(query)
        return r.text

    def construct_query(self, params):
        pass

    def validate_answer(self, string_index):
        """

        :return: {right: bool, right_answer: str, next_button: str}
        """
        pass

    def get_next_question(self):
        """

        :param qui:
        :return: {'id': list question + 4 answers}
        """
        pass

    def advert(self):
        return "Купи наше приложение, там больше вопросов, БОЛЬШЕ ВОПРОСОВ!"

    def terminate(self):
        pass

t = Test()