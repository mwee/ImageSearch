# ImageSearch
ImageSearch is an image scraper and search engine using [Clarifai](http://clarifai.com/)'s image recognition [APIs](https://developer.clarifai.com/).

The crawler is set up to crawl [National Geographic Photography](http://photography.nationalgeographic.com/photography/), though the base site can be changed in `imagespider/imagespider/settings.py`. With this seed, Natural Geographic-y search engine queries such as `safari`, `lake`, `water`, `mountain` will yield good results. Typical.

Keyword search is implemented according to relevance from the Clarifai API and returned in order of relevance. The inputs are keywords in the search box or as a query parameter called `keywords` to the `/search` endpoint.

### Setup
Make sure that `xcode-select update` has been run.

Install Python requirements with `pip install -r requirements.txt`

#### Crawling for images

Inside the `imagespider` directory, run `scrapy crawl image-spider -o items.json`
This will crawl [National Geographic Photography](http://photography.nationalgeographic.com/photography/) and save page urls and image urls to a file called `items.json`.

#### Setting up the Database

Create a Postgres database called `image_search_engine`. This can be done with:

    psql
    create database image_search_engine;

Now run the migrations on the database. Inside the `ImageSearch` directory, run: `python manage.py db upgrade`

#### Populating the engine

Next, we will pass the scraped image urls to Clarifai's API to tag and judge relevance. First, create a [Clarifai account](https://developer.clarifai.com/) and export your tokens:

    export CLARIFAI_APP_ID=<an_application_id_from_your_account>
    export CLARIFAI_APP_SECRET=<an_application_secret_from_your_account>

Inside the `ImageSearch` directory run `python get_tags.py`. This grabs the urls saved in `imagerspider/items.json` and passes them to Clarifai's API to yield tags and relevances from and persists them in the Postgres database.

#### Start the server

In the `ImageSearch` directory, run `python app.py`. The keyword search engine is available at `http://localhost:5000/`. An example query is `http://localhost:5000/search?keywords=safari` or `http://localhost:5000/search?keywords=mountain+lion`.

### Design
* There are two database tables: `Image` and `KeywordRelevance`. Image `has_many` KeywordRelevance, with a `foreign_key` stored on KeywordRelevance. This is better than a flat, normalized table as it reduces duplication and improves performance of queries.
* Scrapy starts at the `start_url` and follows links outward in a breadth-first search to a `DEPTH_LIMIT` depth (defined in `imagespider/settings.py`).

### Future Improvements
Because this project is an MVP built in a matter of hours, there are improvements to be made. Here are a few:

* __Tests__: Unit and integration tests are necessary before an application can go to production.
* __Improved Scraping__: Scraping can be improved. For example, duplicates can present due to the same image appearing more than once on a page, or on different pages. This can be mitigated by enforcing a uniqueness constraint on `image_url`s. A cool feature would also be to keep track of different image sizes and filter by image size.
* __Database Tables__: `Keyword` can be broken off into its own table where the `keyword` column is unique to improve performance. Relevance can hold the foreign key to `Keyword` in a `has_many` relationship. `Keyword` now has deduplication of keywords and Postgres can take advantage of an index on `Keyword`'s primary key.
* __Database Constraints__: Database constraints should be added to enforce data integrity before commiting, for example that `Image` and `KeywordRelevance`'s foreign keys are not `null`, which is a reasonable assertion in this case.
* __Database Sharding__: As this grows web scale, the database will need to be scaled up. Sharding is one way to do this, for example by keyword.
* __Caching__: A production system should take advantage of caching for performance, for example caching images for the most popular queries.
* __Parallelize requests__: To make crawling web scale, crawlers should be distributed across many machines and many threads.
* __Pagination__: Pagination of serialized JSON search results is necessary when the scope of results is the entire web.
