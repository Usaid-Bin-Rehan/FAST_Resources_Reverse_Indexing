# FAST_Resources Reverse_Indexer

# Purpose
To query "FAST_Resources" using text. 
A user should be able to search via keywords and retrieve list of documents that contain those keywords
[Fast Resources Link](https://github.com/hassanzhd/FAST-Resources/tree/master)
## Generate Reverse Index Flow
Iterate over all the documents and generate index to make searching possible
### Steps
1. Iterate over all the files (pdf, docx, pptx) `main.py`
2. Extract text `extract_text.py`
3. Remove **stopwords**, **punctuations**, anything that is not alpha-numeric `process_words.py`
4. Persist in sqlite table `database.py`

## Search Flow (In Progress)
A function that take search keywords as input and returns like of documents that contain those words

### Access Patterns
- Search by keyword(s)
- Search by keywords and Topic Name
### Steps
1. Example

# How can you contribute?

1. Fork repository
2. Git Clone [Fast Resources Link](https://github.com/hassanzhd/FAST-Resources/tree/master)
3. Replace ```self.repo_path = '/Users/jazib/Desktop/workrepo/FAST-Resources/'``` in `main.py` with absolute path to Fast Resources clone
4. Replace ```self.conn = sqlite3.connect('/Users/jazib/Desktop/workrepo/FAST_Resources_Reverse_Indexer/fast_zakhira.db')``` in `database.py` with any local directory
5. Push your changes
6. Create Merge Request

Replace 

```self.repo_path```