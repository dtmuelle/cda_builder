
# creates a clinic, saves a file, transfers files from the first clinic
# to the second clinic

import file_manager
import patient
import datetime
fm = file_manager.FileManager ()
fm.create_clinic_dir ('my_clinic', '.')

p1 = patient.patient ()
p1.date = datetime.datetime.now ()
p1.given_name = 'john'
p1.family_name = 'smith'
p1.id = '1234'
fm2 = file_manager.FileManager ()
fm2.create_clinic_dir ('my_clinic2', '.')

fm.save_patient_files (p1, 'tmp.pkl')

fm.transfer_clinic_files (fm2.get_clinic_dir ())

