mailchimp-gardening
===================

Tools for pruning huge Maichimp lists.

WHY?
----

If you manage large Mailchimp lists, you know their web interface
cant't handle more than a couple thousand addresses at a time. Try
to feed more than that and you start to get "Gateway Timeout" errors.

Even if you are using double opt-in, from time to time the compliance
team may force you to prune your lists.

It is very boring to unsubscribe 100,000 adresses manually in
small batches, so I wrote this.

HOW?
----

First, install some libs, if you don't have them already:

    pip install mailsnake
    pip install requests
    
Next, select the segment you want to prune. For example, if you
have to unsubscribe every hotmail address without proven activity:

  1.   go to your list, subscribers->segment
  1.   select "Subscribers match **[ALL]** of the following"
  1.   select "Email"->"ends with"->"@hotmail.com" and click (+)
  1.   select "Subscriber activity"->"dit not open"->"any campaign" and click (+)
  1.   select "Subscriber activity"->"dit not click"->"any campaign"
  1.   click "View segment"
  1.   if you are satusfied with the results, download the segment - if not
       repeat and rinse.
  1.   take note of your API key. It is under "Account"->"API keys" (add a new if needed)
  1.   take note of your list id. It is under "Lists"->"Settings"->"unique id"
  1.   run prune.py


EXAMPLE
-------

Suppose your API key is 3e3e76c36d0d1f349ae7a13f8e53f16f-us2 and your
list id is 576ef0a71c:

    prune.py -key 3e3e76c36d0d1f349ae7a13f8e53f16f-us2 \
             -list-id 576ef0a71c \
             segmentMyList_Apr_20_2012.csv
             
(where segmentMyList_Apr_20_2012.csv is the file you downloaded at step 7)


CONTRIBUTE
----------

Just send me patches.


AUTHOR
------

My name is [Paulo Scardine][1] and I work at [Xtend][2] in Brazil (so excuse my lame English,
my native idiom is Portuguese).

I manage big websites and huge email lists for a living.

   [1]: mailto:paulo@xtend.com.br
   [2]: http://xtend.com.br/
