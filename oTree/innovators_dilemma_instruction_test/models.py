from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'instruction_test'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    investment_new_1 = models.BooleanField(
        label="あなたは新製品に投資を行いますか？",
        choices=[
            [10,"新製品に投資する"],
            [0,"なにもしない"],
        ],
        widget=widgets.RadioSelect,
    ) 


class Player(BasePlayer):
    test_1 = models.BooleanField(
        label="解答",
        choices =[
            [True,"〇"],
            [False,"×"],
            [False,"わからない"],
        ]
    )

    test_2 = models.BooleanField(
        label="解答",
        choices =[
            [False,"〇"],
            [True,"×"],
            [False,"わからない"],
        ]
    )

    test_3 = models.BooleanField(
        label="解答",
        choices =[
            [False,"0"],
            [False,"100"],
            [False,"150"],
            [True,"200"],
            [False,"250"],
            [False,"300"],
            [False,"400"],
            [False,"わからない"]
        ]
    )

    test_4 = models.BooleanField(
        label="解答",
        choices =[
            [False,"A"],
            [False,"B"],
            [True,"C"],
            [False,"D"],
            [False,"わからない"],
        ]
    )

    test_5 = models.BooleanField(
        label="解答",
        choices =[
            [False,"100"],
            [False,"150"],
            [False,"200"],
            [True,"250"],
            [False,"300"],
            [False,"400"],
            [False,"500"],
            [False,"600"],
            [False,"1000"],
            [False,"わからない"],
        ]
    )

