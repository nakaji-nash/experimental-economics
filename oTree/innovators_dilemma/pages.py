from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class role_round(Page):
    pass



class Investment_new_1(Page):
    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number % 2 == 0 or self.player.id_in_group == 2 and self.round_number % 2 == 1

    form_model = "group"
    form_fields = ["investment_new_1"]  #Investment_new_1ステージで、Playerのinvestment_new_1を入力してもらう

class Investment_old_1(Page):
    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number % 2 == 0 or self.player.id_in_group == 1 and self.round_number % 2 == 1

    form_model = "group"
    form_fields = ["investment_old_1"]

class Investment_new_2(Page):
    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number % 2 == 0 and self.group.total_investments_1 == 0 or self.player.id_in_group == 1 and self.round_number % 2 == 0 and self.group.total_investments_1 == 1 or self.player.id_in_group == 2 and self.round_number % 2 == 1 and self.group.total_investments_1 == 0 or self.player.id_in_group == 2 and self.round_number % 2 == 1 and self.group.total_investments_1 == 1

    form_model = "group"
    form_fields = ["investment_new_2"]

class Investment_old_2(Page):
    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number % 2 == 0 and self.group.total_investments_1 == 0 or self.player.id_in_group == 2 and self.round_number % 2 == 0 and self.group.total_investments_1 == 10 or self.player.id_in_group == 1 and self.round_number % 2 == 1 and self.group.total_investments_1 == 0 or self.player.id_in_group == 1 and self.round_number % 2 == 1 and self.group.total_investments_1 == 10

    form_model = "group"
    form_fields = ["investment_old_2"]

class Investment_new_2_11_or_10(Page):
    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number % 2 == 0 and self.group.total_investments_1 == 11 or self.player.id_in_group == 1 and self.round_number % 2 == 0 and self.group.total_investments_1 == 10 or self.player.id_in_group == 2 and self.round_number % 2 == 1 and self.group.total_investments_1 == 10 or self.player.id_in_group == 2 and self.round_number % 2 == 1 and self.group.total_investments_1 == 11

    form_model = "group"
    form_fields = ["investment_new_2_11_or_10"]

class Investment_old_2_11_or_01(Page):
    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number % 2 == 0 and self.group.total_investments_1 == 11 or self.player.id_in_group == 2 and self.round_number % 2 == 0 and self.group.total_investments_1 == 1 or self.player.id_in_group == 1 and self.round_number % 2 == 1 and self.group.total_investments_1 == 11 or self.player.id_in_group == 1 and self.round_number % 2 == 1 and self.group.total_investments_1 == 1
    
    form_model = "group"
    form_fields = ["investment_old_2_11_or_01"]



class Results_new_1(Page):
    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number % 2 == 0 or self.player.id_in_group == 2 and self.round_number % 2 == 1

class Results_old_1(Page):
    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number % 2 == 0 or self.player.id_in_group == 1 and self.round_number % 2 == 1
#既存企業
class Results_new_2(Page):
    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number % 2 == 0 or self.player.id_in_group == 2 and self.round_number % 2 == 1

class Results_old_2(Page):
    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number % 2 == 0 or self.player.id_in_group == 1 and self.round_number % 2 == 1
#既存企業


#リスク選好テスト
class Test_risk(Page):
    form_model = "player"
    form_fields = ["question_0","question_1","question_2",
                    "question_3","question_4",
                    "question_5","question_6",
                    "question_7","question_8",
                    "question_9","question_10",
                    "question_11","question_12",
                    "question_13","question_14",
                    "question_15","question_16",
                    "question_17","question_18",
                    "question_19","question_20",]
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

#性格テスト　→　（利己的、利他的、競争的）
class Test_personality(Page):
    form_model = "player"
    form_fields = ["question_p_1","question_p_2",
                    "question_p_3","question_p_4",
                    "question_p_5","question_p_6",
                    "question_p_7","question_p_8",
                    "question_p_9",
                    ]
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Start(Page):
    def is_displayed(self):
        return self.round_number == 1

#待機&計算のページ
class FirstWaitPage(WaitPage):
    group_by_arrival_time = True #到着順にグループ化していく
    def is_displayed(self):
        return self.round_number == 1

class FirstAllRoundWaitpage(WaitPage):
    pass

class ResultsWaitPage_1(WaitPage):
    after_all_players_arrive = 'compute_1'
        
class ResultsWaitPage_2(WaitPage):
    after_all_players_arrive = 'compute_2'


class FinalWaitPage(WaitPage):
    pass

class Final_Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [  #ページの順番
    FirstWaitPage,  #到着順にグループ化していく
    Start,
    role_round,
    Investment_new_1,
    Investment_old_1,
    ResultsWaitPage_1,
    Results_new_1,
    Results_old_1,
    Investment_new_2,
    Investment_new_2_11_or_10,
    Investment_old_2,
    Investment_old_2_11_or_01,
    ResultsWaitPage_2,
    Results_new_2,
    Results_old_2,
    FinalWaitPage,
    Final_Results,
    Test_risk,
    Test_personality,
    ]
