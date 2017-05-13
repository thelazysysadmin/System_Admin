#!/usr/bin/python

import datetime
import tarfile
import sys
import glob 
import os
import shutil 
from sys import argv

class SimpleArchiver:
	def __init__(self):	
		
		self.list_files=[]

		self.filepath = None
		self.file = None
		
		self.archive_name = None
		self.archive_destination = None
		
		self.getpid = None
		self.get_time_stamp = None

		self.created_archive = None

		self.complete_filepath = None

		self.getpid = os.getpid()

		self.get_time_stamp = datetime.date.today()

	def setup(self, args):

		self.filepath = args[1]
		self.file = args[2]
		self.archive_name = args[3]
		self.archive_destination = args[4]

		os.chdir(self.filepath)

		for files in glob.glob(self.file):
			self.list_files.append(os.path.join(self.filepath, files))

		return os.path.join(self.filepath, self.file)



	def compress(self):
		filelist = self.list_files
		pid = self.getpid
		date_time = self.get_time_stamp
		archive_name = self.archive_name

		filename = "{0}_{1}_{2}.tar.gz".format(pid, date_time, archive_name)
		self.created_archive = filename


		tar = tarfile.open(filename, "w:gz")
		for file in filelist:
			tar.add(file, arcname=os.path.basename(file))
			print("{0} added to archive: {1}...".format(file, filename))
		tar.close()




	def move_archive(self):		
		
		filepath = self.filepath
		archive_name = self.created_archive

		archive_dir = "{0}{1}".format(filepath+"/", archive_name)
		final_dir = self.archive_destination	
		shutil.move(archive_dir, final_dir)


		

	def tidyup(self):
		filelist = self.list_files
		for file in filelist:
			os.remove(file)
			print("DELETING {0}...".format(file))



simpleArchiver = SimpleArchiver()

if os.path.isfile(simpleArchiver.setup(sys.argv)):
			simpleArchiver.compress()
			simpleArchiver.move_archive()
			simpleArchiver.tidyup()

else:
	sys.exit("Quitting...unable to find file")