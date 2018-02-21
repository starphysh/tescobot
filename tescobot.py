# -*- coding: utf-8 -*-
"""
TescoBot - based on sample code for using ciscosparkbot
Wed 10th Jan - added to git repo!!!
"""

import os, http.client, urllib.request, urllib.parse, urllib.error, base64, json
from ciscosparkbot import SparkBot

__author__ = "Bob Garland"
__author_email__ = "bogarlan@cisco.com"
__copyright__ = "Copyright (c) 2018 Cisco Systems, Inc."
__license__ = "Apache 2.0"

# Retrieve required details from environment variables
bot_email = os.getenv("SPARK_BOT_EMAIL")
spark_token = os.getenv("SPARK_BOT_TOKEN")
bot_url = os.getenv("SPARK_BOT_URL")
bot_app_name = os.getenv("SPARK_BOT_APP_NAME")
tesco_api_key = os.getenv("TESCO_API_KEY")

# Set up the Tesco API headers
tesco_headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': tesco_api_key,
}

# Grocery search on tesco.com
def grocery_search(incoming_msg):
    """
    :param incoming_msg: The incoming message object from Spark
    :return: Return the raw json search result in JSON (markdown format)
    """
    try:
        conn = http.client.HTTPSConnection('dev.tescolabs.com')
        # conn.request("GET", "/grocery/products/?query=beans&offset=1&limit=1&%s" % params, "{body}", tesco_headers)
        # conn.request("GET", "/grocery/products/?query=%s&offset=0&limit=1" % incoming_msg, "{body}", tesco_headers)
        # 20-Feb - Spark Bots appear to return Bot name now - which screwed up the 'replace' below.
        search_string = incoming_msg.text.replace("TescoBot /search ","")
        print("Search string:{}".format(search_string))

        conn.request("GET", "/grocery/products/?query={}&offset=1&limit=1&".format(search_string), "{body}", tesco_headers)
        response = conn.getresponse()
        search_response_data = response.read()
        print(search_response_data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # Turn raw JSON results into a string res_str
    res_str = json.loads(search_response_data)
    # The search results are in a nested dictionary format. However, looking up the "products" key return a list
    # Nasty non-human readable JSON formatting. Grrrr...
    list_of_products=res_str["uk"]["ghs"]["products"]["results"]
    # Should only be one product in the list if there is a match - the top hit - which is element 0
    if list_of_products==[]:
    	return 'I could not find anything matching **{}**'.format(search_string)
    else:
        top_hit=list_of_products[0]
        print(top_hit)

        if "description" in top_hit:
            return 'I found this on tesco.com **Name** {} **Price** £{} **Description** {}'.format(top_hit["name"],top_hit["price"],top_hit["description"])
        else:
            return 'I found this on tesco.com **Name** {} **Price** £{}'.format(top_hit["name"],top_hit["price"])



# Hidden grocery search with full JSON format search results returned
# for practice, demos and debugging
def json_grocery_search(incoming_msg):
    """
    :param incoming_msg: The incoming message object from Spark
    :return: Return the raw json search result in JSON (markdown format)
    :For debugging purposes mainly
    """
    try:
        conn = http.client.HTTPSConnection('dev.tescolabs.com')
        # conn.request("GET", "/grocery/products/?query=beans&offset=1&limit=1&%s" % params, "{body}", tesco_headers)
        # conn.request("GET", "/grocery/products/?query=%s&offset=0&limit=1" % incoming_msg, "{body}", tesco_headers)
        search_string = incoming_msg.text.replace("TescoBot /jsearch ","")
        print("Search string:{}".format(search_string))
        search_arg_list = str.split(search_string)
        if len(search_arg_list) == 3:
            query=str.split(search_string)[0]
            offset=str.split(search_string)[1]
            limit=str.split(search_string)[2]
        elif len(search_arg_list) == 1:
            query=str.split(search_string)[0]
            offset = 1
            limit = 1

        # Request URL https://dev.tescolabs.com/grocery/products/?query={query}&offset={offset}&limit={limit}
        # Request parameters:
        # query (string)    The search term to query by.
        # offset (number)   For use to add pagenation for search results e.g. 10 to start with the 11th result. Default is 0.
        # limit (number)    The number of results to return. Default is 10.
        conn.request("GET", "/grocery/products/?query={}&offset={}&limit={}&".format(query,offset,limit), "{body}", tesco_headers)
        response = conn.getresponse()
        search_response_data = response.read()
        print(search_response_data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # Turn raw JSON results into a string res_str
    res_str = json.loads(search_response_data)

    #return results nicely formatted with indent=2
    return "Grocery search results from devportal.tescolabs.com in raw JSON:\n ``` {}".format(json.dumps(res_str, indent=2))



# Create a new bot
tescobot = SparkBot(bot_app_name, spark_bot_token=spark_token,
               spark_bot_url=bot_url, spark_bot_email=bot_email, debug=True)

# Add new command
tescobot.add_command('/search', 'Look up a product on tesco.com', grocery_search)
tescobot.add_command('/jsearch', 'Return raw JSON output of grocery search [/jsearch query offset limit]', json_grocery_search)


# Run Bot
tescobot.run(host='0.0.0.0', port=5000)
