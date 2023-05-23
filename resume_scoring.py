import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
from nltk.corpus import wordnet
import os
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfpage import PDFPage
from io import StringIO
import pandas as pd
from thefuzz import fuzz
from thefuzz import process
import numpy as np


def predict_resume_scoring(job_title,skill,education,experience):
    
    database = pd.read_csv('database.csv')
    job_title = job_title.lower()
    skill = skill.lower()
    education = education.lower()
    database = database.set_index('file_name')
    database = database[database['job_title']==job_title]
    limit = len(database)
    
    education_match = process.extract(str(education),database['qualification'], limit= limit  , scorer=fuzz.token_set_ratio)
    edu_result_df = pd.DataFrame()
    for i in range(limit):

        education_score = education_match[i][1]
        file_name = education_match[i][2]
        match_df = pd.DataFrame([[file_name,education_score]],columns = ['file_name','education_score'])
        edu_result_df = pd.concat([edu_result_df,match_df])
    
    skill_match = process.extract(str(skill),database['professional_skill'], limit= limit  , scorer=fuzz.token_set_ratio)
    skill_result_df = pd.DataFrame()
    for i in range(limit):
        skill_score = skill_match[i][1]
        file_name = skill_match[i][2]
        match_df = pd.DataFrame([[file_name,skill_score]],columns = ['file_name','skill_score'])
        skill_result_df = pd.concat([skill_result_df,match_df])

            
    database = pd.merge(database,edu_result_df,how = 'left',on = 'file_name')
    database = pd.merge(database,skill_result_df,how = 'left',on = 'file_name')
    
    
    
    database['experience'] =database['experience'].astype('str')
    database['experience'] = database['experience'].str.replace('None','0')
    database['experience'] = database['experience'].astype('float')
    database['experience_score'] = np.where(database['experience']>=experience,100,np.where(np.logical_and(database['experience']>=experience-1,database['experience']<experience),50,0))
    
    database['Total_Score'] = (database['education_score'] + database['skill_score'] + database['experience_score'])/3
    database['Total_Score'] = np.round(database['Total_Score'])
    
    
    selected_resume = database[database['Total_Score']>= 70]
    selected_resume = selected_resume['file_name'].to_list()
    
    #print(selected_resume)
    
    return selected_resume