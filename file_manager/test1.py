
import file_manager

fm = file_manager.FileManager ()

fm.create_clinic_dir ('my_clinic', '.')

fm.get_clinic_dir ()

fm.save_patient_files ('p1', '001', 'tmp.pkl', 'tmp.docx', 'tmp2.img')

fm.save_patient_files ('p1', '001', 'tmp.pkl', profile_image='tmp.img')


fm.save_patient_files ('p1', '001', 'tmp.xml')

files = fm.get_patient_files ('001')

print 'files = ' + ' '.join (files)




