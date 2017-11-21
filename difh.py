import json
import requests
from io import BytesIO
from PIL import Image, ImageChops

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

# each hole is a tuple in the format (left bound, upper bound, width, height)
def fillTemplate(holes, images, template, resample = Image.BILINEAR):
	if (len(holes) != len(images)):
		raise Exception("Arrays of holes and images must be the same length.")

	# sort both lists by w/h ratio (ascending)
	holes.sort(key = lambda x: x[2] / x[3])
	images.sort(key = lambda x: x.width / x.height)
	
	for i in range(len(holes)):
		print(holes[i], images[i])
		x, y, w, h = holes[i]
		cutout = cutImage(images[i], w / h).resize((w, h), resample = resample)
		bottomLayer = Image.new("RGBA", (template.width, template.height), (0, 0, 0, 0))
		bottomLayer.paste(cutout, (x, y, x+w, y+h))
		template = Image.alpha_composite(bottomLayer, template)

	return template

# demo
holes = [
	[12, 681, 163, 167],
	[210, 433, 246, 246],
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
count = len(holes)

imgs = fetchImagesData("tatara_kogasa", count = count)
for i in range(count):
    imgs[i] = fetchImage(imgs[i]["url"])
tmpl = Image.open("template.png")
result = fillTemplate(holes, imgs, tmpl)
result.show()
