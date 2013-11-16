toppu
=====

Simple command line "top" like performance monitor for Heroku. 

As a means to spot service and connect response time spikes, I found myself passing increasingly complex sed/awk magic back and forth with another developer. I decided heroku needed something like top, and I needed a great excuse to finally write an ncurses based command line tool.

Currently toppu implements some very basic functionality. 

```./toppu -a <appname>```

toppu uses the heroku toolbelt cli to open a log stream. It then parses each logline as it arrives and uses the extracted data to draw a top-like screen.

I use toppu to watch 20-30 dynos at once serving thousands of concurrent users and millions of visitors a month. This probably isn't very helpful or exciting to watch on small or low traffic heroku apps. 

[screenshot]: http://i.imgur.com/B8ZhBPY.png "A recent screenshot of toppu watching 20 dynos"
