import nltk
from nltk.corpus import gutenberg
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import string
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize

nltk.download('gutenberg')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('vader_lexicon')



text = gutenberg.raw('melville-moby_dick.txt')


tokens = word_tokenize(text)
tokens = [token for token in tokens if token not in string.punctuation]
tokens = [token for token in tokens if token not in string.punctuation]
tokens = [token for token in tokens if not re.match(r"[-'`]|'s'\d", token)]



stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if not word.lower() in stop_words]


tagged_tokens = nltk.pos_tag(filtered_tokens)


freq_dist = FreqDist([tag[1] for tag in tagged_tokens])
top_pos_tags = freq_dist.most_common(5)

print("Top 5 POS tags and their frequencies:")
for tag, freq in top_pos_tags:
  print(tag, freq) 


lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens][:20]
print("\nLemmatized tokens:")
print(lemmatized_tokens)



freq_dist.pop(string.punctuation, None)
plt.bar(freq_dist.keys(), freq_dist.values())
plt.show()



sia = SentimentIntensityAnalyzer()
sentence = sent_tokenize(text)


score = 0
for s in sentence:
    score += sia.polarity_scores(s)['compound']
score = score / len(sentence)

if score > 0.05:
    overall_sentiment = 'positive'
elif score <= 0.05:
    overall_sentiment = 'negative'

print("Average Sentiment Score:", score)
print("Overall Text Sentiment:", overall_sentiment)