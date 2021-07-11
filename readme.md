# Project "News Analysis"

## Project plan (alpha)
Part 1 - getting the data:
* Crawl news data from __inform.kz__
* * Set up a crawler to fetch the data and store in DB - done
* * * For now, simply crawl the data in a single thread
* * * Write crawler in paraller (4 threads) - later
* * * Think about efficient I/O operation for storing the crawled data - later
* Set up PostgreSQL DB for storing the links and articles - done
* * Set up tables and build ORM using sqlalchemy - done

Part 2 - working over models:
* Run EDA, some ETL and build models. Candidate models:
* * Text Generation based on LSTM
* * Label prediction
* * Will see based on EDA
* Deploy the model locally
* * Set up the server for serving the service (or website)
* Write tests
* * First tests - done
* Write logs for crawler - done
* * Start working on logging - done

More on Part 2:


* Try different NLP approaches:
* * Why traditional approach - perform good enough in many tasks, less costly, combined with DL can give good results
* * Rule-based methods (traditional NLP)
* * Probabilistic modeling and machine learning (traditional NLP)
* * Deep Learning (modern approach)
* Text classification task
* * Prediction of tag
* * Prediction of sentiment
* Word sequences
* * POS tagging - incorporate into transformation using embeddings
* * Named entities - need to think
* * Semantic slot filling - we can use this for question transformation - [link](https://medium.com/koderunners/semantic-slot-filling-part-1-7982d786928e)
* Embeddings and topic models
* * Word embeddings
* * Sentence embeddings
* * Topic modeling
* Seq2Seq tasks
* * Fake data generation - maybe I should try using semantic retrieval for loss function
* * Machine translation

* Text normalization methods
* * Tokenization and lemmatization
* * Text into units by - BOW, TFIDF
* * Text into units by - word2vec, CNN for n-grams


* I was thinking a lot about where to start but couldn't come to specific decision. So I think it is better start with deduplication task (or retrieval of similar articles) based on __TF-IDF__. So, let's go ahead and start working on this shit.



The project will be run based on flask server. The server will act as a daemon for crawler fetching the web-data while computer is on.


## Crawler structure
* Crawler for the links
* Crawler of the articles

## `sqlacodegen` script
`sqlacodegen postgresql://biddy:12345@localhost/projectnews`

## Launching jupyter lab with hidden files on
`jupyter lab --ContentsManager.allow_hidden=True`
___

# Notes:

* URL encoding using `requests` library: - [link](https://2.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls)
* Python OOP best practices 2020 - [link](https://towardsdatascience.com/5-best-practices-for-professional-object-oriented-programming-in-python-20613e08baee)
* The try and except blocks are used to handle exceptions. The assert is used to ensure the conditions are compatible with the requirements of a function. - [link](https://towardsdatascience.com/practical-python-try-except-and-assert-7117355ccaab)
* Python’s assert statement is a debugging aid, not a mechanism for handling run-time errors. The goal of using assertions is to let developers find the likely root cause of a bug more quickly. An assertion error should never be raised unless there’s a bug in your program. - [link](https://medium.com/@jadhavmanoj/python-what-is-raise-and-assert-statement-c3908697bc62)
* Python style guide - [link](https://stackoverflow.com/questions/159720/what-is-the-naming-convention-in-python-for-variable-and-function-names)
* How to structure `Flask App` - [link](https://itnext.io/flask-project-structure-the-right-choice-to-start-4553740fad98)
* Guide to python packaging tool (for file `setup.py`) - [link](https://realpython.com/pipenv-guide/)
* Python relative path importing using `setup.py` - [link](https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder)
* Using SQLAlchemy with Flask, not Flask-SQLAlchemy - [link](https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4)
* Thread-local session SQLAlchemy - [link](https://docs.sqlalchemy.org/en/13/orm/contextual.html#unitofwork-contextual)
* SQLAlchemy session how-to - [link](https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-faq-whentocreate)
* SQLAlchemy different quering approaches - through explicit session object and through models - [link](https://stackoverflow.com/questions/12350807/whats-the-difference-between-model-query-and-session-querymodel-in-sqlalchemy/14553324#14553324)
* Scoped session vs local session - `This pattern allows disparate sections of the application to call upon a global scoped_session, so that all those areas may share the same session without the need to pass it explicitly. The Session we’ve established in our registry will remain, until we explicitly tell our registry to dispose of it, by calling scoped_session.remove()` - [link](https://docs.sqlalchemy.org/en/13/orm/contextual.html)
* Very interesting - basically, ORM operations should separate session and orm operations (doing ORM operations and then act upon session), but this way it is hard to catch any exception due, one way to handle this is to create a function separate for session operations, maybe later.
* TypeHinting and return type in case of error - what should I return with type hinting in case of exception with no case of raising exception?
* `logging` modular - [link](https://stackoverflow.com/questions/15727420/using-logging-in-multiple-modules), general tutorial on logging - [link](https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial)


# Logs

## 13-06-2021
* First test for retrieving links
* Custom test for retrieving articles
* Articles data structure will include links, date, title, and tags

## 15-06-2021
* Created ORM using sqlacodegen
* When parsing sometimes OSError is raised along with ConnectionError and ProtocolError
* * Should wrap the calls with try-except closure
* Implement corrrect way of making request using the same [session](https://docs.python-requests.org/en/master/user/advanced/) and maybe set up the [header values](https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/)

## 16-06-2021
* Did modification to test crawling script
* Need to implement logging in try-except closure

## 19-06-2021
* Modified crawler
* Formatted code

## 21-06-2021
* Testing ORM
* TO-DO: write ORM operations for testing
* NOTE: I don't if additional class for `Base` is implemented correctly. Some expert opinion would be helpful.

## 24-06-2021
* Writing ORM operations
* Got some ideas from Raushan on models
* * Tags retrieval based on NER extraction model from DeepPavlov
* * Article embeddings for finding similar (or identical) articles using some google shit
* * Fake article generation based on BERT-embeddings with attention

## 25-06-2021
* Fixed SQL query regarding the primary key set up - [link](https://stackoverflow.com/questions/64016778/better-to-use-serial-primary-key-or-generated-always-as-identity-for-primary-key)
* Next [link](https://www.postgresqltutorial.com/postgresql-identity-column/)
* ~~__TODO__~~: Couldn't find any instruction on how to implement identity (`generate as always`) column - [link](https://github.com/sqlalchemy/alembic/issues/775), thus temporarily using autoincrement -> Solved it by using self designed ORM including Identity feature, need expertise opinion on this
* ~~__TODO__~~: New identity column attribute works differently than expected, we can insert similar articles, need to debug.

## 26-06-2021
* Finally finished testing, now need to implement function that will flawlessly crawl the data and save to DB.

## 27-06-2021
* Function that will flawlessly crawl the website and save to DB is implemented (seemingly)
* Now need to leave the crawler active over night or day to crawl data for several years. Maybe should first test it for one year, we will see.

## 01-07-2021
* Still crawling, at the same time thinking on what kind of models I can deploy
* Also fixed the some bug in `get_url` function