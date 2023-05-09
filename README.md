# CeneoScraper

### CSS selectors of the components of all opinions in [Ceneo.pl](https://www.ceneo.pl/) service

|Components|Variable/Dictionary key|Data type|Selector|
| :- | :- | :- | :- |
|opinion|opinion/single\_opinion|Tag, dictionary|div.js\_product-review|
|opinion ID|opinion\_id|string|["data-entry-id"]|
|opinion’s author|author|string|span.user-post\_\_author-name|
|author’s recommendation|recommendation|bool|span.user-post\_\_author-recomendation > em|
|score expressed in number of stars|score|float|span.user-post\_\_score-count|
|opinion’s content|description|string|div.user-post\_\_text|
|list of product advantages|pros|string|div.review-feature\_\_col:has( > div.review-feature\_\_title--positives) > div.review-feature\_\_item|
|list of product disadvantages|cons|string|div.review-feature\_\_col:has( > div.review-feature\_\_title--negatives) > div.review-feature\_\_item|
|how many users think that opinion was helpful|like|int|<p>button.vote-yes["data-total-vote"]</p><p>button.vote-yes > span</p><p>span[id^=votes-yes]</p>|
|how many users think that opinion was unhelpful|dislike|int|<p>button.vote-no["data-total-vote"]</p><p>button.vote-no > span</p><p>span[id^=votes-no]</p>|
|publishing date|publish\_date|string|span.user-post\_\_published > time:nth-child(1) ["datetime"]|
|purchase date|purchase\_date|string|span.user-post\_\_published > time:nth-child(2) ["datetime"]|

## Python libraries used in project
1. Requests
2. BeautifulSoup
3. Json
4. Os
5. Translate
6. Numpy
7. Pandas
8. Matplotlib