import nltk
from nltk.corpus import movie_reviews
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy as nltk_accuracy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random

# Ensure you have the necessary NLTK data files
nltk.download('movie_reviews')
nltk.download('stopwords')
nltk.download('punkt')

# Load the movie reviews dataset
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

# Shuffle the documents to ensure randomness
random.shuffle(documents)

# Split the dataset into training and testing sets
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)[:2000]

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

# Create feature sets
featuresets = [(document_features(d), c) for (d, c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]

# Train the Naive Bayes classifier
classifier = NaiveBayesClassifier.train(train_set)

# Evaluate the classifier
print("Accuracy:", nltk_accuracy(classifier, test_set))

# Show the most informative features
classifier.show_most_informative_features(10)

# Function to classify a new review
def classify_review(review):
    features = document_features(word_tokenize(review))
    return classifier.classify(features)

# Example reviews
positive_review = "This movie was fantastic! The acting was superb and the plot was engaging."
negative_review = "I did not enjoy this movie. The acting was poor and the story was boring."

print("Classification of positive review:", classify_review(positive_review))
print("Classification of negative review:", classify_review(negative_review))

# You can test the classifier with your own reviews
user_review = input("Enter a movie review: ")
print("Classification of user review:", classify_review(user_review))
