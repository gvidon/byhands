# -*- coding: utf-8 -*-
from PIL import Image

#СГЕНЕРИРОВАТЬ ТУМБ
def generate_thumb(input, size=(100, 100), output=None):
	image = Image.open(input)
	
	if(not output):
		output = input+'_thumb'
	
	if image.mode not in ('L', 'RGB'):
		image = image.convert('RGB')
	
	box = image.size[0] > image.size[1] and image.size[1] or image.size[0]
	
	image.crop((0, 0, box, box)).resize(size, Image.ANTIALIAS).save(output, image.format)
	
	return output

#РЕСАЙЗИТЬ ВСЕ ИЗОБРАЖЕНИЯ
def resize(path, size=(600, 800)):
	image = Image.open(path)
	
	image.thumbnail(size, Image.ANTIALIAS)
	image.save(path, image.format)

	return True

