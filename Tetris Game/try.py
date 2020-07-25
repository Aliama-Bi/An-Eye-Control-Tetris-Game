'''
@Author: your name
@Date: 2020-05-18 11:06:47
@LastEditTime: 2020-05-18 11:10:13
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /Tetris/try.py
'''
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
pandas2ri.activate()

readRDS = robjects.r['readRDS']
df = readRDS('/Users/doctor/Documents/GitHub/Eye-Movement-Game/Models/rf_model3.rds')
df = pandas2ri.ri2py(df)