# **FAST_Resources Reverse_Indexer**

# _Abstract_
Search Engine for [FAST-Resources](https://github.com/hassanzhd/FAST-Resources/tree/master), a repository of study materials, for user to enter keywords as text, to retrieve all files that contains them. 

# _Pipeline_

## 1. Extract (extract_text.py)
### Used Python Libraries to extract text from respective file types (PDF/PPT/DOC)

## 2. Transform (process_words.py)
### i. Using Regular Expressions library to clean trailing whitespaces from files and converting to Lower Case
### ii. Using NLTK library predefined stopwords dictionary to identify any Stop Words
### iii. Transforming into Cleansed Words after filtering Fillers (Stop Words / Punctuation / 3 Letter Words)

## 3. Load (main.py)
### i. Initializing the FAST-Resources repository and SQLite database on Local machine
### ii. Extracting text from file, skipping over any text-less files and Counting Term Frequency of Transformed
### iii. Extracting Topic Name, that is, text in the file path before '/' endpoint
### iv. Creating Absolute Link, that is, replacing whitespaces with '%20' to format as URL
### v. Running the driver program to perform all the above for all the files present in FAST-Resources repository

## 4. Search (search.py)
### i. Searching for the query (input) by splitting into words for using as index to fetch file paths in its row
### ii. If only single file is found then its keys (file paths and Relevance score) is fetched from src dict (DB)
### iii. If multiple files are found then their file paths are intersected and the intersection's keys are fetched

## 5. CICD (database.py --> AWS + GitHub-Actions)
### i. Iniating SQLite database with text columns: Word, Topic, File and integer column: Relevance score
### ii. Creating Index at runtime on Word column and initiating Search Pattern 1 that allows search with Topic
### iii. Creating Index at runtime on Word column and initiating Search Pattern 2 that allows search without Topic
### iv. Inserting the Word and its Topic, File Path, and Relevance score (TF in main.py for ordering search results)
### v. Using S3 as front, DynamoDB over SQLite, and Actions to trigger Lambda API-Gateway when new file added




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
