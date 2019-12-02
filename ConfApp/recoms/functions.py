from gensim.models import Word2Vec
from gensim.similarities import WmdSimilarity
import re
from gensim import corpora
import spacy

additional_stopwords = ['abstract', 'introduction', 'keyword', 'method', 'result', 'discussion', 'conclusion',
                        'reference', 'et', 'al', 'journal', 'river', 'flow', 'paper', 'display', 'apply', 'find',
                        'description', 'information', 'characteristic', 'new', 'discuss', 'show', 'require', 'tensity',
                        'induce', 'form', 'reproduce', 'work', 'investigation', 'system', 'solution', 'carry', 'reveal',
                        'assume', 'similar', 'general', 'occur', 'associate', 'important', 'affect', 'quasi', 'know',
                        'discuss', 'influence', 'relation', 'account', 'direction', 'maximum', 'minimum', 'mainly',
                        'typically',
                        'plot', 'procedure', 'end', 'example', 'strength', 'increase', 'decrease', 'length', 'equal',
                        'remain', 'table', 'datum', 'several', 'total', 'main', 'feature', 'view', 'zero', 'wide',
                        'other',
                        'allow', 'provide', 'technique', 'observation', 'detail', 'determine', 'analysis', 'describe',
                        'expect', 'outer', 'perform', 'inside', 'include', 'current', 'purpose', 'propose',
                        'comparison', 'consider'
                        ]


p=r'C:\Users\Cyala\PycharmProjects\ConfApp4\Recommendation_branch\w2d\word2vec_v1.model'
model = Word2Vec.load(p)

def vocab2(vocabulary):
    '''
    :param vocabulary: vocab function result
    :return: return vocab function results without frequencies
    '''
    vocab_treated = vocab(vocabulary)
    result = [elt[0] for elt in vocab_treated if elt[0] in model.wv.vocab]
    return result

def vocab(vocabulary):
    '''
    Create a vocabulary from a list of kwords
    :param vocabulary: list of kwords
    :return: cleaned vocabulary
    '''
    replacements = {
        ' ': '_',
        '+': '',
        "-": '_',
        "1-D": "oned",
        "1D": "oned",
        'one-dimensional': "oned",
        "2-D": "twod",
        "2D": "twod",
        "two-dimensional": 'twod',
        "3-D": "threed",
        "3D": "threed",
        "three-dimensional": "threed"

    }

    # Remove the "-" at the end of lines + replacing 1D/2D/3D with oneD/twoD/threeD
    txt = [multiple_replace(replacements, elt) for elt in vocabulary]

    nlp = spacy.load('en_core_web_sm')
    clean1 = [sentence.lower() for sentence in txt]
    clean2 = [cleaning2(sent) for sent in nlp.pipe(clean1)]

    # We look for the bag of words & frequency for each word
    texts = [text.split() for text in clean2]
    bow = [elt for tx in texts for elt in tx]
    dictionary = corpora.Dictionary()
    mycorpus = dictionary.doc2bow(bow, allow_update=True)
    word_counts = [(dictionary[elt[0]], elt[1]) for elt in mycorpus]

    return word_counts

def multiple_replace(dictt, text):
    '''
    :param dictt: dictionary of elements and their replacement
    :param text: text to be treated
    :return: texted replaced with elements from dictt
    '''
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dictt.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dictt[mo.string[mo.start():mo.end()]], text)

def cleaning2(content_page):
    txt = [token.lemma_ for token in content_page if not token.is_stop]
    txt = [elt for elt in txt if elt not in additional_stopwords]
    txt = [elt for elt in txt if len(elt) > 3]
    return ' '.join(txt)

def remove9(list_):
    list2 = [elt for elt in list_ if elt != '9']
    return list2