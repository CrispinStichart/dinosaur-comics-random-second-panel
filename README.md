![gasp](panels/1.png)

# Random Dinosaur Comics Second Panel

## Background

There is a webcomic by the name of Dinosaur Comics. Naturally, its URL is [qwantz.com][qwantz] (although you can also access it via [chewbac.ca][chewbacca]).

It's what wikipedia calls a "[constrained comic][wiki]" -- in this case the constraint is that in every comic, the art remains the same (with some minor exceptions).  

You might think that the author, Ryan North, would run out of content, but after almost two decades and just under 4000 comics, he's still going strong.

## Get to the point please

Due to the nature of Ryan's writing style, the second panel of almost any of the comics can be taken out of context and remain funny (if your sense of humour is tuned correctly, I guess).

In the long-ago times (circa 2009) someone had written a randomizer that would do just that. There was a URL you could go to that would return a random second panel, and... that was it. That was all it needed to do. 

Back then, I had a website on which I used this randomizer, and I loved it. I recently remembered it and decided I wanted the same thing my [current website][site], but sadly the olf script URL is dead, and I couldn't find a new version. 

So I made one!

## I had no idea making web apps was so easy

Seriously, last time I messed around with making server-side websites, there were no free offerings. If you wanted a server you could actually do something with, you had to pay for it. 

And once you paid for it, you had to manage it. Take your eyes off it for a minute, and next thing you know it's part of a russian botnet. 

Today, in the span of an hour, I:

1. discovered that Heroku has a free tier
2. signed up
3. read enough of the docs to stumble my way to victory
4. pushed my git repo to their server

And... that's it. A free host for running a dynamic web application (albeit a very simple one, in this case) that integrates with git and manages everything I don't want to care about. 

## Gimmie the URL!

Check this out:

https://dino-comics-second-panel.herokuapp.com/random

You can also request specific panels, like so:

* https://dino-comics-second-panel.herokuapp.com/comic/1
* https://dino-comics-second-panel.herokuapp.com/comic/69
* https://dino-comics-second-panel.herokuapp.com/comic/420

## Do it yourself

If you like this but want to host it yourself, or use the panels for another purpose, that's what this repo is for.

Running `bulk-downloader.py` will download and crop all currently existing comics (it starts from 1 and keeps going until it runs out), skipping already downloaded ones.


[site]: https://crispinstichart.github.io/
[qwantz]: https://qwantz.com/
[chewbacca]: http://chewbac.ca/
[wiki]: https://en.wikipedia.org/wiki/Constrained_comics