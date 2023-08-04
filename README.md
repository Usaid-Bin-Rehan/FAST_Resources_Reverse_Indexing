# **FAST_Resources Reverse_Indexer**

# _Abstract_
Search Engine for [FAST-Resources](https://github.com/hassanzhd/FAST-Resources/tree/master), a repository of study materials, for user to enter keywords as text, to retrieve all files that contains them. 

# _Pipeline_

## 1. Extract (extract_text.py)
#### Using Python Libraries to extract text from respective file types (PDF/PPT/DOC)

## 2. Transform (process_words.py)
#### i. Using Regular Expressions library to clean trailing whitespaces from files and converting to Lower Case
#### ii. Using NLTK library predefined stopwords dictionary to identify any Stop Words
#### iii. Transforming into Cleansed Words after filtering Fillers (Stop Words / Punctuation / 3 Letter Words)

## 3. Load (main.py)
#### i. Initializing the FAST-Resources repository and SQLite database on Local machine
#### ii. Extracting text from file, skipping over any text-less files and Counting Term Frequency of Transformed
#### iii. Extracting Topic Name, that is, text in the file path before '/' endpoint
#### iv. Creating Absolute Link, that is, replacing whitespaces with '%20' to format as URL
#### v. Running the driver program to perform all the above for all the files present in FAST-Resources repository

## 4. Search (search.py)
#### i. Searching for the query (input) by splitting into words for using as index to fetch file paths in its row
#### ii. If only single file is found then its keys (file paths and Relevance score) is fetched from src dict (DB)
#### iii. If multiple files are found then their file paths are intersected into posting list before keys fetched

## 5. CICD (database.py --> AWS + GitHub-Actions)
#### i. Iniating SQLite database with text columns: Word, Topic, File and integer column: Relevance score
#### ii. Creating Index at runtime on Word column and initiating Search Pattern 1 that allows search with Topic
#### iii. Creating Index at runtime on Word column and initiating Search Pattern 2 that allows search without Topic
#### iv. Inserting the Word and its Topic, File Path, and Relevance score (TF in main.py for ordering search results)
#### v. Using S3 as front, DynamoDB over SQLite, and Actions to trigger Lambda API-Gateway when new file added

# _Contributions_

## _(1) IR Good-First Issues_

### 1. Resolve Processing Challenges
#### i. Tokenization (CURRENTLY USING)
##### a. Encoding
##### b. Stopwords
##### ii. Phrase Query (Positional Posting-List)
##### a. Biword-Index
##### b. Extended Biword-Index
##### c. Positional-Index
#### iii. Morphological Analysis
##### a. Stemming-Lemmatization
##### b. POS-Tagging
##### c. NER / Topic-Recognition

### 2. Constructions & Compressions for Mining
#### i. Constructions
##### a. Block-based
##### b. Single Pass-in
##### c. Distributed
#### ii. Compressions
##### a. Index
##### b. Dictionary
##### c. Posting-List
#### iii. Mining
##### a. Classification
##### b. Clustering
##### c. Recommender-System
##### d. Crawling & Linking

### 3. Benchmark Models
#### i. Boolean Retrieval (BoW ie Set Algebra)
##### a. Simple
##### b. Extended (Partial-Matching & Term-Weights to Rank)
##### c. Fuzzy-Set (Fuzzy Set Theory 
#### ii. AdHoc Retrieval (Inverted-Index & Posting-List Query w/ Prec & Recall)
#### iii. Tolerant-Retrieval (Tree / Hashmap Dictionary w/ WildCard & Spelling)
##### a. General
##### b. Kgram
##### c. Kgram-Overlap
##### d. Levesthein / Edit-Distance
#### iv. Vector-Space (CURRENTLY USING)
#### v. Probabilistic
##### a. Binary Independence
##### b. Probability Ranking Principle

## _(2) Data-Engineering Good-First Issues_
- Check Issues

## _(3) Security Good-First Issues_

# _Need to fix documentation below & Create separate Contributions Guidline file:_
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
