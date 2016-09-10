

class Test:
    def __init__(self, test_id, **credentials):
        self.test_id = test_id
        self.session_id = 0
        self.questions = dict()  # TODO: populate
        self.last_id = 0
        self.questions_left = len(self.questions)

    # def get_question_by_id(self, qid):
    #     """
    #
    #     :param qui:
    #     :return: {'id': list question + 4 answers}
    #     """
    #     self.last_id = qid
    #     pass

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
        self.last_id = qid
        pass

