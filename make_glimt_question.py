from datetime import datetime

def make_glimt_question(row):
    return {'id': row.conid,
            'type': 'bins',
            'state': 'active',
            'dates': {'startDay': str(datetime.now())[0:10].replace('-',''),'endDay': row.lastTradeDate},
            'props': {'title': row.longDescription, 'shortTitle': row.shortDescription, 'details': ''},
            'kind': 'discrete',
            'bins': [{'props': {'title': 'Yes', 'ai_title': '', 'order': 0, 'color': ''},
                        'isActive': True,
                        'endDay': 0},
                    {'props': {'title': 'No', 'ai_title': '', 'order': 0, 'color': ''},
                        'isActive': True,
                        'endDay': 0}]}