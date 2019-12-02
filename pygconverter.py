###############################
##
##	Script: PyGconverter
##	Author: Gbenga Michael
##	Description: This script helps to convert the bible i downloaded from
##	txt to csv to make it compatible with openlp.
##############################

import os
import re
import csv


class PyGconverter:

	def load_txt_file(self,file = None):
		'''This method loads the file to be
		worked on if the format is ".txt"'''
		if file is not None:
			if True:
				file.endswith('.txt')
				if True:
					INPUT_FILE = open(file,'r')
					INPUT_FILE_CONTENT = INPUT_FILE.read()
					INPUT_FILE.close()
					text_file = open('txt_file.txt','w+')
					text_file.write(INPUT_FILE_CONTENT)
					text_file.close()
					text_file = open('txt_file.txt','r')
					self.TXT_FILE = text_file.read()
					text_file.close()
					return print(f"[ OK ] : opened \"{file}\"")
				else:
					return print("[ Error ] : Unable to import this file")
			else:
				return print('[ Error ] : Invalid file format')
		else:
			return print('[ Error ] : Please supply input file')

	def _txt_strip_to_chapter(self, chapter_name, rchapter_name):
		CONTENT = self.TXT_FILE
		query = rf'\W{rchapter_name}'
		queryX = rf'\W{chapter_name}'
		search_rchapter = re.search(query,CONTENT)
		search_chapter = re.search(queryX,CONTENT)
		if search_rchapter is not None and search_chapter is not None:
			END_INDEX = search_rchapter.span()[0] - 1
			START_INDEX = search_chapter.span()[1] + 1
			print(END_INDEX)
			CHAPTER_CONTENT = CONTENT[START_INDEX:END_INDEX]
			nc = 'chapters/%s.txt' % chapter_name
			NEW_CHAPTER = open(nc,'w')
			NEW_CHAPTER.write(CHAPTER_CONTENT)
			NEW_CHAPTER.close()
			return print(f"[ OK ] : written chapter \"{chapter_name}\"")
		else:
			if search_rchapter is None:
				return print('[ Error ] : rchapter_name not found!')
			elif search_chapter is None:
				return print('[ Error ] : chapter_name not found!')
			else:
				return print('[ Error ] : Unable to strip to chapter')

	def _txt_strip_last_chapter(self, chapter_name):
		CONTENT = self.TXT_FILE
		queryX = rf'\W{chapter_name}'

		search_chapter = re.search(queryX,CONTENT)
		if search_chapter is not None:
			END_INDEX = len(CONTENT)
			START_INDEX = search_chapter.span()[1] + 1
			print(END_INDEX)
			CHAPTER_CONTENT = CONTENT[START_INDEX:END_INDEX]
			nc = 'chapters/%s.txt' % chapter_name
			NEW_CHAPTER = open(nc,'w')
			NEW_CHAPTER.write(CHAPTER_CONTENT)
			NEW_CHAPTER.close()
			return print(f"[ OK ] : written chapter \"{chapter_name}\"")
		else:
			if search_rchapter is None:
				return print('[ Error ] : rchapter_name not found!')
			elif search_chapter is None:
				return print('[ Error ] : chapter_name not found!')
			else:
				return print('[ Error ] : Unable to strip to chapter')



	def txt_strip_to_chapter(self, chapter_name = None, rchapter_name =None):
		'''Strips the ".txt" input file to
		chapters, all chapters are stored in
		the chapters folder

		this method uses re module to sort out the
		chapters so the rchapter_name has to be the
		chapter before the chapter we are trying to strip'''
		try:
			os.mkdir('chapters')
			self._txt_strip_to_chapter(chapter_name,rchapter_name)
		except FileExistsError:
			self._txt_strip_to_chapter(chapter_name,rchapter_name)
		except:
			return print("[ Error ] : Unable to create chapters directory")

	def _verses_count(self,chapter_name):
		''' returns the number of verses
		present in that chapter'''
		nc = 'chapters/%s.txt' % chapter_name
		CHAPTER = open(nc,'r+')
		CHAPTER_CONTENT = CHAPTER.read()
		CHAPTER.close()
		VERSES = 1
		query = rf'\W{VERSES}'
		find_verses = re.search(query, CHAPTER_CONTENT)
		while find_verses is not None:
			VERSES +=1
			query = rf'\W{VERSES}'
			find_verses = re.search(query, CHAPTER_CONTENT)
		return VERSES - 1

	def _open_chapter(self, chapter_name):
		'''Helps to open generated chapters in
		the generated chapters folder'''
		nc = f'chapters/{chapter_name}.txt'
		chapter = open(nc,'r+')
		content = chapter.read()
		chapter.close()
		return content

	def _chapter_to_csv(self, csv_name, chapter_name, book_name, chapter_number):
		'''This method if for the small logic
		necessary for writing the chapter to csv'''
		CONTENT = self._open_chapter(chapter_name)
		VERSES_COUNT = self._verses_count(chapter_name)
		CURRENT_COUNT = 0
		csv_name = f'{csv_name}.csv'
		CSV_FILE = open(csv_name,'a+')
		CSV_WRITER = csv.writer(CSV_FILE)
		V,RV, = 0,1
		while CURRENT_COUNT < VERSES_COUNT:
			V +=1; RV+=1; CURRENT_COUNT +=1
			if V is VERSES_COUNT:
				v_query = rf'\W{V}'
				START_INDEX = re.search(v_query, CONTENT).span()[0]
				END_INDEX = len(CONTENT)
				if START_INDEX is not -1:
					NEW_VERSE = CONTENT[START_INDEX:END_INDEX]
					NEW_ROW = [book_name,chapter_number,V,NEW_VERSE]
					CSV_WRITER.writerow(NEW_ROW)
					CSV_FILE.close()
				else:
					return print('[ Error ] : An error occured creating csv file')
			else:
				v_query = rf'\W{V}'
				rv_query = rf'\W{RV}'
				START_INDEX = re.search(v_query, CONTENT).span()[0]
				END_INDEX = re.search(rv_query, CONTENT).span()[0] - 1
				if START_INDEX is not -1 and END_INDEX is not -1:
					NEW_VERSE = CONTENT[START_INDEX:END_INDEX]
					NEW_ROW = [book_name,chapter_number,V,NEW_VERSE]
					CSV_WRITER.writerow(NEW_ROW)
		CSV_FILE.close()


	def chapter_to_csv(self, csv_name, chapter_name, book_name, chapter_number):
		'''After the input file has been striped to chapters,
		this method helps to write the chapter to csv via the csv file
		name supplied. Note: if the csv file exits, it append the chapter
		to the csv'''
		return self._chapter_to_csv(csv_name, chapter_name, book_name, chapter_number)

	def _books_gen(self, books):
			'''This function is a generator for
			books in the book_list'''
			for book in books:
				yield book

	def create_chapters(self, book_list):
		'''This method creates the chapters
		for all the book of the input'''

		books = self._books_gen(book_list)
		next_book = next(books)


		for book in book_list:
			count = book[1]
			chapter = 1; next_chapter = 2
			while chapter < count:
				self.txt_strip_to_chapter(f'{book[0]} {chapter}',f'{book[0]} {next_chapter}')
				chapter +=1; next_chapter +=1
			if chapter == count:
				try:
					next_book = next(books)
					self.txt_strip_to_chapter(f'{book[0]} {chapter}',f'{next_book[0]} 1')
					chapter = 1; next_chapter = 2
				except StopIteration:
					self._txt_strip_last_chapter(f'{book[0]} {book[1]}')
					return print(f"[ OK ] : All chapters completely written")

	def chapters_to_csv(self, csv_name, book_list):

		for book in book_list:
			count = book[1]
			chapter = 1
			print(chapter)
			while chapter <= count:
				self.chapter_to_csv(csv_name, f'{book[0]} {chapter}',f'{book[0]}',f"{chapter}")
				print(f"[ OK ] : Added {book[0]} {chapter} to {csv_name}")
				chapter +=1
			chapter = 1
		print(f"[ OK ] : completely addded all books to {csv_name}")






if __name__ == '__main__':
	g = PyGconverter()
	g.load_txt_file('x.txt')
	book_details = [
	['Genesisi',50],
	['Eksodu',40],
	['Lefitiku',27],
	['Numeri',36],
	['Deuteronomi',34],
	['Joṣua',24],
	['Onidajọ',21],
	['Rutu',4],
	['1 Samueli',31],
	['2 Samueli',24],
	['1 Ọba',22],
	['2 Ọba',25],
	['1 Kronika',29],
	['2 Kronika',36],
	['Esra',10],
	['Nehemiah',13],
	['Esteri',10],
	['Jobu',42],
	['Psalmu',150],
	['Owe',31],
	['Oniwasu',12],
	['Orin',8],
	['Isaiah',66],
	['Jeremiah',52],
	['Ẹkún',5],
	['Esekieli',48],
	['Danieli',12],
	['Hosea',14],
	['Joeli',3],
	['Amosi',9],
	['Obadiah',1],
	['Jona',4],
	['Mika',7],
	['Nahumu',3],
	['Habakuku',3],
	['Sefaniah',3],
	['Hagai',2],
	['Sekariah',14],
	['Malaki',4],
	['Matteu',28],
	['Marku',16],
	['Luku',24],
	['Johanu',21],
	['Iṣe',28],
	['Romu',16],
	['1 Korinti',16],
	['2 Korinti',13],
	['Galatia',6],
	['Efesu',6],
	['Filippi',4],
	['Kolosse',4],
	['1 Tessalonika',5],
	['2 Tessalonika',3],
	['1 Timotiu',6],
	['2 Timotiu',4],
	['Titu',3],
	['Filemoni',1],
	['Heberu',13],
	['Jakọbu',5],
	['1 Peteru',5],
	['2 Peteru',3],
	['1 Johanu',5],
	['2 Johanu',1],
	['3 Johanu',1],
	['Juda',1],
	['Ifihàn',22],
	]

	g.create_chapters(book_details)
	g.chapters_to_csv('verses',book_details)
