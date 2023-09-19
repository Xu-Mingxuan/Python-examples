import nltk
from nltk.corpus import gutenberg
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import string

nltk.download('gutenberg')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

text = gutenberg.raw('melville-moby_dick.txt')


tokens = word_tokenize(text)
tokens = [token for token in tokens if token not in string.punctuation]

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



tags, frequencies = zip(*top_pos_tags)

plt.bar(tags, frequencies)
plt.xlabel('POS Tags')
plt.ylabel('Frequency')
plt.title('Frequency Distribution of POS Tags')
plt.show()