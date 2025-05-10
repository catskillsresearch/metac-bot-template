#!/usr/bin/env python
# coding: utf-8

# # Base forecaster against open questions -- test community forecast alignment

# ## Imports

# In[1]:


from forecasting_tools import MetaculusApi, ApiFilter
from datetime import datetime, timedelta
import asyncio, os
import numpy as np
from predict import predict


# In[2]:


from load_secrets import load_secrets
load_secrets()


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


# In[4]:


from tqdm import tqdm
tqdm.pandas()


# ## Question sample

# In[5]:


num_of_questions_to_return = 42


# In[6]:


one_year_from_now = datetime.now() + timedelta(days=365)
api_filter = ApiFilter(
    allowed_statuses=["open"],
    num_forecasters_gte=40,
    scheduled_resolve_time_lt=one_year_from_now,
    includes_bots_in_aggregates=False,
)


# In[7]:


questions = asyncio.run(MetaculusApi.get_questions_matching_filter(
        api_filter,
        num_questions=num_of_questions_to_return,
        randomly_sample=True))


# In[8]:


question_binary = [question for question in questions if question.api_json['question']['type'] == 'binary'][0]


# In[9]:


question_multiple_choice = [question for question in questions if question.api_json['question']['type'] == 'multiple_choice'][0]


# In[10]:


question_numeric = [question for question in questions if question.api_json['question']['type'] == 'numeric'][0]


# ## Community forecast

# In[11]:


from community_forecast import *


# ### Numeric

# In[12]:


community_forecast_numeric(question_numeric)


# ### Binary

# In[13]:


community_forecast_binary(question_binary)


# ### Multiple choice

# In[14]:


community_forecast_multiple_choice(question_multiple_choice)


# ## All

# In[15]:


id_to_forecast = {question.api_json['id']: community_forecast(question) for question in questions}


# In[16]:


id_to_forecast


# ## Forecast the questions

# In[17]:


from flatten_dict import flatten_dict
import pandas as pd
from prompt_question import prompt_question
pd.set_option('display.max_columns', None)


# In[18]:


qflat = [flatten_dict(q.api_json, sep='_') for q in questions]


# In[99]:


df = pd.DataFrame(qflat)


# In[119]:


df.iloc[26]


# In[100]:


df['crowd'] = df.apply(lambda row: id_to_forecast[row.id], axis=1)


# In[101]:


df['question_options'] = df['question_options'].apply(repr)


# In[102]:


df = df[['id',
 'open_time',
 'scheduled_resolve_time',
 'title',
 'question_description',
 'question_resolution_criteria',
 'question_fine_print',
 'question_type',
 'question_options',
 'question_group_variable',
 'question_question_weight',
 'question_unit',
 'question_open_upper_bound',
 'question_open_lower_bound',
 'question_scaling_range_max',
 'question_scaling_range_min',
 'crowd']]


# In[103]:


dfn = 'forecast_community'
os.makedirs(dfn, exist_ok=True)


# In[104]:


df['today'] = datetime.now().strftime("%Y-%m-%d")


# In[105]:


from ResearchProModule import ResearchProModule


# In[106]:


bot = ResearchProModule()
bot.process_dataframe(df)


# In[107]:


from load_research import load_research


# In[108]:


df['research'] = df.apply(load_research, axis=1)


# In[109]:


df['prompt'] = df.apply(prompt_question, axis=1)


# In[110]:


df[df.question_type == 'multiple_choice']


# In[111]:


df['forecast'] = df.progress_apply(lambda question: predict(dfn, question), axis=1)


# In[114]:


from extract_forecast import extract_forecast


# In[115]:


df['prediction'] = df.apply(extract_forecast, axis=1)


# ## Compare crowd and forecast

# In[116]:


from error import error


# ## Assess performance

# In[129]:


df = df[~df.crowd.apply(lambda x: x is None)].copy()


# In[130]:


df['error'] = df.apply(error, axis=1)


# In[131]:


df


# In[136]:


plt.hist(df.error.values);


# In[139]:


df.to_json('community_results.json', indent=4)


# In[141]:


df1 = df[['title', 'question_type', 'prediction', 'crowd', 'error']]


# In[142]:


df1


# In[144]:


df1.to_csv('community.csv')


# https://www.perplexity.ai/search/here-are-some-questions-a-ques-fgZ1.vMOS1Sa.rOC1G3b7w

# In[ ]:




