
import file_manager
import patient
import datetime

p1 = patient.patient ()
p1.given_name = 'John'
p1.family_name = 'Smith'
#p1.date = "15" # error will be printed
p1.date = datetime.datetime.now ()
p1.id = '12345678910'

fm = file_manager.FileManager ()

print "\n"
print "////////////////////// Starting Test 4 /////////////////////"
print "\n"
print "calling fm.create_clinic_dir ('my_clinic', '.')"
print "\n"


fm.create_clinic_dir ('my_clinic', '.')

print "calling fm.get_clinic_dir ()"
print "\n"

print "clinic_dir = ", fm.get_clinic_dir ()
print "\n"

print "saving patient John Smith's files" 
print ("calling fm.save_patient_files ",
       "(p1, 'tmp.pkl', 'tmp2.img')")
print "\n"

fm.save_patient_files (p1, 'tmp.pkl', 'tmp2.img')

print "saving patient John Smith's files" 
print ("calling fm.save_patient_files (p1, 'tmp.pkl', ",
       "profile_image='tmp.img')")
print "\n"

fm.save_patient_files (p1, 'tmp.pkl', 
                       profile_image='tmp.img')

print ("calling fm.set_images_symlink ('./static/images')")
fm.set_images_symlink ('./static/images')



print "\n"
print "////////////////////// Test 4 Complete /////////////////////"
print "\n"


