from datetime import datetime
import websocket
import requests
import shutil
import pdfkit
import base64
import time
import json
import re
import os

BOOK_ID = "#BOOK_ID#"
AUTH_TOKEN = "#AUTH_TOKEN#"

# download pages
while True:
	while True:
		try:
			ws = websocket.create_connection("wss://api-ws.perlego.com/book-delivery/", skip_utf8_validation=True)
		except Exception:
			continue
		break

	time.sleep(1)

	ws.send(json.dumps({"action":"initialise","data":{"authToken": AUTH_TOKEN, "reCaptchaToken": AUTH_TOKEN, "bookId": str(BOOK_ID)}}))

	page_loaded = False

	while True:
		data = json.loads(ws.recv())

		if data['event'] == 'initialisationDataChunk':
			data_content = json.loads(json.loads(data['data']['content']))
			book_format = data_content['bookType']
			merged_chapter_part_idx = 0

			if book_format == 'EPUB':
				chapters = {}
				contents = {}
				bookmap = data_content['bookMap']
				for chapter_no in bookmap:
					chapters[int(chapter_no)] = []
					contents[int(chapter_no)] = {}
					for subchapter_no in bookmap[chapter_no]:
						chapters[int(chapter_no)].append(subchapter_no)
						contents[subchapter_no] = {}

			elif book_format == 'PDF':
				chapters = {}
				contents = {}
				for i in range(1, data_content['numberOfChapters'] + 1):
					chapters[i] = []
					contents[i] = {}

			else:
				raise Exception(f'unknown book format ({book_format})!')

			ws.send(json.dumps({"action":"loadPage","data":{"authToken": AUTH_TOKEN, "pageId": list(chapters)[0], "bookType": book_format, "windowWidth":1792, "mergedChapterPartIndex":0}}))


		elif 'pageChunk' in data['event']:
			page_id = int(data['data']['pageId'])

			merged_chapter_no = (int(data['data']['mergedChapterNumber']) - 1) if book_format == 'EPUB' else 0
			number_of_merged_chapters = int(data['data']['numberOfMergedChapters']) if book_format == 'EPUB' else 1

			chunk_no = int(data['data']['chunkNumber']) - 1
			number_of_chunks = int(data['data']['numberOfChunks'])

			chapter_no = page_id + merged_chapter_no + merged_chapter_part_idx

			if contents[chapter_no] == {}:
				for i in range(number_of_chunks):
					contents[chapter_no][i] = ""

			contents[chapter_no][chunk_no] = data['data']['content']

			# check if all chunks of all merged pages/chapters have been downloaded
			if all(contents[i] != {} and all(chunk != "" for chunk in contents[i].values()) for i in range(page_id, page_id+number_of_merged_chapters+merged_chapter_part_idx)):

				# check if all pages/chapters have been downloaded
				if all(contents[i] != {} for i in [page_id]+chapters[page_id]):

					print(f"{'chapters' if book_format == 'EPUB' else 'page'} {'-'.join(str(i) for i in range(page_id, page_id+number_of_merged_chapters+merged_chapter_part_idx))} downloaded")
					merged_chapter_part_idx = 0
					try:
						next_page = list(chapters)[list(chapters).index(page_id) + 1]
					except IndexError:
						break
				else:
					merged_chapter_part_idx += 1
					next_page = page_id

				ws.send(json.dumps({"action":"loadPage","data":{"authToken": AUTH_TOKEN, "pageId": str(next_page), "bookType": book_format, "windowWidth":1792, "mergedChapterPartIndex":merged_chapter_part_idx}}))

	break

# create cache dir
cache_dir = f'{book_format}_{BOOK_ID}'
try:
	os.mkdir(cache_dir)
except FileExistsError:
	pass

# convert html files to pdf
print('building pdf...')
page_no = 0

for chapter_no in contents:

	# merge chunks
	content = ""
	for chunk_no in sorted(contents[chapter_no]):
		content += contents[chapter_no][chunk_no]

	# replace svg (see https://stackoverflow.com/questions/12395541/wkhtmltopdf-failure-when-embed-an-svg)
	svgs = re.findall("<svg.*?</svg>", content, re.S)
	for svg in svgs:
		url = re.search('xlink:href="(.*?)"', svg).group(1)
		height = re.search('height="([0-9]*)"', svg).group(1)
		width = re.search('width="([0-9]*)"', svg).group(1)
		content = content.replace(svg, f'<img src="{url}" width="{width}" height="{height}">')

	# replace picture
	pictures = re.findall("<picture.*?</picture>", content, re.S)
	for picture in pictures:
		url = re.search('data-src="(.*?)"', picture).group(1)
		content = content.replace(picture, f'<img src="{url}">')

	# reveal hidden images
	imgs = re.findall("<img.*?>", content, re.S)
	for img in imgs:
		img_new = img.replace('opacity: 0', 'opacity: 1')
		img_new = img_new.replace('data-src', 'src')
		content = content.replace(img, img_new)

	# replace objects
	objects = re.findall("<object.*?</object>", content, re.S)
	for obj in objects:
		src = re.search('data="(.*?)"', obj).group(1)
		if 'base64,' in src:
			b64 = base64.b64decode(src.split('base64,')[1]).decode('utf-8')
			content = content.replace(obj, b64)
		else:
			obj_new = obj.replace('</object>', '')
			obj_new = obj_new.replace('object', 'img')
			obj_new = obj_new.replace('data="', 'src="')
			content = content.replace(obj, obj_new)

	# save page in the cache dir
	f = open(f'{book_format}_{BOOK_ID}/{page_no}.html', 'w', encoding='utf-8')
	f.write(content)
	f.close()

	page_no += 1

pdfkit.from_file([f'{book_format}_{BOOK_ID}/{i}.html' for i in range(page_no)], f'{BOOK_ID}.pdf', options={'encoding': 'UTF-8', 'enable-local-file-access': None})
print(f'{BOOK_ID}.pdf created!')

# delete cache dir
shutil.rmtree(f'{book_format}_{BOOK_ID}')
