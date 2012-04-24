mailchimp-gardening
===================

Tools for pruning Maichimp lists.

WHY?
----

If you manage large Mailchimp lists, you know their web interface
cant't handle more than a couple thousand addresses at a time. Try
to feed more than that and you start to get "Gateway Timeout" errors.

If you are not using double opt-in, from time to time the compliance
team you force you to prune your lists. It is very boring to unsubscribe
100,000 adresses manually.


HOW?
----

First, install mailsnake, if you don't have it already:

    pip install mailsnake
    
Next, select the segment you want to prune. For example, if you
have to unsubscribe every hotmail address without proven activity:

  1. go to your list, subscribers->segment
  2. select "Subscribers match **[ALL]** of the following"
  3. select "Email"->"ends with"->"@hotmail.com" and click (+)
  4. select "Subscriber activity"->"dit not open"->"any campaign" and click (+)
  5. select "Subscriber activity"->"dit not click"->"any campaign"
  6. click "View segment"
  7. if you are satusfied with the results, download the segment - if not
     repeat and rinse.
  8. take note of your API key. It is under "Account"->"API keys" (add a new if needed)
  9. take note of your list id. It is under "Lists"->"Settings"->"unique id"
 10. run prune.py

EXAMPLE
-------

Suppose your API key is 3e3e76c36d0d1f349ae7a13f8e53f16f-us2 and your
list id is 576ef0a71c:

    prune.py -key 3e3e76c36d0d1f349ae7a13f8e53f16f-us2 \
             -list-id 576ef0a71c \
             segmentMyList_Apr_20_2012.csv
             
(where segmentMyList_Apr_20_2012.csv is the file you downloaded at step 7)




