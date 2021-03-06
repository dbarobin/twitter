#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Robin Wen <blockxyz@gmail.com>
#
# Distributed under terms of the MIT license.

# twitter-following
#  - lists all of a given user's friends (ie, followees)

from twitter import *

# load our API credentials
import sys
sys.path.append(".")
import config

# this is the user whose friends we will list
username = "YOUR_TWITTER_NAME"

def main():
    # create twitter API object
    twitter = Twitter(auth = OAuth(config.access_key,
                      config.access_secret,
                      config.consumer_key,
                      config.consumer_secret))

    # perform a basic search
    # twitter API docs: https://dev.twitter.com/rest/reference/get/friends/ids
    query = twitter.friends.ids(screen_name = username)

    # tell the user how many friends we've found.
    # note that the twitter API will NOT immediately give us any more
    # information about friends except their numeric IDs...
    print("Found %d friends\n" % (len(query["ids"])))

    print("Write result to file. Wait until program exit elegantly.\n")

    # write to file
    f = open(username+'-result.log', 'w')

    # now we loop through them to pull out more info, in blocks of 100.
    for n in range(0, len(query["ids"]), 100):
        ids = query["ids"][n:n+100]

        # create a comma-separated string from the ID list
        ids_string = ",".join(str(id) for id in ids)

        # create a subquery, looking up information about these users
        # twitter API docs: https://dev.twitter.com/rest/reference/get/users/lookup
        subquery = twitter.users.lookup(user_id = ids_string)

        for user in subquery:

            # now write user info to file.
            f.write("https://rsshub.app/twitter/user/%s\n" % (user["screen_name"]))

    f.close

if __name__ == "__main__":
    main()