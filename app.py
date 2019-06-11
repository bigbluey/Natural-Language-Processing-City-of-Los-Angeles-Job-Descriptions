import os, glob, sys
from flask import Flask, jsonify, render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import pandas as pd
import re
import textstat
from textstat.textstat import textstat
import nltk
# nltk.download('punkt')
import nltk.corpus
import string
import spacy
from spacy.matcher import PhraseMatcher
import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def main():
    all_files = os.listdir("data/Job Bulletins")
    all_files.sort()
    return jsonify(all_files)

@app.route("/terms-and-weights/<sample>")
def terms_and_weights(sample):
    sentences = list()
    file_path = f"data/Job Bulletins/{sample}"
    with open(file_path) as file:
        reading_score = textstat.flesch_reading_ease(file_path)
        reading_score_2 = textstat.dale_chall_readability_score(file_path)
        for line in file:
            for l in re.split(r"\.\s|\?\s|\!\s|\n",line):
                if l:
                    sentences.append(l)
    cvec = CountVectorizer(stop_words='english', min_df=3, max_df=0.5, ngram_range=(1,2))
    sf = cvec.fit_transform(sentences)
    transformer = TfidfTransformer()
    transformed_weights = transformer.fit_transform(sf)
    weights = np.asarray(transformed_weights.mean(axis=0)).ravel().tolist()
    weights_df = pd.DataFrame({'term': cvec.get_feature_names(), 'weight': weights})
    weights_df = weights_df.sort_values(by='weight', ascending=False).head(10)
    myList = {"term" : weights_df.term.tolist(), "weight" : weights_df.weight.tolist(), "scores" : [reading_score, reading_score_2]}
    file.close()
    return jsonify(myList)

@app.route("/readability")
def readability():    


    text = "I am some really difficult text to read because I use obnoxiously large words."
    test_data = ("data/Job Bulletins/ACCOUNTANT 1513 062218.txt")

    all_files = os.listdir("data/Job Bulletins")
    all_files.sort()

    counter = 0
    average = 0

    for file_name in all_files:
        test_data = file_name
        # print(test_data)

        test_data_name = f"data/Job Bulletins/{test_data}"
        # print(test_data_name)

        a = textstat.flesch_reading_ease(test_data_name)
        # counter += 1

        '''Score	Difficulty
        90-100	Very Easy
        80-89	Easy
        70-79	Fairly Easy
        60-69	Standard
        50-59	Fairly Difficult
        30-49	Difficult
        0-29	Very Confusing
        '''

        b = textstat.smog_index(test_data)
        c = textstat.flesch_kincaid_grade(test_data)
        d = textstat.coleman_liau_index(test_data)
        e = textstat.automated_readability_index(test_data)

        f = textstat.dale_chall_readability_score(test_data)
        '''Score	Understood by
        4.9 or lower	average 4th-grade student or lower
        5.0–5.9	average 5th or 6th-grade student
        6.0–6.9	average 7th or 8th-grade student
        7.0–7.9	average 9th or 10th-grade student
        8.0–8.9	average 11th or 12th-grade student
        9.0–9.9	average 13th to 15th-grade (college) student
        '''

        g = textstat.difficult_words(test_data)
        h = textstat.linsear_write_formula(test_data)
        i = textstat.gunning_fog(test_data)
        j = textstat.text_standard(test_data)
        k = textstat.syllable_count(text, lang='en_US')
        l = textstat.lexicon_count(text, removepunct=True)
        m = textstat.gunning_fog(text)
        n = textstat.text_standard(text, float_output=False)

        counter += a

    average = counter / 683

    # print(average)

    my_list = [a]

    return(jsonify(my_list))




@app.route("/readability_scores")
def scores():
    # Codecs Open
    # import codecs

    # # Open All Files in Directory
    # all_files = os.listdir("data/Job Bulletins")
    # all_contents = []

    # for files in all_files:
    #     if files.endswith(".txt"):
    #         f = codecs.open("data/Job Bulletins/" + str(files), "r", "utf-8")
    #         try:
    #             all_contents.append(f.read())
    #         except:
    #             all_contents.append("None")

    # from nltk.tokenize import word_tokenize

    # all_contents_str = str(all_contents)
    # # type(all_contents_str)

    # contents_tokens = word_tokenize(all_contents_str)
    # # print(contents_tokens)

    # from nltk.corpus import stopwords

    # stop = set(stopwords.words('english'))
    # contents_tokens_list1 = [ ]
    # for token in contents_tokens:
    #     if token not in stop:
    #         contents_tokens_list1.append(token)

    # punctuation = re.compile(r'[\\\n\$#-.?!,":;()|0-9|`/]')
    # contents_tokens_list2 = [ ]
    # for token in contents_tokens_list1:
    #     word = punctuation.sub("", token)
    #     if len(word)>0:
    #         contents_tokens_list2.append(word)

    # tokens_pos_tag = nltk.pos_tag(contents_tokens_list2)
    # pos_df = pd.DataFrame(tokens_pos_tag, columns = ('word','POS'))
    # pos_sum = pos_df.groupby('POS', as_index=False).count()
    # tagged = pos_sum.sort_values(['word'], ascending=[False])

    # filtered_pos = [ ]
    # for one in tokens_pos_tag:
    #     if one[1] == 'NN' or one[1] == 'NNS' or one[1] == 'NNP' or one[1] == 'NNPS':
    #         filtered_pos.append(one)

    # fdist_pos = nltk.FreqDist(filtered_pos)
    # top_100_words = fdist_pos.most_common(100)

    # top_words_df = pd.DataFrame(top_100_words, columns = ('pos','count'))
    # top_words_df['Word'] = top_words_df['pos'].apply(lambda x: x[0]) 
    # top_words_df = top_words_df.drop('pos', 1)

    # top_words_df = top_words_df.head(25)

    # my_list = {"count" : top_words_df["count"].tolist(), "word" : top_words_df.Word.tolist()}
    
    # # print(my_list)

    data = pd.read_csv("word_counts.csv") 

    data = data.head(25)

    my_list = {"count" : data["count"].tolist(), "word" : data.Word.tolist()}

    # print(data)

    return jsonify(my_list)

    # return("Done.")

@app.route("/analyze/<option>")
def analyze(option):
    # Create a files array to hold all of the file names in the folder
    files = []
    # Folder Path
    folder_path = "data/Job Bulletins"
    # Iterate through all of the files in the folder path
    counter = 0
    for filename in glob.glob(os.path.join(folder_path, '*.txt')):
        with open(filename, 'r') as f:
            # Throw exception for file names that are not usable
            try:
                files.append(filename)
                counter += 1
            except:
                files.append('None')
    files.sort()
    # print(f'Successfully retrieved {counter} files from folder.')

    # Create NLP pipeline
    nlp = spacy.load('en')

    # Model and languague data load and check
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe('ner')
    else:
        nlp.get_pipe('ner')

    # if option == 0:
    label = 'OUTSIDE'
    matcher = PhraseMatcher(nlp.vocab)
    for i in ["supervisory", "Safety",]:
        matcher.add(label, None, nlp(i))

    # Define the offest function to turn string indexes into item indexes 
    def offsetter(lbl, doc, matchitem):
        o_one = len(str(doc[0:matchitem[1]]))
        subdoc = doc[matchitem[1]:matchitem[2]]
        o_two = o_one + len(str(subdoc))
        return (o_one, o_two, lbl)

    # Warning ⚠️: Will take a while if used on every file, recommend 
    # using test_files for testing.
    # Create docs and entities to train the model with the labels created

    test_files = files[:10]
    # test_file = os.path.join('data/Job Bulletins/SENIOR SAFETY ENGINEER ELEVATORS 4264  042718.txt')

    res = []
    to_train_ents = []

    counter_2 = 0
    for file_name in test_files:
        if (file_name != 'None'):
            with open(f'{file_name}') as jb:
                counter_2 += 1
                line = True
                while line:
                    line = jb.readline()
                    mnlp_line = nlp(line)
                    matches = matcher(mnlp_line)
                    res = [offsetter(label, mnlp_line, x)
                        for x
                        in matches]
                    to_train_ents.append((line, 
                                        dict(entities=res), counter_2))

    docs = []
    for ent in to_train_ents:
        if (ent[1] != {'entities': []}):
            docs.append(ent[2])

    # Clean Data
    # Remove empty lines...
    for line in to_train_ents:
        if ([line[0]] == ['']):
            to_train_ents.remove(line)

    # Find Files
    job_names = []
    for i in range(len(files)):
        for doc in docs:
            if (i == doc - 1):
                # print(files[i])
                my_file = files[i]
                my_file = my_file[19:-4]
                job_names.append(my_file)

    return(jsonify(job_names))

if __name__ == "__main__":
    app.run()