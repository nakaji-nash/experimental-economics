from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Notes(Page):
    pass


class Instruction(Page):
    pass

class inst_Investment_new_1(Page):
    pass
class inst_Investment_old_1(Page):
    pass

class Test(Page):
    form_model = "player"
    form_fields = ["test_1","test_2",
                    "test_3","test_4",
                    "test_5",
                    ]

    def test_1_error_message(self, test_1):
        if test_1 != True:
            return '※　役割は各ラウンドごとに交互に入れ替わります。'

    def test_2_error_message(self, test_2):
        if test_2 !=  True:
            return '※　一期目に「新製品に投資」を選択した場合、二期目も引き続き「新製品に投資」することになり、別の選択をすることはできません。'

    def test_3_error_message(self, test_3):
        if test_3 != True:
            return '※　左側の青字の選択肢があなたの選択肢、右上の選択肢が相手の選択肢です。セルに（A、B）とある場合、Aがあなたのポイント、Bが相手のポイントです。'

    def test_4_error_message(self, test_4):
        if test_4 != True :
            return '※　４つの表の上に、それぞれあなたと相手の選択肢の組み合わせについて書かれています。確認してください。'

    def test_5_error_message(self, test_5):
        if test_5 != True :
            return '※　一期目に、あなた：「既存製品に投資」、相手：「新製品に投資」を選ぶ場合、一期目の獲得ポイントは300です。二期目のポイント表は、下部の４つの表のうち、左下の表になり、二期目の獲得ポイントは400です。一期目と二期目のポイントを足すと700です。'




class End_instruction(Page):
    pass



page_sequence = [
    #inst_Investment_old_1,
    Notes,
    Instruction,
    Test,
    End_instruction,
    ]
