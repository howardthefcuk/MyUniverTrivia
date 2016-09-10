class Question:
    def __init__(self):
        self.answer_strings = list()
        self.button_strings = list()
        self.question_text = ""

class Test:
    def __init__(self, test_id, **credentials):
        self.test_id = test_id
        self.session_id = 0
        self.questions = dict()  # TODO: populate
        self.last_id = 0
        self.questions_left = len(self.questions)

    def validate_answer(self):
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

