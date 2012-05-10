
import file_manager
import patient
import datetime

p1 = patient.patient ('p1', 'tmp.img', 'tmp desc', 'tmp')
p1.date = datetime.datetime.now ()
p1.UUID = '001'

fm = file_manager.FileManager ()

fm.create_clinic_dir ('my_clinic', '.')

fm.get_clinic_dir ()

fm.save_patient_files (p1, 'tmp.pkl', 'tmp.docx', 'tmp2.img')

fm.save_patient_files (p1, '001', 'tmp.pkl', profile_image='tmp.img')

fm.save_patient_files (p1, '001', 'tmp.xml')

files = fm.get_patient_files ('001')

print 'files = ' + ' '.join (files)




