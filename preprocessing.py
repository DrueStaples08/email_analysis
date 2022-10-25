# from types import NoneType
import gensim.downloader as gapi
from gensim import models
from gensim.models import word2vec
from gensim.models.word2vec import Word2Vec
# nltk.download('stopwords')
import nltk
# nltk.download()
# nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np
import re 
from nltk.corpus import stopwords
# stopwords.words('english')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
from nltk.stem import *
from nltk.stem.porter import *
# from odem_career_embeddings import odem_skills
# from langdetect import detect
# from googletrans import Translator, constants
# from dbconnect import extract_id_skills
from email_data_analysis import extract_email

# Attribute 1: dataset scraped from ODEM Platform including all job titles and a string nested list of skills
# Attribute 2: Analogical Reasoning Corpuses of various sizes which can be used for comparison
class Analogy:
    def __init__(self, career_skills):
        self.career_skills = career_skills
        #self.g_model = gapi.load('glove-wiki-gigaword-100')
        # self.g_model = gapi.load('glove-wiki-gigaword-300')
        self.w2v_corpus = gapi.load('text8')
        # self.w2v_corpus = gapi.load('word2vec-google-news-300') #remove .wv attribute from model object
        #self.concept_net_numberbatch_model = gapi.load("conceptnet-numberbatch-17-06-300")
        #self.fast_text_model = gapi.load('fasttext-wiki-news-subwords-300')
        #self.gpt2_model = GPT2LMHeadModel.from_pretrained('gpt2')  

    # Returns the dataset - this function is used below to feed in the data
    # def return_skills(self):
    #     translator = Translator()
    #     if type(self.career_skills) == dict:
    #         for k,v in self.career_skills.items():
    #             corpus = ''.join(v)
    #             if detect(corpus) != 'en':
    #                 self.career_skills[k] = [f'''{translator.translate(corpus)}''']
    #     return self.career_skills


# This a Word2Vec Sub-Class used to preprocess the data and compute the word embeddings
class Word2VecAnalogy(Analogy):
    def __init__(self, career_skills):
        Analogy.__init__(self, career_skills)

    def word2vec_model(self):
        corpus = self.w2v_corpus
        model = Word2Vec(corpus, sg=1) #0 for cbow, 1 for skip-gram
        return model
    
    # Pre-process data - Use stemming and lemmatizing to gather the stem of the word and the context of the word
    def prep_data(self):
        count = 0
        # career_skills = self.return_skills()
        career_skills = self.career_skills
        # print(career_skills)
        career_results = {}
        if type(career_skills) == list:
            my_skills = career_skills
            career_skills = {}
            career_skills['Career Search'] = my_skills
        stemmer=PorterStemmer()
        lemmmatizer=WordNetLemmatizer()
        for keymails, emails in career_skills.items():
            for words in emails:
                data = re.sub('[^a-zA-Z]', ' ',' '.join(words))
                data = data.lower()
                data = data.split()
                data = [lemmmatizer.lemmatize(stemmer.stem(word.lower())) for word in data if not word in set(stopwords.words('english'))]
                # data = [stemmer.stem(word.lower()) for word in data if not word in set(stopwords.words('english'))]
                # data = [lemmmatizer.lemmatize(word.lower()) for word in data if not word in set(stopwords.words('english'))]
                # data = [word.lower() for word in data if not word in set(stopwords.words('english'))]
                # data = [word for word in data if word]
                data = ' '.join(data)
                career_results[count] = data.split()
                count += 1
        return career_results

    # Computes Word Embeddings
    def word_embeddings(self):
        model = self.word2vec_model()
        career_skills = self.prep_data()
        career_results = {}
        for k,v in career_skills.items():
            res = []
            for g in v:
                try:
                    x = model.wv[g]
                    res.append(x)
                except KeyError:
                    res.append(0)
            #         embedding_skills = np.add.reduce(res) / len(v)
            # career_results[k] = embedding_skills
            #     embedding_skills = np.add.reduce(res) / len(v)
            # career_results[k] = embedding_skills
            embedding_skills = np.add.reduce(res) / len(v)
            career_results[k] = embedding_skills
        return career_results



# if __name__ == '__main__':
#     # wa = Word2VecAnalogy(['Hello, world, this, a, test'])
#     # print(wa.word_embeddings())
#     ee = extract_email()
#     wa = Word2VecAnalogy(ee)
#     # print(wa.word_embeddings())
#     print(wa.prep_data())