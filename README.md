# do it for h(er) - motivational anime girl collage generator

## A little bit of lore

In the 13th episode of the 6th season of _The Simpsons_, Mr. Burns decorates Homer's cubicle with a special demotivational plaque. Throughout the episode, Homer deepens his relationship with his daughter Maggie and embellishes the poster accordingly.

<p align="center">
<img src=http://i0.kym-cdn.com/photos/images/original/000/509/312/a1e.png height="250px"> <img src=http://i0.kym-cdn.com/photos/images/original/000/509/298/b62.jpg height="250px">
</p>

Over the years, the collage was turned into a template, vectorized and eventually gained meme status in the wider anime community.

<p align="center">
<img src=http://i0.kym-cdn.com/photos/images/newsfeed/000/509/329/176.png height="250px"> <img src=http://i0.kym-cdn.com/photos/images/newsfeed/001/130/384/ff7.jpg height="250px">
</p>

This script steps up the game a level higher and automates the whole ordeal of downloading images and painstakingly pasting them into the template.

## Dependencies

* Python 3.x
  * requests
  * PIL

## Invocation and options

`./difh.py -c character_name` generates a collage, displays it and saves it in the working directory as **character_name_xyz.png**
`./difh.py -h` shows additional options

### On character names

Character tags on Danbooru and other similar aggregators follow a few specific conventions, such as:
* all lowercase, words separated by underscores (example: `princess_zelda`)
* in case of Japanese names, Asian name order is used (surname first) (`hakurei_reimu`)
* in rare cases (mostly short names or ambiguity), franchise name may be required (`mercy_(overwatch)`)

When in doubts or no images have been found, try searching among [Danbooru tags](https://danbooru.donmai.us/tags) - though be wary when clicking on the tags themselves, as content on Danbooru is unfiltered and not always safe for work.

## Image sources

Currently, all imagws are grabbed from [Safebooru](https://safebooru.org/), a very NSFW-filtered version of _Danbooru_. Switches for different aggregators are planned.
