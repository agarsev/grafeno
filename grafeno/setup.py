
def setup ():
    try:
        import nltk
        nltk.download(['wordnet', 'wordnet_ic'])
    except ImportError:
        pass

    try:
        from spacy.cli import download
        download('en')
    except ImportError:
        pass
