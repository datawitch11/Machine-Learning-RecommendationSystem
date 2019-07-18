#!/usr/bin/env python
# coding: utf-8

# In[180]:


import pandas as pd
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# __read movie dataset__

# In[181]:


movies_df = pd.read_csv('movies_metadata.csv') 
movies_df.head()


# __read ratings dataset__

# In[182]:


ratings_df = pd.read_csv('ratings_small.csv')
ratings_df.head()


# In[183]:


movies_df.columns


# In[184]:


mdsub=movies_df.filter(['original_title','id','genres'])


# In[185]:


mdsub=mdsub.rename(columns = {'id':'movieid','original_title':'title'})
mdsub.head()


# In[186]:


from ast import literal_eval

mdsub['genres'] = mdsub['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])


# In[187]:


mdsub.head()


# In[188]:


#Copying the movie dataframe into a new one since we won't need to use the genre information in our first case.
moviesWithGenres_df = mdsub.copy()

#For every row in the dataframe, iterate through the list of genres and place a 1 into the corresponding column
for index, row in mdsub.iterrows():
    for genre in row['genres']:
        moviesWithGenres_df.at[index, genre] = 1
#Filling in the NaN values with 0 to show that a movie doesn't have that column's genre
moviesWithGenres_df = moviesWithGenres_df.fillna(0)
moviesWithGenres_df.head()


# In[189]:


ratings_df.head()


# In[190]:


#Drop removes a specified row or column from a dataframe
ratings_df = ratings_df.drop('timestamp', 1)
ratings_df.head()


# <a id="ref3"></a>
# # Content-Based recommendation system

# In[191]:


userInput = [
            {'title':'Waiting to Exhale', 'rating':5},
            {'title':'Toy Story', 'rating':3.5},
            {'title':'Jumanji', 'rating':2},
            {'title':"Pulp Fiction", 'rating':5},
            {'title':'Akira', 'rating':4.5}
         ] 
inputMovies = pd.DataFrame(userInput)
inputMovies


# In[192]:


#Filtering out the movies by title
inputId = mdsub[mdsub['title'].isin(inputMovies['title'].tolist())]
#Then merging it so we can get the movieId. It's implicitly merging it by title.
inputMovies = pd.merge(inputId, inputMovies)
#Dropping information we won't use from the input dataframe
inputMovies.head()


# In[193]:


im = inputMovies.drop('genres', 1)
im.head()


# In[194]:


#Filtering out the movies from the input
userMovies = moviesWithGenres_df[moviesWithGenres_df['movieid'].isin(inputMovies['movieid'].tolist())]
userMovies


# In[195]:


#Resetting the index to avoid future issues
userMovies = userMovies.reset_index(drop=True)
#Dropping unnecessary issues due to save memory and to avoid issues
userGenreTable = userMovies.drop('movieid', 1).drop('title', 1).drop('genres', 1)
userGenreTable


# In[196]:


inputMovies['rating']


# In[197]:


#Dot produt to get weights
userProfile = userGenreTable.transpose().dot(inputMovies['rating'])
#The user profile
userProfile


# In[198]:


#Now let's get the genres of every movie in our original dataframe
genreTable = moviesWithGenres_df.set_index(moviesWithGenres_df['movieid'])
#And drop the unnecessary information
genreTable = genreTable.drop('movieid', 1).drop('title', 1).drop('genres', 1)


# In[199]:


genreTable.shape


# In[200]:


#Multiply the genres by the weights and then take the weighted average
recommendationTable_df = ((genreTable*userProfile).sum(axis=1))/(userProfile.sum())
recommendationTable_df.head()


# In[201]:


#Sort our recommendations in descending order
recommendationTable_df = recommendationTable_df.sort_values(ascending=False)
#Just a peek at the values
recommendationTable_df.head()


# In[223]:


#The final recommendation table
mdsub.loc[mdsub['movieid'].isin(recommendationTable_df.head(20).keys())]


# In[266]:


import tkinter as tk 
from tkinter import *


root= tk.Tk() 
 
canvas1 = tk.Canvas(root, width = 1200, height = 450)
canvas1.pack()

var1 = tk.StringVar()
var2 = tk.StringVar()
var3 = tk.StringVar()





# New label and input box
label1 = tk.Label(root, text='first favorite movie title: ')
canvas1.create_window(100, 100, window=label1)

entry1 = tk.Entry(root,textvariable=var1) # create 1st entry box
canvas1.create_window(270, 100, window=entry1)

label2 = tk.Label(root, text='your rating: ')
canvas1.create_window(100, 120, window=label2)

entry2 = tk.Entry(root) # create 1st entry box
canvas1.create_window(270, 120, window=entry2)

# New label and input box
label3 = tk.Label(root, text='second favorite movie title: ')
canvas1.create_window(90, 140, window=label3)

entry3 = tk.Entry (root,textvariable=var2) # create 2nd entry box
canvas1.create_window(270, 140, window=entry3)

label4 = tk.Label(root, text='your rating: ')
canvas1.create_window(100, 160, window=label4)

entry4 = tk.Entry (root) # create 2nd entry box
canvas1.create_window(270, 160, window=entry4)

# New label and input box
label5 = tk.Label(root, text='third favorite movie title: ')
canvas1.create_window(100, 180, window=label5)

entry5 = tk.Entry (root,textvariable=var3) # create 2nd entry box
canvas1.create_window(270, 180, window=entry5)

label6 = tk.Label(root, text='your rating: ')
canvas1.create_window(90, 200, window=label6)

entry6 = tk.Entry (root) # create 2nd entry box
canvas1.create_window(270, 200, window=entry6)

def values(): 
    global first_fav #our 1st input variable
    first_fav = str(entry1.get())
    global first_rate #our 1st input variable
    first_rate = float(entry2.get()) 
    global second_fav #our 2nd input variable
    second_fav = str(entry3.get())
    global second_rate #our 2nd input variable
    second_rate = float(entry4.get()) 
    global third_fav #our 3rd input variable
    third_fav = str(entry5.get())
    global third_rate #our 3rd input variable
    third_rate = float(entry6.get())
    userInputtest = [
            {'title':first_fav, 'rating': first_rate },
            {'title':second_fav, 'rating': second_rate },
            {'title':third_fav, 'rating': third_rate }] 
    
    inputMoviestest = pd.DataFrame(userInputtest)

    inputIdtest = mdsub[mdsub['title'].isin(inputMoviestest['title'].tolist())]
    inputMoviestest = pd.merge(inputIdtest, inputMoviestest)
    inputMoviestest=inputMoviestest.drop('genres', 1)
    
    userMoviestest = moviesWithGenres_df[moviesWithGenres_df['movieid'].isin(inputMoviestest['movieid'].tolist())]

    userMoviestest = userMoviestest.reset_index(drop=True)
   # Dropping unnecessary issues due to save memory and to avoid issues
    userGenreTabletest = userMoviestest.drop('movieid', 1).drop('title', 1).drop('genres', 1)
    
    userProfiletest = userGenreTabletest.transpose().dot(inputMoviestest['rating'])
    recommendationTabletest_df = ((genreTable*userProfiletest).sum(axis=1))/(userProfiletest.sum())
    recommendationTabletest_df = recommendationTabletest_df.sort_values(ascending=False)

                         
    Prediction_result  = (mdsub.loc[mdsub['movieid'].isin(recommendationTabletest_df.head(20).keys())])
    label_Prediction = tk.Label(root, text= Prediction_result, bg='orange')
    canvas1.create_window(700, 400, window=label_Prediction)
    
button1 = tk.Button (root, text='Recommendations for you:',command=values, bg='orange') # button to call the 'values' command above 
canvas1.create_window(270, 250, window=button1)

root.mainloop()


# In[262]:


import gc
gc.collect()


# <hr>
# 
# <a id="ref3"></a>
# # Collaborative Filtering

# In[291]:


#Filtering out users that have watched movies that the input has watched and storing it
userSubset = ratings_df[ratings_df['movieId'].isin(inputMovies['movieid'].tolist())]
userSubset


# In[273]:


#Groupby creates several sub dataframes where they all have the same value in the column specified as the parameter
userSubsetGroup = userSubset.groupby(['userId'])


# In[290]:


#Sorting it so users with movie most in common with the input will have priority
userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)


# In[275]:


userSubsetGroup[0:3]


# In[276]:


ratings_df


# In[289]:


userSubsetGroup = userSubsetGroup[0:100]
userSubsetGroup.userId.unique()


# In[285]:


#Store the Pearson Correlation in a dictionary, where the key is the user Id and the value is the coefficient
pearsonCorrelationDict = {}

#For every user group in our subset
for name, group in userSubsetGroup:
    #Let's start by sorting the input and current user group so the values aren't mixed up later on
    group = group.sort_values(by='movieId')
    inputMovies = inputMovies.sort_values(by='movieid')
    #Get the N for the formula
    nRatings = len(group)
    #Get the review scores for the movies that they both have in common
    temp_df = inputMovies[inputMovies['movieid'].isin(group['movieId'].tolist())]
    #And then store them in a temporary buffer variable in a list format to facilitate future calculations
    tempRatingList = temp_df['rating'].tolist()
    #Let's also put the current user group reviews in a list format
    tempGroupList = group['rating'].tolist()
    #Now let's calculate the pearson correlation between two users, so called, x and y
    Sxx = sum([i**2 for i in tempRatingList]) - pow(sum(tempRatingList),2)/float(nRatings)
    Syy = sum([i**2 for i in tempGroupList]) - pow(sum(tempGroupList),2)/float(nRatings)
    Sxy = sum( i*j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList)*sum(tempGroupList)/float(nRatings)
    
    #If the denominator is different than zero, then divide, else, 0 correlation.
    if Sxx != 0 and Syy != 0:
        pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
    else:
        pearsonCorrelationDict[name] = 0


# In[281]:


pearsonCorrelationDict.items()


# In[282]:


pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')
pearsonDF.columns = ['similarityIndex']
pearsonDF['userId'] = pearsonDF.index
pearsonDF.index = range(len(pearsonDF))
pearsonDF.head()


# In[ ]:




