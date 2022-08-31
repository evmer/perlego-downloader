from datetime import datetime
import websocket
import requests
import shutil
import pdfkit
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
			chapters = {}
			contents = {}
			merged_chapter_part_idx = 0
			bookmap = json.loads(json.loads(data['data']['content']))['bookMap']
			for chapter_no in bookmap:
				chapters[int(chapter_no)] = []
				contents[int(chapter_no)] = {}
				for subchapter_no in bookmap[chapter_no]:
					chapters[int(chapter_no)].append(subchapter_no)
					contents[subchapter_no] = {}
			ws.send(json.dumps({"action":"loadPage","data":{"authToken": AUTH_TOKEN, "pageId": list(chapters)[0], "bookType":"EPUB", "windowWidth":1792, "mergedChapterPartIndex":0}}))

		elif 'pageChunk' in data['event']:
			page_id = int(data['data']['pageId'])

			merged_chapter_no = int(data['data']['mergedChapterNumber']) - 1
			number_of_merged_chapters = int(data['data']['numberOfMergedChapters'])

			chunk_no = int(data['data']['chunkNumber']) - 1
			number_of_chunks = int(data['data']['numberOfChunks'])

			chapter_no = page_id + merged_chapter_no + merged_chapter_part_idx

			if contents[chapter_no] == {}:
				for i in range(number_of_chunks):
					contents[chapter_no][i] = ""

			contents[chapter_no][chunk_no] = data['data']['content']

			# check if all chunks of all merged chapters have been downloaded
			all_downloaded = True
			for i in range(page_id, page_id+number_of_merged_chapters):
				if contents[i] == {}: all_downloaded = False; continue
				for (_, chunk) in contents[i].items():
					if chunk == "":
						all_downloaded = False
			if not all_downloaded:
				continue

			# check if all chapters have been downloaded
			all_downloaded = True
			for i in [page_id]+chapters[page_id]:
				if contents[i] == {}:
					all_downloaded = False

			if all_downloaded:
				print(f"chapters {'-'.join(str(i) for i in range(page_id, page_id+number_of_merged_chapters))} downloaded")
				merged_chapter_part_idx = 0
				try:
					next_page = list(chapters)[list(chapters).index(page_id) + 1]
				except IndexError:
					break
			else:
				merged_chapter_part_idx += 1
				next_page = page_id

			ws.send(json.dumps({"action":"loadPage","data":{"authToken": AUTH_TOKEN, "pageId": str(next_page), "bookType":"EPUB", "windowWidth":1792, "mergedChapterPartIndex":merged_chapter_part_idx}}))

	break

# create cache dir
cache_dir = f'epub_{BOOK_ID}'
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

	# reveal hidden images
	imgs = re.findall("<img.*?>", content, re.S)
	for img in imgs:
		img_new = img.replace('opacity: 0', 'opacity: 1')
		img_new = img_new.replace('data-src', 'src')
		content = content.replace(img, img_new)

	# save page in the cache dir
	f = open(f'epub_{BOOK_ID}/{page_no}.html', 'w')
	f.write(content)
	f.close()

	page_no += 1

pdfkit.from_file([f'epub_{BOOK_ID}/{i}.html' for i in range(page_no)], f'{BOOK_ID}.pdf', options={'encoding': 'UTF-8'})
print(f'{BOOK_ID}.pdf created!')

# delete cache dir
shutil.rmtree(f'epub_{BOOK_ID}')
