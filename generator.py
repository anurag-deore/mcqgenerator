from summarizer import Summarizer
import pke
import string
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
from nltk.corpus import wordnet as wn
from pywsd.similarity import max_similarity as maxsim
import requests
import re
import random

def bert_summarizer(full_text):
    model = Summarizer()

    
    result = model(full_text, min_length = 60, max_length = 500, ratio = 0.4)
    summarized_text = ''.join(result)
    return full_text, summarized_text

def keyword_extractor(Full_Text, summarized_text):
    
    extractor = pke.unsupervised.MultipartiteRank()
    extractor.load_document(input = Full_Text)
    pos = {'PROPN'}
    stoplist = list(string.punctuation)
    stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
    stoplist += stopwords.words('english')
    extractor.candidate_selection(pos = pos, stoplist = stoplist)
    extractor.candidate_weighting(alpha=1.1, threshold=0.74, method='average')

    keyphrases = extractor.get_n_best(n=20)
    key_phrases = [i[0] for i in keyphrases]
    filtered_key_phrases = [keyword.lower() for keyword in key_phrases if keyword.lower() in summarized_text.lower()]
    return filtered_key_phrases

def sentence_mapper(summarized_text, filtered_key_phrases):
    sentences = sent_tokenize(summarized_text)
    sentences = [sentence.strip() for sentence in sentences if len(sentence) > 20]
    keyword_processor = KeywordProcessor()
    keyword_sentence_map = {}  

    for word in filtered_key_phrases:
        keyword_sentence_map[word] = []
        keyword_processor.add_keyword(word)  
    
    for sentence in sentences:
        keywords_found = keyword_processor.extract_keywords(sentence)  
        for key in keywords_found:
            keyword_sentence_map[key].append(sentence)    
    
    for key in keyword_sentence_map.keys():
        values = keyword_sentence_map[key]
        values = sorted(values, key = len, reverse = True)
        keyword_sentence_map[key] = values
    
    return keyword_sentence_map

def get_word_sense(sentence, keyword):
    keyword = keyword.lower()
    if len(keyword.split()) > 0:
        keyword = keyword.replace(" ", "_")
    
    synsets = wn.synsets(keyword, pos = wn.NOUN)
    if len(synsets) > 0:
        wup_similarity = maxsim(sentence, keyword, 'wup', pos = wn.NOUN)
        return wup_similarity
    else:
        return None

def get_distractors_wordnet(synset, word):
    distractors = []
    word = word.lower()
    orignal_word = word
    if len(word.split()) > 0:
        word = word.replace(" ", "_")
    hypernym = synset.hypernyms()
    if len(hypernym) == 0:
        return distractors
    for item in hypernym[0].hyponyms():

        name = item.lemmas()[0].name()
        if name == orignal_word:
            continue
        name = name.replace("_", " ")

        if name is not None and name not in distractors:
            distractors.append(name)
    
    return distractors

def get_distractors_conceptnet(word):
    word = word.lower()
    original_word = word

    if len(word.split()) > 0:
        word = word.replace(" ","_")
    distractor_list = [] 
    
    url = "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en/%s&limit=5"%(word,word)
    obj = requests.get(url).json()

    for edge in obj['edges']:
        link = edge['end']['term'] 

        url2 = "http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10"%(link,link)
        obj2 = requests.get(url2).json()
        for edge in obj2['edges']:
            word2 = edge['start']['label']
            if word2 not in distractor_list and original_word.lower() not in word2.lower():
                distractor_list.append(word2)
                   
    return distractor_list

def key_distractor_mapper(keyword_sentence_map):
    keyword_distractor_map = {}

    for keyword in keyword_sentence_map:
        if len(keyword_sentence_map[keyword]) > 0:
            wordSense = get_word_sense(keyword_sentence_map[keyword][0], keyword)
            if wordSense:
                distractors = get_distractors_wordnet(wordSense, keyword)
                if len(distractors) == 0:
                    distractors = get_distractors_conceptnet(keyword)
                if len(distractors) != 0:
                    keyword_distractor_map[keyword] = distractors
            else:
                distractors = get_distractors_conceptnet(keyword)
                if len(distractors) != 0:
                    keyword_distractor_map[keyword] = distractors
                else:
                    print(keyword)
    return keyword_distractor_map

def get_mcqs(keyword_distractor_map, keyword_sentence_map):
    mcqs = {}
    Ques_no = 1
    print(keyword_distractor_map, keyword_sentence_map)
    for answer in keyword_distractor_map:
        mcqs[Ques_no] = {'question':"", 'options':[], 'answer':''}
        sentence = keyword_sentence_map[answer][0]
        pattern = re.compile(answer, re.IGNORECASE)
        output = pattern.sub("________", sentence)
        print("{}) {}".format(Ques_no, output))
        
        '''Temp Dict'''
        mcqs[Ques_no]['question'] = output
        
        options = [answer.capitalize()] + keyword_distractor_map[answer]
        MCQ = options[:4]
        mcqs[Ques_no]['answer'] = answer.capitalize()
        random.shuffle(MCQ)
        option_label = ['A', 'B', 'C', 'D']

        for id, opt in enumerate(MCQ):
            mcqs[Ques_no]['options'].append(opt)
            # print("\t{}) {}".format(option_label[id], opt))
        print("LOL => {}".format(mcqs))

        Ques_no += 1
    print("LOL AGAIN => {}".format(mcqs))
    return mcqs



def mcq_generate(file_content):

    full_text, summarized_text = bert_summarizer(file_content)
    filtered_key_phrases = keyword_extractor(full_text, summarized_text)
    keyword_sentence_map = sentence_mapper(summarized_text, filtered_key_phrases)
    keyword_distractor_map = key_distractor_mapper(keyword_sentence_map)
    mcqs = get_mcqs(keyword_distractor_map, keyword_sentence_map)
    return full_text, summarized_text, mcqs