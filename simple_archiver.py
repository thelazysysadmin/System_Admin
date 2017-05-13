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
		
	def setup(self, args):
		filepath_args = args[1]
		file_args = args[2]
		archive_name = args[3]

		archive_destination = args[4]
		
		self.filepath = filepath_args
		self.file = file_args
		self.archive_name = archive_name

		self.archive_destination = archive_destination
		
		get_my_pid = os.getpid()
		self.getpid = get_my_pid

		date_time = datetime.date.today()
		self.get_time_stamp = date_time
		
	
	def gatherfiles(self):
		filepath = self.filepath
		file = self.file
		filelist = self.list_files
		os.chdir(filepath)
		
		for file in glob.glob(file):
			filelist.append(os.path.join(filepath, file))

	
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
simpleArchiver.setup(sys.argv)
print(simpleArchiver.gatherfiles())
simpleArchiver.compress()
simpleArchiver.move_archive()
simpleArchiver.tidyup()
