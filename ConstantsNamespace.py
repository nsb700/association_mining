import os


class AssociationMiningConstantsNamespace:
    __slots__ = ()
    PROJECT_DIR = os.path.dirname(__file__)
    RAW_CSV_FILES_PATH = os.path.join(PROJECT_DIR, 'step01_clean_raw_data/raw_csv_files')
    CLEAN_CSV_FILES_PATH = os.path.join(PROJECT_DIR, 'step02_association_mining/clean_csv_files')

    RAW_DIAG_CSV_FILENAME = 'diag.csv'
    CLEAN_DIAG_CSV_FILENAME = 'clean_diag.csv'

    RAW_PROV_CSV_FILENAME = 'prov.csv'
    CLEAN_PROV_CSV_FILENAME = 'clean_prov.csv'

    RAW_SERV_CSV_FILENAME = 'serv.csv'
    CLEAN_SERV_CSV_FILENAME = 'clean_serv.csv'

    RAW_TRAN_CSV_FILENAME = 'tran.csv'
    CLEAN_TRAN_CSV_FILENAME = 'clean_tran.csv'