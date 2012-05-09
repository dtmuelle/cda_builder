
import file_manager


# setup a clinic and save files to it
fm1 = file_manager.FileManager ()

fm1.create_clinic_dir ('my_clinic', '.')

fm1.get_clinic_dir ()

fm1.save_patient_files ('p1', '001', 'tmp.pkl', 'tmp.docx', 'tmp2.img')

fm1.save_patient_files ('p1', '001', 'tmp.pkl', profile_image='tmp.img')


fm1.save_patient_files ('p1', '001', 'tmp.xml')

files = fm1.get_patient_files ('001')

print 'files in my_clinic1 for patient 001 = ' + ' '.join (files)


# setup another clinic and save files to it
fm2 = file_manager.FileManager ()

fm2.create_clinic_dir ('my_clinic2', '.')

fm2.get_clinic_dir ()

fm2.save_patient_files ('p1', '001', 'tmp.pkl', 'tmp.xml')

fm2.save_patient_files ('p1', '001', 'tmp.pkl', profile_image='tmp2.img')

fm2.save_patient_files ('p1', '001', 'tmp.xml')

files = fm2.get_patient_files ('001')

print 'files in my_clinic2 for patient 001 = ' + ' '.join (files)


# transfer file from the first clinic to the second clinic, asking the
# user whether or not files should be overwritten
fm1.transfer_clinic_files (fm2.get_clinic_dir (), interactive=True)



