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


## Add_Lambda_Code




## Main (Created λ for Backend Search & Terraform provisioned S3 for Frontend Static-Assets / FAST-Resources)

Terraform, used for IaC, allows automated & reusable provisioning (CRUD) of infra (containers / cloud), using YML,
a declarative and non-compiling, to replace error-prone & manual set-up of resources, similar to running a program

(1) Set up provider (AWS) in main.tf
(2) Create var, to store profile, bucket, document and base directory names, for reusability instead of hardcode
(3) Create tfvars file to initialize those variables with the actual names of our AWS services and run-time values
(4) Automatically generated lock.hcl file that stores version of AWS for compatibility considerations
(5) tfstate and tfstate.backup to keep log of resources provisioned for ability to revert to an instance

1. terraform init  # project is currently using IaC only for S3 not DDB nor Lambda
2. terraform plan  # generates execution plan displaying changes being made to infra
3. terraform apply # apply those changes based on config in main.tf and tfvars

#1 Created a reusable module static_files to manage static files
#2 Its source is set as templates from HashiCorp's predefined directory with variable base directory
#3 Resource is created for S3 object to store static files
#4 Loop is created to execute resource block for each file in the file variable
#5 Base dir is removed & source relative path is made absolute when files are made as keys of S3 bucket w/ checksum


# 
