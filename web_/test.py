from textblob import TextBlob

blob = TextBlob("Python is amazing. It can generate text. and what about me")
print(blob.sentences)
print(blob.words)
