#!/usr/bin/env python3

import json
import requests
import random
import sys
from io import BytesIO
from optparse import OptionParser
from pathlib import Path
from PIL import Image, ImageChops

def cutImage(im, width, height, resample = Image.BILINEAR):
	ratio = width / height

	if (im.width < width):
		im = im.resize((width, int(im.height * width / im.width) + 1), resample = resample)
	if (im.height < height):
		im = im.resize((int(im.width * width / im.height) + 1, height), resample = resample)

	if ratio < im.width / im.height:
		return im.crop((
			(im.width - im.height * ratio) / 2,
			0, 
			(im.width + im.height * ratio) / 2,
			im.height
		))
	else:
		return im.crop((
			0,
			(im.height - im.width / ratio) / 3,
			im.width,
			(im.height + 2 * im.width / ratio) / 3
		))

def fetchImagesData(char, tags, count = 100, site = "safebooru"):
	if tags != "":
		tags = '+' + tags

	if site == "safebooru":
		url = "https://safebooru.org/index.php?page=dapi&s=post&q=index&tags=" + char + tags + "&limit=" + str(count) + "&json=1"
	elif site == "gelbooru":
		url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=" + char + tags + "&limit=" + str(count) + "&json=1"
	elif site == "danbooru":
		raise NotImplementedError("As of now, Danbooru support is not impemented yet.")
	else:
		raise NameError("Site " + site + " not supported.")
	
	r = requests.get(url).text
	if not r:
		return []
	jsonData = json.loads(r)
	imageData = []
	for img in jsonData:
		imgDict = {}
		for attribute in ("width", "height"):
			imgDict[attribute] = img[attribute]
		imgDict["ratio"] = imgDict["width"] / imgDict["height"]
		if site == "safebooru":
			imgDict["url"] = "https://safebooru.org/images/" + img["directory"] + "/" + img["image"] + "?" + str(img["id"]);
		elif site == "gelbooru":
			imgDict["url"] = "https://gelbooru.org/images/" + img["directory"] + "/" + img["image"] + "?" + str(img["id"]);
		imageData.append(imgDict)

	return imageData

def fetchImage(url):
	if type(url) is str:
		r = requests.get(url)
	elif type(url) is dict:
		r = requests.get(url["url"])
	else:
		raise TypeError

	img = Image.open(BytesIO(r.content))
	return img

# each hole is a tuple in the format (left bound, upper bound, width, height)
def fillTemplate(holes, images, template, resample = Image.BILINEAR):
	if (len(holes) != len(images)):
		raise Exception("Arrays of holes and images must be the same length.")

	# sort both lists by w/h ratio (ascending)
	holes.sort(key = lambda x: x[2] / x[3])
	images.sort(key = lambda x: x.width / x.height)
	
	for i in range(len(holes)):
		x, y, w, h = holes[i]
		cutout = cutImage(images[i], w, h).resize((w, h), resample = resample)
		bottomLayer = Image.new("RGBA", (template.width, template.height), (0, 0, 0, 0))
		bottomLayer.paste(cutout, (x, y, x+w, y+h))
		template = Image.alpha_composite(bottomLayer, template)

	return template

# demo
holes = [
	[12, 681, 163, 167],
	[210, 433, 346, 246],
	[212, 26, 319, 172],
	[379, 282, 86, 105],
	[455, 226, 62, 68],
	[483, 408, 217, 136],
	[555, 547, 462, 441],
	[895, 229, 230, 138],
	[1068, 262, 284, 336],
	[1099, 10, 290, 188],
	[1151, 685, 157, 232],
]

def doItForHer(char, tags = "solo", imgDir = "."):
	imgData = fetchImagesData(char, tags = tags, count = 100)
	imgs = []
	while len(imgs) < len(holes):
		temp = fetchImage(random.choice(imgData))
		imgs.append(temp)

	tmpl = Image.open("template.png")
	result = fillTemplate(holes, imgs, tmpl)
	result.show()

	for filenum in range(1000):
		path = imgDir + "/" + char + "_{:03d}".format(filenum) + ".png"
		if not Path(path).is_file():
			result.save(path)
			break

def main(argv):
	parser = OptionParser(usage = "usage: %prog [options] -c character")
	parser.add_option("-c", "--character",
		action = "store", type = "string",
		help = "character to use in the collage (booru-style naming)")
	parser.add_option("-d", "--directory",
		action = "store", type = "string", default = ".",
		help = "directory for image output (by default workdir)")
	parser.add_option("-t", "--tags",
		action = "store", type = "string", default = "solo",
		help = "booru-style tags separated by '+' (by default solo)")
	
	(options, argv) = parser.parse_args()
	if(options.character == None):
		parser.error("provide a character name, see -h for help")
	
	doItForHer(options.character, tags = options.tags, imgDir = options.directory)

if __name__ == "__main__":
	main(sys.argv)
