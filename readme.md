# Project "News Analysis" - Crawler

## Project plan (alpha)
Part 1 - getting the data:
* Crawl news data from __inform.kz__
* * Set up a crawler to fetch the data and store in DB - done
* * * For now, simply crawl the data in a single thread
* * * Write crawler in paraller (4 threads) - later
* * * Think about efficient I/O operation for storing the crawled data - later
* Set up PostgreSQL DB for storing the links and articles - done
* * Set up tables and build ORM using sqlalchemy - done


The project will be run based on flask server. The server will act as a daemon for crawler fetching the web-data while computer is on.


## Crawler structure
* Crawler for the links
* Crawler of the articles


# Notes:

* URL encoding using `requests` library: - [link](https://2.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls)
* The try and except blocks are used to handle exceptions. The assert is used to ensure the conditions are compatible with the requirements of a function. - [link](https://towardsdatascience.com/practical-python-try-except-and-assert-7117355ccaab)
* Python’s assert statement is a debugging aid, not a mechanism for handling run-time errors. The goal of using assertions is to let developers find the likely root cause of a bug more quickly. An assertion error should never be raised unless there’s a bug in your program. - [link](https://medium.com/@jadhavmanoj/python-what-is-raise-and-assert-statement-c3908697bc62)
* Using SQLAlchemy with Flask, not Flask-SQLAlchemy - [link](https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4)
* Thread-local session SQLAlchemy - [link](https://docs.sqlalchemy.org/en/13/orm/contextual.html#unitofwork-contextual)
* SQLAlchemy session how-to - [link](https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-faq-whentocreate)
* SQLAlchemy different quering approaches - through explicit session object and through models - [link](https://stackoverflow.com/questions/12350807/whats-the-difference-between-model-query-and-session-querymodel-in-sqlalchemy/14553324#14553324)
* Scoped session vs local session - `This pattern allows disparate sections of the application to call upon a global scoped_session, so that all those areas may share the same session without the need to pass it explicitly. The Session we’ve established in our registry will remain, until we explicitly tell our registry to dispose of it, by calling scoped_session.remove()` - [link](https://docs.sqlalchemy.org/en/13/orm/contextual.html)
* Very interesting - basically, ORM operations should separate session and orm operations (doing ORM operations and then act upon session), but this way it is hard to catch any exception due, one way to handle this is to create a function separate for session operations, maybe later.
* TypeHinting and return type in case of error - what should I return with type hinting in case of exception with no case of raising exception?
* `logging` modular - [link](https://stackoverflow.com/questions/15727420/using-logging-in-multiple-modules), general tutorial on logging - [link](https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial)