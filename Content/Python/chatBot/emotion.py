import sys
from transformers import pipeline


classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)


def classify(txt_input):
    return classifier(txt_input)


emotions = ['abandonment', 'ableism', 'acceptance', 'acknowledgment', 'admiration', 'adoration', 'aesthetic appreciation', 'ageism', 'aggression', 'agitation', 'amusement', 'anger', 'anguish', 'anticipation', 'anxiety', 'apathy', 'appreciation', 'apprehensive', 'arousal', 'awe', 'awkwardness', 'belonging', 'bigotry', 'bitterness', 'bliss', 'boredom', 'calmness', 'caring', 'change', 'climate change', 'communication', 'community', 'compassion', 'confidence', 'confusion', 'connection', 'contentment', 'corruption', 'craving', 'curiosity', 'dazed', 'degradation', 'depression', 'desire', 'despair', 'determination', 'development', 'dignity', 'disappointment', 'discrimination', 'disgust', 'dislike', 'dread', 'ecstasy', 'elation', 'embarrassed', 'embarrassment', 'empathetic pain', 'empathy', 'enthusiasm', 'entrancement', 'envy', 'euphoria', 'euphoric', 'excitement', 'exclusion', 'extinction', 'faith', 'family', 'fear', 'forgiveness', 'friendship', 'frustration', 'generosity', 'genocide', 'giving', 'gratitude', 'greed', 'grief', 'growth', 'guilt', 'happiness', 'hate crimes', 'hatred', 'helplessness', 'homesickness', 'homophobia', 'hope', 'hopelessness', 'horror', 'hostility', 'humble', 'humiliation', 'injustice', 'interest', 'intolerance', 'irritation', 'isolation', 'jealousy', 'joy', 'kindness', 'learning', 'loneliness', 'longing', 'loss', 'love', 'marginalization', 'meaning', 'melancholy', 'mesmerized', 'misery', 'nostalgia', 'oppression', 'outrage', 'panic', 'passion', 'persecution', 'pity', 'pleasure', 'pollution', 'powerlessness', 'prejudice', 'pride', 'purpose', 'racism', 'rapture', 'receiving', 'regret', 'regretful', 'rejection', 'remorse', 'resentment', 'respect', 'romance', 'sadness', 'satisfaction', 'schadenfreude', 'self-confidence', 'self-consciousness', 'serenity', 'sexism', 'sexual desire', 'shame', 'sharing', 'sorrow', 'submission', 'suffering', 'surprise', 'sympathy', 'teaching', 'terror', 'terrorism', 'torment', 'transformation', 'transphobia', 'triumph', 'trust', 'unease', 'value', 'vengefulness', 'violence', 'war', 'worry', 'worth', 'xenophobia']


def main():
    text_input = sys.argv[1]
    emotions_scores = classify(text_input)
    for emotion_score in emotions_scores:
        print(emotion_score)


if __name__ == '__main__':
    main()


def test():
    pass
    # import nltk
    # from nltk import pos_tag_sents
    # from nltk.sentiment.vader import SentimentIntensityAnalyzer
    # from sklearn.cluster import KMeans
    # from sklearn.preprocessing import LabelEncoder
    # from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
    # nltk.download('vader_lexicon')
    # Compile a large corpus of text data
    # corpus = "I feel sad today. I am very sad. The sky is cloudy and it's raining. I don't want to go outside."

    # Use NLTK to extract features from the text data
    # sentences = nltk.sent_tokenize(corpus)
    # tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
    # tagged_tokens = pos_tag_sents(tokens)
    # sentiment_scores = SentimentIntensityAnalyzer().polarity_scores(corpus)

    # Use scikit-learn to apply unsupervised learning algorithms
    # encoder = LabelEncoder()
    # labels = [tag for sentence in tagged_tokens for word, tag in sentence]
    # encoded_labels = encoder.fit_transform(labels)

    # clustering_model = KMeans(n_clusters=2)
    # clustering_model.fit(encoded_labels.reshape(-1, 1))

    # Use NLTK and scikit-learn to analyze and interpret the emotional content of the text

    # Flatten the list of tagged tokens so that it can be used by the BigramCollocationFinder
    # flattened_tagged_tokens = [word_tag for sentence in tagged_tokens for word_tag in sentence]

    # Create a BigramCollocationFinder and find the 10 most likely bigram collocations
    # finder = BigramCollocationFinder.from_words([word for (word, tag) in flattened_tagged_tokens])
    # collocations = finder.nbest(BigramAssocMeasures.likelihood_ratio, 10)

    # Create a Concordance
    # concordance = nltk.ConcordanceIndex([word for (word, tag) in flattened_tagged_tokens])

    # Print the concordance for the word "sad"
    # concordance.print_concordance("sad")