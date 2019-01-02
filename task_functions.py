'''All methods are are used to gather information about a task'''
import formats

def store_category():
	while True:
		category = input("\nSpecify what type of task was conducted:\n>>> ").strip().upper()
		if not category:
			print("Category not entered...")
			continue
		return category

def store_note():
	while True:
		note = input("\nProvide details as to what was completed:\n>>> ").strip().upper()
		if not note:
			print("Note not entered...")
			continue
		return note

def store_date():
		date = input("\nProvide the date for which the task was completed - [yyyy-mm-dd]:\n>>> ")
		return formats.date(date)

def store_duration():
	time_duration = input("\nProvide how much time was need to complete the task - [hh:mm]:\n>>> ")
	return formats.timeclock(time_duration)