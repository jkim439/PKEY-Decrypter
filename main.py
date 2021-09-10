__author__ = 'Junghwan Kim'
__copyright__ = 'Copyright 2016-2018 Junghwan Kim. All Rights Reserved.'
__version__ = '1.0.0'

import os
import pydicom
from cryptography.fernet import Fernet


def main():

    # Set file
    path = '/home/jkim/NAS/raw_dicom/brain/_1_normal/PKeys/FROM20180201_TO20180210_PKey.log'

    # Output information
    print '\n----------------------------------------------------------------------------------------------------' \
          '\nPKEY Decrypter %s' \
          '\n----------------------------------------------------------------------------------------------------' \
          '\nYou set path: %s' % (__version__, path)

    # Set path
    path_pkey = os.path.abspath(os.path.join(path, '..'))
    path_parent = os.path.abspath(os.path.join(os.path.abspath(os.path.join(path, '..')), '..'))
    path_name = os.path.basename(path)[0:23]

    # Read file
    with open(path, 'r') as file_read:
        line = file_read.readlines()
        line = [x.strip() for x in line]

    # New file
    file_write = open(path_pkey + '/' + path_name + '_pkey_decrypted.log', 'w')

    # Recur load each line
    i = 0
    for _ in line:

        # Set variables
        accessionNumber = line[i][1:21]
        pkey = line[i][23:67]
        path_dcms = path_parent + '/' + path_name + '/' + accessionNumber + '/dcms/'

        # Output loaded directory
        print '\n[LOAD]', path_dcms

        # Load the first dcm file and Get PatientID
        for paths, dirs, files in sorted(os.walk(path_dcms)):
            dcms = sorted(files)[0]
        try:
            ds = pydicom.dcmread(path_dcms + dcms)
            if ds.PatientID:
                pass
        except:
            print '[ERROR] Cannot load dicom file:', path_dcms + dcms
            exit(1)
        print '[INFO] Encrypted Patient ID:', ds.PatientID[0:25] + '...'

        # Try to decrypt using PKEY
        try:
            fernet = Fernet(pkey)
            patientid = fernet.decrypt(str(ds.PatientID))
            if patientid:
                print '[SUCCESS] Patient ID:', patientid
        except:
            print '[ERROR] Incorrect PKEY:', path_dcms + dcms
            exit(1)

        # Write new line
        newline = line[i] + '\t' + patientid
        file_write.write(newline+'\n')

        i += 1

    # Print result
    print '\n----------------------------------------------------------------------------------------------------' \
          '\nResult' \
          '\n----------------------------------------------------------------------------------------------------' \
          '\n', i, 'Patient IDs are decrypted successfully.'

    return None


if __name__ == '__main__':
    main()