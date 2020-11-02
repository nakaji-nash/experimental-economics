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

import random
from random import randint

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'innovators_dilemma'
    players_per_group = 2
    num_rounds = 24



"""
ステージの条件分岐　Stage_type
stage_type == 1 　→　30%で拡大：70%で縮小
stage_type == 2 　→　50%で拡大：50%で縮小
stage_type == 3 　→　700%で拡大：30%で縮小
"""







class Subsession(BaseSubsession):

    random_vars_stage = models.LongStringField()#記録用
    stage_type = models.IntegerField() #ステージの3種類のタイプ（30、5 = models.IntegerField()
    expansion_or_shrink = models.IntegerField() #拡大＝１　縮小＝２
    stage_type_random = models.IntegerField() #計算用のランダム変数


    def creating_session(self):

        if self.round_number == 4 or self.round_number ==6 or self.round_number ==13 or self.round_number ==15 or self.round_number ==17 or self.round_number ==18 or self.round_number ==21 or self.round_number ==23:
            self.stage_type = 1
        elif self.round_number == 2 or self.round_number ==3 or self.round_number == 9 or self.round_number == 16 or self.round_number == 19 or self.round_number == 20  or self.round_number == 22 or self.round_number ==24:
            self.stage_type = 2
        elif self.round_number == 1 or self.round_number ==5 or self.round_number ==7 or self.round_number ==8 or self.round_number ==10 or self.round_number ==11 or self.round_number ==12 or self.round_number ==14 :
            self.stage_type = 3


        

#ラウンドごとに数値をリセット

        '''
        total_investment_1 = 0
        total_investment_2 = 0
        payoff_new = 0
        payoff_old = 0
        '''


#「Subsession.random_vars_stage 」は　ステージの拡大縮小を決める

        for group in self.get_players():
            group.stage_type_random = random.randint(1,100)
            Subsession.random_vars_stage = group.stage_type_random
            self.random_vars_stage = str(Subsession.random_vars_stage)


            if self.stage_type == 1:
                if Subsession.random_vars_stage < 30 :
                    self.expansion_or_shrink = 1
                else:
                    self.expansion_or_shrink = 2
            elif self.stage_type == 2:
                if Subsession.random_vars_stage < 50 :
                    self.expansion_or_shrink = 1
                else:
                    self.expansion_or_shrink = 2           
            elif self.stage_type == 3:
                if Subsession.random_vars_stage < 70 :
                    self.expansion_or_shrink = 1
                else:
                    self.expansion_or_shrink = 2



#random_vars_stageは記録用



#１ラウンドはランダム、そのあとは同じグループで
#変える可能性あり（確認テストを終わった人からマッチングする場合変更するかも）
# →　インストラクション＆確認テストとゲームを別々アプリとして繋げたらいける
        if self.round_number == 1:
            self.group_randomly()
        else:
            self.group_like_round(1)

class Group(BaseGroup):
    payoff_new_1 = models.CurrencyField() #一期目の利得
    payoff_old_1 = models.CurrencyField()
    payoff_new_2 = models.CurrencyField() #二期目の利得
    payoff_old_2 = models.CurrencyField()
    payoff_new = models.CurrencyField() #ラウンドの合計利得　→　全部の合計はpayoff
    payoff_old = models.CurrencyField()
    
    random_vars_stage = models.LongStringField()#記録用
    stage_type_random = models.IntegerField() 
    total_investments_1 = models.IntegerField()
    #11 → 一期目に両方が投資, 10　→ 一期目に新規だけ投資, 1 →　一期目に既存だけ投資
    total_investments_2 = models.IntegerField()









    
    #投資したかどうか。
    investment_new_1 = models.IntegerField(
        label="一期目から、あなたは新製品に投資を行いますか？",
        choices=[
            [10,"新製品に投資する"],
            [0,"なにもしない"],
        ],
        widget=widgets.RadioSelect,
    ) 
    investment_new_2 = models.IntegerField(
        label="二期目に、あなたは新製品に投資を行いますか？",
        choices=[
            [20,"新製品に投資する"],
            [0,"なにもしない"],
        ],
        widget=widgets.RadioSelect,
        initial = 3000
    )
    investment_new_2_11_or_10 = models.IntegerField(
        label="引き続き、新製品に投資します。",
        choices=[
            [3000,"確認しました。"],
        ],
        widget=widgets.RadioSelect,
    )
    investment_old_1 = models.IntegerField(
        label="一期目から、あなたは新製品に投資を行いますか？",
        choices=[
            [1,"新製品に投資する"],
            [0,"既存製品に投資する"],
        ],
        widget=widgets.RadioSelect,
    )
    investment_old_2 = models.IntegerField(
            label="二期目に、あなたは新製品に投資を行いますか？",
        choices=[
            [2,"新製品に投資する"],
            [0,"既存製品に投資する"],
        ],
        widget=widgets.RadioSelect,
    )
    investment_old_2_11_or_01 = models.IntegerField(
            label="引き続き、新製品に投資します。",
        choices=[
            [3000,"確認しました。"],
        ],
        widget=widgets.RadioSelect,
    )


#一期目の計算
    def compute_1(self):

        for p in self.get_players():

            self.total_investments_1 = self.investment_new_1 + self.investment_old_1
    
            
            if self.total_investments_1 == 11 : #新規と既存が両方投資
                self.payoff_new_1 =  -222
                self.payoff_old_1 = 313
            elif self.total_investments_1 == 10: #新規のみ投資
                self.payoff_new_1 = -173
                self.payoff_old_1 = 218
            elif self.total_investments_1 == 1: #既存のみ投資
                self.payoff_new_1 = 0
                self.payoff_old_1 = 1167
            elif self.total_investments_1 == 0: #両方投資しない
                self.payoff_new_1 = 0
                self.payoff_old_1 = 250

            if p.id_in_group == 1 and self.round_number % 2 == 0 or p.id_in_group == 2 and  self.round_number % 2 == 1:
                p.payoff += self.payoff_new_1
            elif p.id_in_group == 2 and self.round_number % 2 == 0 or p.id_in_group == 1 and self.round_number % 2 == 1:
                p.payoff += self.payoff_old_1

#二期目のステージの拡大（=１)縮小(=２)を決める。
            if Subsession.stage_type == 1:
                if Subsession.random_vars_stage < 30 :
                    self.expansion_or_shrink = 1
                else:
                    self.expansion_or_shrink = 2
            elif Subsession.stage_type == 2:
                if Subsession.random_vars_stage < 50 :
                    self.expansion_or_shrink = 1
                else:
                    self.expansion_or_shrink = 2           
            elif Subsession.stage_type == 3:
                if Subsession.random_vars_stage < 70 :
                    self.expansion_or_shrink = 1
                else:
                    self.expansion_or_shrink = 2



#二期目の計算
    def compute_2(self):

        for p in self.get_players():
            if self.total_investments_1 == 11:
                self.total_investments_2 = self.investment_new_2_11_or_10 + self.investment_old_2_11_or_01
            elif self.total_investments_1 == 10:
                self.total_investments_2 = self.investment_old_2 + self.investment_new_2_11_or_10
            elif self.total_investments_1 == 1 :
                self.total_investments_2 = self.investment_new_2 + self.investment_old_2_11_or_01
            elif self.total_investments_1 == 0 :
                self.total_investments_2 = self.investment_new_2 + self.investment_old_2


            if self.subsession.stage_type == 1 : #拡大30％、縮小70％
                if self.subsession.expansion_or_shrink == 1 : #ステージ１の拡大の場合
                    if self.total_investments_1 == 11 : #新規と既存が両方投資
                        self.payoff_new_2 =  650
                        self.payoff_old_2 = 1574
                    elif self.total_investments_1 == 10: #新規のみ投資
                        if self.total_investments_2 == 3002: #12  #3000は片方が投資継続の場合、数値入力がないから3000を追加
                            self.payoff_new_2 = 650
                            self.payoff_old_2 = 907
                        elif self.total_investments_2 == 3000: #10
                            self.payoff_new_2 = 1115
                            self.payoff_old_2 = 98
                    elif self.total_investments_1 == 1: #既存のみ投資
                        if self.total_investments_2 == 3020: #21
                            self.payoff_new_2 = -17
                            self.payoff_old_2 = 1574
                        elif self.total_investments_2 == 3000: #01
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 4145
                    elif self.total_investments_1 == 0: #両方投資しない
                        if self.total_investments_2 == 22: #22
                            self.payoff_new_2 = -17
                            self.payoff_old_2 = 907
                        elif self.total_investments_2 == 20: #20
                            self.payoff_new_2 = 448
                            self.payoff_old_2 = 98
                        elif self.total_investments_2 == 2 :#02
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 3478
                        elif self.total_investments_2 == 0 : #00
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 250

                            
                elif self.subsession.expansion_or_shrink == 2 :#ステージ１の縮小の場合
                    if self.total_investments_1 == 11 : #新規と既存が両方投資
                        self.payoff_new_2 = 186
                        self.payoff_old_2 = 450
                    elif self.total_investments_1 == 10: #新規のみ投資
                        if self.total_investments_2 == 3002: #12  #3000は方法が投資継続の場合、数値入力がないから3000を追加
                            self.payoff_new_2 =186 
                            self.payoff_old_2 = 259
                        elif self.total_investments_2 == 3000: #10
                            self.payoff_new_2 = 319
                            self.payoff_old_2 = 98
                    elif self.total_investments_1 == 1: #既存のみ投資
                        if self.total_investments_2 == 3020: #21
                            self.payoff_new_2 = -5
                            self.payoff_old_2 = 450
                        elif self.total_investments_2 == 3000: #01
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 1184
                    elif self.total_investments_1 == 0: #両方投資しない
                        if self.total_investments_2 == 22: #22
                            self.payoff_new_2 = -5
                            self.payoff_old_2 = 259
                        elif self.total_investments_2 == 20: #20
                            self.payoff_new_2 = 128
                            self.payoff_old_2 = 98
                        elif self.total_investments_2 == 2 :#02
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 994
                        elif self.total_investments_2 ==0 : #00
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 250

            elif self.subsession.stage_type == 2 : #拡大50%,縮小50%

                if self.subsession.expansion_or_shrink == 1 :#ステージ2の拡大の場合
                    if self.total_investments_1 == 11 : #新規と既存が両方投資
                        self.payoff_new_2 = 488
                        self.payoff_old_2 = 1180
                    elif self.total_investments_1 == 10: #新規のみ投資
                        if self.total_investments_2 == 3002: #12  #3000は方法が投資継続の場合、数値入力がないから3000を追加
                            self.payoff_new_2 = 488
                            self.payoff_old_2 = 680
                        elif self.total_investments_2 == 3000: #10
                            self.payoff_new_2 = 836
                            self.payoff_old_2 = 98
                    elif self.total_investments_1 == 1: #既存のみ投資
                        if self.total_investments_2 == 3020: #21
                            self.payoff_new_2 = -12
                            self.payoff_old_2 = 1180
                        elif self.total_investments_2 == 3000: #01
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 3109
                    elif self.total_investments_1 == 0: #両方投資しない
                        if self.total_investments_2 == 22: #22
                            self.payoff_new_2 = -12
                            self.payoff_old_2 =  680
                        elif self.total_investments_2 == 20: #20
                            self.payoff_new_2 = 336
                            self.payoff_old_2 = 98
                        elif self.total_investments_2 == 2 :#02
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 2609
                        elif self.total_investments_2 ==0 : #00
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 250
    
                elif self.subsession.expansion_or_shrink == 2 :#ステージ2の縮小の場合
                    
                    if self.total_investments_1 == 11 : #新規と既存が両方投資
                        self.payoff_new_2 = 163
                        self.payoff_old_2 = 393
                    elif self.total_investments_1 == 10: #新規のみ投資
                        if self.total_investments_2 == 3002: #12  #3000は方法が投資継続の場合、数値入力がないから3000を追加
                            self.payoff_new_2 = 163
                            self.payoff_old_2 = 227
                        elif self.total_investments_2 == 3000: #10
                            self.payoff_new_2 = 279
                            self.payoff_old_2 = 98
                    elif self.total_investments_1 == 1: #既存のみ投資
                        if self.total_investments_2 == 3020: #21
                            self.payoff_new_2 = -4
                            self.payoff_old_2 = 393
                        elif self.total_investments_2 == 3000: #01
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 1036
                    elif self.total_investments_1 == 0: #両方投資しない
                        if self.total_investments_2 == 22: #22
                            self.payoff_new_2 = -4
                            self.payoff_old_2 = 227
                        elif self.total_investments_2 == 20: #20
                            self.payoff_new_2 = 112
                            self.payoff_old_2 = 98
                        elif self.total_investments_2 == 2 :#02
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 870
                        elif self.total_investments_2 ==0 : #00
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 250
                
            elif self.subsession.stage_type == 3 :#拡大70%、縮小30%

                if self.subsession.expansion_or_shrink == 1 :#ステージ3の拡大の場合
                    if self.total_investments_1 == 11 : #新規と既存が両方投資
                        self.payoff_new_2 = 390
                        self.payoff_old_2 = 944
                    elif self.total_investments_1 == 10: #新規のみ投資
                        if self.total_investments_2 == 3002: #12  #3000は方法が投資継続の場合、数値入力がないから3000を追加
                            self.payoff_new_2 =390 
                            self.payoff_old_2 = 544
                        elif self.total_investments_2 == 3000: #10
                            self.payoff_new_2 = 669
                            self.payoff_old_2 = 98
                    elif self.total_investments_1 == 1: #既存のみ投資
                        if self.total_investments_2 == 3020: #21
                            self.payoff_new_2 = -10
                            self.payoff_old_2 = 944
                        elif self.total_investments_2 == 3000: #01
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 2487
                    elif self.total_investments_1 == 0: #両方投資しない
                        if self.total_investments_2 == 22: #22
                            self.payoff_new_2 = -10
                            self.payoff_old_2 = 544
                        elif self.total_investments_2 == 20: #20
                            self.payoff_new_2 = 269
                            self.payoff_old_2 = 98
                        elif self.total_investments_2 == 2 :#02
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 2087
                        elif self.total_investments_2 ==0 : #00
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 250

                elif self.subsession.expansion_or_shrink == 2 :#ステージ3の縮小の場合
                    if self.total_investments_1 == 11 : #新規と既存が両方投資
                        self.payoff_new_2 = 173
                        self.payoff_old_2 = 419
                    elif self.total_investments_1 == 10: #新規のみ投資
                        if self.total_investments_2 == 3002: #12  #3000は方法が投資継続の場合、数値入力がないから3000を追加
                            self.payoff_new_2 = 173
                            self.payoff_old_2 = 242
                        elif self.total_investments_2 == 3000: #10
                            self.payoff_new_2 = 297
                            self.payoff_old_2 = 98
                    elif self.total_investments_1 == 1: #既存のみ投資
                        if self.total_investments_2 == 3020: #21
                            self.payoff_new_2 = -4
                            self.payoff_old_2 = 419
                        elif self.total_investments_2 == 3000: #01
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 1105
                    elif self.total_investments_1 == 0: #両方投資しない
                        if self.total_investments_2 == 22: #22
                            self.payoff_new_2 = -4
                            self.payoff_old_2 = 242
                        elif self.total_investments_2 == 20: #20
                            self.payoff_new_2 = 119
                            self.payoff_old_2 = 98
                        elif self.total_investments_2 == 2 :#02
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 927
                        elif self.total_investments_2 ==0 : #00
                            self.payoff_new_2 = 0
                            self.payoff_old_2 = 250
                


            self.payoff_new = self.payoff_new_1 + self.payoff_new_2
            self.payoff_old = self.payoff_old_1 + self.payoff_old_2

            if p.id_in_group == 1 and self.round_number % 2 == 0 or p.id_in_group == 2 and  self.round_number % 2 == 1:
                p.payoff += self.payoff_new_2
                p.investment_new_1 = self.investment_new_1 #実験結果の被験者の行動の確認用　個人のプレイヤークラスに情報を記録する
                p.investment_new_2 = self.investment_new_2
                p.investment_new_2_11_or_10 = self.investment_new_2_11_or_10
            elif p.id_in_group == 2 and self.round_number % 2 == 0 or p.id_in_group == 1 and self.round_number % 2 == 1:
                p.payoff += self.payoff_old_2
                p.investment_old_1 = self.investment_old_1 #実験結果の被験者の行動の確認用
                p.investment_old_2 = self.investment_old_2
                p.investment_old_2_11_or_01 = self.investment_old_2_11_or_01
            #既存企業のとき(没案)
'''         elif self.player.id_in_group == 2 and self.session.vars["role_random"] % 2 == 0 or self.player.id_in_group == 1 and self.session.vars["role_random"] % 2 == 1:

                if Constants.stage_type == 1 :
                    if self.total_investment_1 == 11 : #新規と既存が両方投資
                        p.payoff_old_1 = 79
                        p.payoff_old_2 = 157
                    elif self.total_investment_1 == 10: #新規のみ投資
                        p.payoff_old_1 = 10
                        if self.total_investments_2 == 2:#12
                            p.payoff_old_2 = 91
                        elif self.total_investments_2 == 0:#10
                            p.payoff_old_2 = 10
                    elif self.total_investment_1 == 1: #既存のみ投資
                        p.payoff_old_1 = 207
                        if self.total_investments_2 == 20: #21
                            p.payoff_old_2 = 157
                        elif self.total_investments_2 == 0: #01
                            p.payoff_old_2 = 415
                    elif self.total_investment_1 == 0: #両方投資しない
                        p.payoff_old_1 = 25
                        if self.total_investments_2 == 22: #22
                                p.payoff_old_2 = 91
                        elif self.total_investments_2 == 20 : #20
                                p.payoff_old_2 = 10
                        elif self.total_investments_2 == 2 : #02
                                p.payoff_old_2 = 348
                        elif self.total_investments_2 == 0 :#00
                                p.payoff_old_2 =25
                #elif stage_type == 2 :
                
                #elif stage_type == 3 :
'''


class Player(BasePlayer):
    user_id = models.StringField() #被験者IDの記録
    stage_type_random = models.IntegerField()

    investment_new_1 = models.IntegerField() 
    investment_new_2 = models.IntegerField()
    investment_new_2_11_or_10 = models.IntegerField()
    investment_old_1 = models.IntegerField()
    investment_old_2 = models.IntegerField()
    investment_old_2_11_or_01 = models.IntegerField()



    

    def other_player(self): #同じグループの相手のデータを得る
        return self.get_others_in_group()[0]

    def role(self): #グループ内番号が1のとき、新規参入企業
# ラウンド数が偶数のときはグループ内IDが1の人が新規参入企業
        if self.round_number % 2 == 0 : 
            if self.id_in_group == 1:
                return "新規参入企業"
            elif self.id_in_group == 2:
                return "既存企業"
        elif self.round_number % 2 == 1 :
            if self.id_in_group == 1:
                return "既存企業"
            elif self.id_in_group == 2:
                return "新規参入企業"




#リスク選好テスト用
    question_0 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [10,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal   
    )

    question_1 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [50,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal   
    )

    question_2 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [100,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal
    )
    
    question_3 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [150,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )
    question_4 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [200,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )

    question_5 = models.IntegerField(
        label = False,
        choices = [
            [5,"選択肢A"],
            [250,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )
    
    question_6 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [300,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )

    question_7 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [350,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )

    question_8 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [400,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )
    
    question_9 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [450,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )

    question_10 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [500,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )

    question_11 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [550,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )
    
    question_12 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [600,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )

    question_13 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [650,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )

    question_14 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [700,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )
    
    question_15 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [750,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )

    question_16 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [800,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )

    question_17 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [850,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )

    question_18 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [900,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )

    question_19 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [950,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )

    question_20 = models.IntegerField(
        label = False,
        choices = [
            [0,"選択肢A"],
            [1000,"選択肢B"],
            ],
        widget=widgets.RadioSelectHorizontal    
    )


#性格テスト用
    """
        利己的　100
        利他的　10
        競争的　1
    """
    type_personality = models.IntegerField()


    question_p_1 = models.IntegerField(
        label = "質問01",
        choices =[
            [1,"A　あなたが得るポイント：480　相手が得るポイント：80"],
            [100,"B　あなたが得るポイント：540　相手が得るポイント：280"],
            [10,"C　あなたが得るポイント：480　相手が得るポイント：480"],
            ],
        widget=widgets.RadioSelect
    )

    question_p_2 = models.IntegerField(
        label = "質問02",
        choices =[
            [100,"A　あなたが得るポイント：560　相手が得るポイント：300"],
            [10,"B　あなたが得るポイント：500　相手が得るポイント：500"],
            [1,"C　あなたが得るポイント：500　相手が得るポイント：100"],
            ],
        widget=widgets.RadioSelect
    )    
    
    question_p_3 = models.IntegerField(
        label = "質問03",
        choices =[
            [10,"A　あなたが得るポイント：520　相手が得るポイント：520"],
            [1,"B　あなたが得るポイント：520　相手が得るポイント：120"],
            [100,"C　あなたが得るポイント：580　相手が得るポイント：320"],
            ],
        widget=widgets.RadioSelect
    )    
    
    question_p_4 = models.IntegerField(
        label = "質問04",
        choices =[
            [1,"A　あなたが得るポイント：500　相手が得るポイント：100"],
            [100,"B　あなたが得るポイント：560　相手が得るポイント：300"],
            [10,"C　あなたが得るポイント：490　相手が得るポイント：490"],
            ],
        widget=widgets.RadioSelect
    )    
    
    question_p_5 = models.IntegerField(
        label = "質問05",
        choices =[
            [100,"A　あなたが得るポイント：560　相手が得るポイント：300"],
            [10,"B　あなたが得るポイント：500　相手が得るポイント：500"],
            [1,"C　あなたが得るポイント：490　相手が得るポイント：90"],
            ],
        widget=widgets.RadioSelect
    )    
    
    question_p_6 = models.IntegerField(
        label = "質問06",
        choices =[
            [10,"A　あなたが得るポイント：500　相手が得るポイント：500"],
            [100,"B　あなたが得るポイント：500　相手が得るポイント：100"],
            [1,"C　あなたが得るポイント：570　相手が得るポイント：300"],
            ],
        widget=widgets.RadioSelect
    )   
    
    question_p_7 = models.IntegerField(
        label = "質問07",
        choices =[
            [10,"A　あなたが得るポイント：510　相手が得るポイント：510"],
            [100,"B　あなたが得るポイント：560　相手が得るポイント：300"],
            [1,"C　あなたが得るポイント：510　相手が得るポイント：110"],
            ],
        widget=widgets.RadioSelect
    )   
    
    question_p_8 = models.IntegerField(
        label = "質問08",
        choices =[
            [100,"A　あなたが得るポイント：550　相手が得るポイント：300"],
            [1,"B　あなたが得るポイント：500　相手が得るポイント：100"],
            [10,"C　あなたが得るポイント：500　相手が得るポイント：500"],
            ],
        widget=widgets.RadioSelect
    )   
    
    question_p_9 = models.IntegerField(
        label = "質問09",
        choices =[
            [1,"A　あなたが得るポイント：480　相手が得るポイント：100"],
            [100,"B　あなたが得るポイント：490　相手が得るポイント：490"],
            [10,"C　あなたが得るポイント：540　相手が得るポイント：300"],
            ],
        widget=widgets.RadioSelect
    )