
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
files = fm.get_patient_files2 (day='13',file_type='.pkl')

print "files = ", ' '.join (files)



