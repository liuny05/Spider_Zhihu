# Spider_Zhihu
Crawl user info of [zhihu.com](zhihu.com).

Refer to [Zhihu_Crawler](https://github.com/salamer/Zhihu_Crawler), but change quite a lot feature.

The changes mainly include:

+ Optimize the structure.
+ Slow the crawling speed to avoid IP forbidden.
+ Add a proxy to improve the crawling speed and avoid IP forbidden.
+ Print more useful info for debugging.
+ Automatically output logs to `log/crawl.log`.
+ Automatically detect IP forbidden and break, output the last download html file to `html` folder for debugging.
+ Crawl both `/followees`, `/topics`, /answers` url, so user's topics and answers will also be got.
+ Besides, collect more info likes user's question num which is ignored in the original codes.

Note that at present this spider can only crawl 20 topics or answers at most.

Crawling entire info will be considered as a futher function.
