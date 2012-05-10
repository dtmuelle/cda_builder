
import os
import shutil
import sys
import re


FM_DEBUG = False


# FileManager -
#     Creates and manages the directory where patient files are stored
#     and retrieved.
class FileManager:


    def __init__ (self):
        # valid file extensions and their directory names
        self._file_ext_dict = {'.img':'/images/', '.pkl':'/pickles/', 
                               '.fingerprint':'/fingerprints/',
                               '.xml':'/xmls/'}
        

    ################# Public Method Attributes #######################

    
    ######################## Accessors ###############################


    # Returns the the current clinic's directory.
    # Returns False if create_clinic_dir () has not yet been called.
    def get_clinic_dir (self):

        if self._clinic_path == '':
            self._file_mgr_error ('get_clinic_dir',
                                  'clinic directory not yet created')
            return False

        return self._clinic_path


    ######################## Mutators ################################


    # create_clinic_directory -
    #     Creates the directory structure for a clinic instance
    #     with the clinic directory and the patient data directories
    #     below it. This will be invoked one time on every workstation 
    #     that makes up a clinic.
    # Arguments:
    #     clinic_name - A string containing the name of the clinic.
    #     root_dir - A string containing the name of the directory in which
    #         the new clinic directory will be saved.
    # Returns: 
    #     - True for success, False for failure
    def create_clinic_dir (self, clinic_name, root_dir):

        if self._clinic_path != '':
            self._file_mgr_error ('create_clinic_dir',
                                  'create_clinic_dir () already called')
            return False

        clinic_dir = root_dir + '/' + clinic_name

        if (FM_DEBUG): print "clinic_dir = ", clinic_dir

        if os.path.exists (clinic_dir):
            self._file_mgr_error ('create_clinic_dir',
                          'the path ' + clinic_dir + ' already exists')
            return False

        self._clinic_path = clinic_dir

        # make subdirectories
        os.makedirs (self._clinic_path + '/clinic_config')
        os.makedirs (self._clinic_path + '/patients')
        for directory in self._file_ext_dict.values ():
            os.makedirs (self._clinic_path + '/patients' + directory)

        return True


    # save_patient_files -
    #     Save a patient file(s) to the directory with the appropriate 
    #     name (could be pkl, img, xml, or fingerprint file). Files 
    #     with extentions other than .pkl, .img, .xml, or .fingerprint 
    #     will not be saved. If save_patient_files is called for files 
    #     which are already in the clinic directory, a duplicate will be
    #     saved under a different name.
    # Arguments:
    #     patient_object - a patient object containing the fields "UUID",
    #         "name", and "date"
    #     files - 1 or more strings containing the names of files to be
    #         saved
    #     special_files - If a keyword argument 'profile_image=file_name'
    #         (where file_name is a string containg a specified filename)
    #         is given, file_name will be saved as the profile image.
    #         If a profile image is already saved, it will be overwritten.
    # Returns: 
    #     - An array containing the paths of the files that were 
    #       successfully saved.
    #     - False if create_clinic_dir () has not yet been called
    #     - False if patient_object is invalid or if its UUID, name, or
    #       date fields have not been initialized.
    def save_patient_files (self, patient_object, *files, **special_files):

        if self._clinic_path == '':
            self._file_mgr_error ('save_patient_files',
                                  'clinic directory not yet created')
            return False


        # add error check, patient_object must be valid, fields filled
        UUID = patient_object.UUID # check for actual field names
        patient_name = patient_object.name
        time_stamp = patient_object.date
        time_stamp = (str (time_stamp[0]) + '-' + 
                      str (time_stamp[1]) + '-' + 
                      str (time_stamp[2]) + '-' + 
                      str (time_stamp[3]) + '-' + 
                      str (time_stamp[4]) + '-' + 
                      str (time_stamp[5]) + '-' +
                      str (time_stamp[7]))

        new_filename = ''
        counter = 0
        file_ext = ''
        filenames = []

        if 'profile_image' in special_files.keys ():
            if not os.path.isfile (special_files['profile_image']):
                self._file_mgr_error ('save_patient_files', 
                  special_files['profile_image'] + ': file does not exist')

            elif (re.search (r'(\.[^.]*$)|($)', 
                             special_files['profile_image']).group () != 
                  '.img'):
                self._file_mgr_error ('save_patient_files', 
                                      special_files['profile_image'] + 
                                      ': invalid file extension')
            else:
                new_filename = (self._clinic_path + '/patients' +
                                self._file_ext_dict ['.img'] + 
                                patient_name + '_' + UUID + '_' + 
                                time_stamp + '_p.img')
                shutil.copyfile (special_files['profile_image'], 
                                 new_filename)
                filenames.append (new_filename)


        for old_filename in files:

            if not os.path.isfile (old_filename):
                self._file_mgr_error ('save_patient_files', 
                                    old_filename + ': file does not exist')
                continue
                
            file_ext = re.search (r'(\.[^.]*$)|($)', old_filename).group () 

            if (FM_DEBUG): print "file_ext = ", file_ext

            if (not file_ext or 
                not file_ext in self._file_ext_dict.keys ()):
                self._file_mgr_error ('save_patient_files', 
                             old_filename + ': invalid file extension')
                continue

            new_filename = (self._clinic_path + '/patients' +
                            self._file_ext_dict [file_ext] + patient_name +
                            '_' + UUID + '_' + time_stamp + '_' +
                            str (counter) + file_ext)
                
            # If the filename already exists, suffix the filename with
            # the first available integer.
            while os.path.exists (new_filename):
                new_filename = re.sub (str (counter) + file_ext + r'$',
                                       str (counter + 1) + file_ext, 
                                       new_filename)
                counter = counter + 1
            counter = 0

            shutil.copyfile (old_filename, new_filename)

            filenames.append (new_filename)

        return filenames

        

    # Note: changed parameters to just UUID, assuming that it's unique 
    # to each patient.
    # get_patient_files -
    #     Retrieves all patient files that are connected to the 
    #     specified UUID. 
    # Argument:
    #     UUID - a string containing a UUID
    # Returns:
    #     - An array containing all files for the patient with the 
    #       specified UUID
    #     - False if create_clinic_dir () has not yet been called
    def get_patient_files (self, UUID):

        if self._clinic_path == '':
            self._file_mgr_error ('get_patient_files',
                                  'clinic directory not yet created')
            return False

        patient_files = []

        # look through all directories for file names containing UUID
        for directory in self._file_ext_dict.values ():
            for filename in os.listdir (self._clinic_path + '/patients'
                                        + directory):
                if UUID in filename:
                    patient_files.append (self._clinic_path + '/patients' +
                                          directory + filename)

        return patient_files



    # transfer_clinic_files -
    #     Copies files from this clinic's directory to the target directory.
    #     This clinic's subdirectories are copied recursively. This would 
    #     be invoked if the exit station needed to be moved from one 
    #     workstation to another.
    # Arguments:
    #     target_directory - a string containing the name of the directory 
    #         to which all files should be transferred
    #     interactive - if this is set to True, the used is asked whether
    #         or not files in the target directory should be overwritten.
    #         This is set to False by default.
    # Returns:
    #     - False if create_clinic_dir () has not yet been called or if
    #       the target directory does not exist.
    #     - True for success
    def transfer_clinic_files (self, target_directory, interactive=False):

        if self._clinic_path == '':
            self._file_mgr_error ('transfer_clinic_files',
                                  'clinic directory not yet created')
            return False

        if not os.path.isdir (target_directory):
            self._file_mgr_error ('transfer_clinic_files',
                                  target_directory + ' is not a directory')
            return False

        user_input = ''
        target_dirpath = ''

        for dirpath, dirnames, filenames in os.walk (self._clinic_path):
            
            if (FM_DEBUG): print dirpath, dirnames, filenames

            target_dirpath = re.sub (self._clinic_path, target_directory,
                                     dirpath)
            if (FM_DEBUG): print 'target_dirpath = ', target_dirpath
           
            for dirname in dirnames:
                if not os.path.isdir (target_dirpath + '/' + dirname):
                    os.makedirs (target_dirpath + '/' + dirname)

            for filename in filenames:

                if (interactive == False or
                    not os.path.isfile (target_dirpath + '/' + filename)):
                    shutil.copyfile (dirpath + '/' + filename,
                                     target_dirpath + '/' + filename)

                else: # interactive == True and 
                      # os.path.isfile (target_directory + '/' + filename))
                    user_input = raw_input (('File ' + dirpath + '/' +
                                             filename +
                                             ' exists. Overwrite it?'))

                    if user_input.startswith ('y'):
                        shutil.copyfile (dirpath + '/' + filename,
                                         target_dirpath + '/' + filename)

        return True



    ################# private method attributes ######################


    # prints out an error message to stderr of the form:
    # "class_name: function_name: error_message"
    def _file_mgr_error (self, func_name, error_msg):
        print >> sys.stderr, (__name__ + ': ' + func_name + ': ' + 
                              error_msg)
               
            


    ################### private data attributes ######################

    # the path to the clinic directory
    _clinic_path = ''

    # valid file extensions and their directory names
    _file_ext_dict = {} 

































