def clean_text_tokenize(text_in):
    import re
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    ps = PorterStemmer()
    sw = stopwords.words('english')
    clean_text = re.sub('[^A-z]+', " ", text_in).lower().split()
    clean_text = [word for word in clean_text if word not in sw]
    clean_text = [ps.stem(word) for word in clean_text]
    return clean_text


def stem_text_tokenize(text_in):
    import re
    from nltk.corpus import stopwords
    sw = stopwords.words('english')
    clean_text = re.sub('[^A-z]+', " ", text_in).lower().split()
    clean_text = [word for word in clean_text if word not in sw]
    return clean_text
