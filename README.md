# Reddit History Deleter

Automated script that will control a browser to delete the history of your posts and/or comments on reddit.

It will just perform the delete action on all the posts and/or comments you have made on reddit.

# Usage:

1- Enter the credentials in the config.json file

2- Set the directory of the web driver executable to be used with the script

3- Modify at lines 100 and 101 what you want to delete, as far as I know, this can not be reversed.

4- I never tested with gilded comments/posts (which may raise an error)

5- Modify lines 13,14, and 15 to use with a browser other than firefox.

-- Timers, sleeps, pauses, and whatever else that may have the script appear as if there's nothing happenning:

6- It uses a 30 second wait to find an element on the page(will also wait that much when confirming that there are no more comments or posts) you can change it on line 17 and it could result in a malfunction.

7- It uses a "requests wait"(basically a timer that sleeps for 5 seconds) because I was lazy to introduce an asynchronous method to handle the login process. You can change the sleep duration on line 18 and it could result in a malfunction.

Only tested on linux with firefox. the OS used shouldn't be a problem if you do step 2 correctly.
