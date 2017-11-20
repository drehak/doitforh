import json
import requests
from io import BytesIO
from PIL import Image

def cutImage(im, ratio):
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
			(im.height - im.width / ratio) / 2,
			im.width,
			(im.height + im.width / ratio) / 2
		))

def fetchImagesData(char, tags = "solo", count = 100, site = "safebooru"):
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
