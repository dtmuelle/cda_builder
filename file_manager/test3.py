
# Creates a clinic, saves patient files and then retrieves all .pkl 
# files from a particular day.


import file_manager
import patient
import datetime

fm = file_manager.FileManager ()
fm.create_clinic_dir ('my_clinic3', '.')

p = patient.patient ()
p.date = datetime.datetime.now ()
p.family_name = "smith"
p.id = "12345"
p.given_name = "john"

fm.save_patient_files (p, 'tmp.img', 'tmp.pkl')
fm.save_patient_files (p, 'tmp.img', 'tmp.pkl')
fm.save_patient_files (p, 'tmp.img', 'tmp.pkl')

today = datetime.datetime.now ().strftime ('%d')

files = fm.get_patient_files2 (day=today, file_type='.pkl')

print "files = ", ' '.join (files)



