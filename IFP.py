import sqlite3, os, json
from datetime import datetime
from metaculus import post_question_prediction, post_question_comment, get_question_details, list_questions
from config import config

class IFP:

    forecast_fields = ['id',
                       'title',
                       'feedback',
                       'resolution_criteria', 
                       'background', 
                       'event', 
                       'model_domain']

    forecast_format = f"|{'|'.join(forecast_fields)}|"

    openai_max_tokens = 30000

    def format(self):
        rec = vars(self)
        fmt = '|'.join([f"{x}: {rec[x]}" for x in self.forecast_fields])
        return '|' + fmt + '|'

    def over_openai_max(self):
        sep = self.format()
        return len(sep.split(' ')) > self.openai_max_tokens # Max limit for OpenAI

    def __init__(self, id):
        self.root = f'{config.project}/forecasts'
        os.makedirs(self.root, exist_ok=True)
        self.id = id
        self.event = ''
        self.model_domain = ''
        self.feedback = ''
        self.critic_concurs = False
        self.question_details = get_question_details(self.id)
        if self.question_details['question']['type'] == 'binary':
            self.question_details['categories'] = ['Yes']
        self.today = datetime.now().strftime("%Y-%m-%d")   
        self.title = self.question_details["title"]
        self.published_at = self.question_details['published_at']
        self.resolution_criteria = self.question_details['question']['resolution_criteria']
        self.background = self.question_details["description"]
        self.fine_print = self.question_details['question']["fine_print"]
        self.resolution = self.question_details['question']["resolution"]

    def report(self):
        rpt = f"""
The future event is described by this question: [ {self.title} ]
The resolution criteria are: [ {self.resolution_criteria} ]
The background is: [ {self.background} ]"""
        if self.fine_print:
            rpt += f"""
The fine print is: [ {self.fine_print} ]"""
        return rpt

    def save(self):
        fn = f'{self.root}/{self.id}.json'
        payload = vars(self)
        with open(fn, 'w') as f:
            json.dump(payload, f, indent=4)
            print('saved', fn)

    def upload(self):
        self.save()
        post_question_prediction(self.id, self.forecast)
        post_question_comment(self.id, self.biggy)
