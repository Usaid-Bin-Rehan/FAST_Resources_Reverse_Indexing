# FAST_Resources Reverse_Indexer

# Purpose
To query "FAST_Resources" using text. 
A user should be able to search via keywords and retrieve list of documents that contain those keywords

## Generate Reverse Index Flow
Iterate over all the documents and generate index to make searching possible
### Steps
1. Iterate over all the files (pdf, docx, pptx) `main.py`
2. Extract text `extract_text.py`
3. Remove **stopwords**, **punctuations**, anything that is not alpha-numeric `process_words.py`
4. Persist in sqlite table `database.py`

## Search Flow (In Progress)
A function that take search keywords as input and returns like of documents that contain those words
### Steps
1. Example

# How can you contribute?

1. Fork repository 
2. Push your changes
3. Create Merge Request

