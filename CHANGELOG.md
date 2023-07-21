# CHANGELOG.md

File serves as history of step by step development approach

Good place for understanding codebase with little overwhelm

Needs verification of other contributors to see if accurate

Needs to be formatted according to changelog.md standards

Learn the CHANGELOG.md standards from Internet


## Phase 1 (can be quickly run on Colab)

#1 Extract text from PDF / PPT / DOC

#2 Filter non-aboves & stopwords

#3 Create a Reverse-Index[word]:

      Word | Appended Files it Occurs in
      
#4 Store the above table as SQLite DB

#5 View any search term from DB by query:

      cursor.execute("SELECT * FROM reverse_index WHERE word LIKE '%' || ? || '%'", (search_term,))


## Phase 2 (need to replace repo_path to your local path to repo)

#1 Broke down Notebook into multiple files

#2 Cleansed whitespaces, removed fillers and punctuations

#3 Added a Topic Extraction stored in filepath upto endpoint ie '/'

#4 Added Topic_Name col, 2 search patterns and insert function to DB

#5 Added Relevance col by Counter(filtered_words) ie freq of cleaned_word


## Phase 3 (Implemented a basic search)

#1 Added Absolute_Link_Creator to replace ' ' with '%20' (URL Enc)

#2 Added Search to db.py: SELECT * FROM table WHERE word is search_term displayed in order of decreasing Relevance

#3  Passing the search_query to search() with result stored in search_result

#4 search() works by splitting query into words, storing docs occurred in into results

#5 If multiple docs then they are intersected. Keys ie inv-ind gotten from source_dict ie our DB


## Main (Deployed on DynamoDB & considering S3 for frontend and improving performance before Lambda)

### Potential Next Steps (First 3 may be Essential while other may be Nice to Haves)

#1 Calculate relevance using TF*IDF instead of only TF (more accurate based on term-sig)

#2 Use Cos_Sim in Search Function (check to see if performance improved)

#3 Use Github Actions to trigger API then lambda to update index when new doc added (performance improvement)

#4 Improve UX by Phrase Queries (more accurate based on exact words order)

#5 Improve UX by Fuzzy Distance / Stem-Lemm (handle minor errors or variations in search term)
