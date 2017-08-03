#!/usr/bin/python3.6

__author__ = 'Buky'

import os, sys, re, zipfile, mimetypes


def extract(file_path, repertory_path):
    zip_ref = zipfile.ZipFile(file_path, 'r')
    zip_ref.extractall(os.path.join(repertory_path,'tmp'))

def analyze_phishery(file_path, repertory_path):
    """
    Find URL embed in an office document. More info: https://github.com/ryhanson/phishery
    """
    
    file_settings = repertory_path + '/tmp/word/_rels/settings.xml.rels'
    file_document = repertory_path + '/tmp/word/_rels/document.xml.rels'
    
    if os.path.exists(file_settings):
        file_analyse = file_settings
        print('[*] Phishery, suspicious file detected: settings.xml.\n')
    elif os.path.exists(file_document):
        file_analyse = file_document
        print('[*] Phishery, checking in legit file : docuement.xml.\n')
    else:
        print('[*] No Phishery method.\n')
        return 0

    with open(file_analyse, 'r') as file:
        target = re.findall(r'Target=\"(http.*)\"\s+TargetMode=\"External\"/>', file.read())
        if target:
            print(f"[!] IOC: { ''.join(target) }")
            # print("[!] IOC:", ''.join(target))        # If not in python 3.6.2

def clean(repertory_path):
    try:
        os.remove(os.path.join(repertory_path, 'tmp'))
    except:
        os.system('rm -rf ' + os.path.join(repertory_path, 'tmp'))
    print('[*] Remove temporary files.')

        

if sys.argv[1:]:
    path_file = sys.argv[1]
else:
    path_file = input('[?] File path: ')
path_repertory = os.path.dirname(path_file)

if not os.path.isfile(path_file):
    sys.exit('[*] No file found.')

extract(path_file, path_repertory)
analyze_phishery(path_file, path_repertory)
clean(path_repertory)
