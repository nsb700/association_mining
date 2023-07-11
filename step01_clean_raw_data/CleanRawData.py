import os
import pandas as pd
import random
from ConstantsNamespace import AssociationMiningConstantsNamespace


if __name__ == "__main__":

    constants = AssociationMiningConstantsNamespace()

    # DIAGNOSIS CODES FILE
    raw_diag_df = pd.read_csv(os.path.join(constants.RAW_CSV_FILES_PATH, constants.RAW_DIAG_CSV_FILENAME))
    raw_diag_df = raw_diag_df.fillna('')
    raw_diag_df.to_csv(os.path.join(constants.CLEAN_CSV_FILES_PATH, constants.CLEAN_DIAG_CSV_FILENAME), index=False)

    # PROVIDER FILE
    raw_prov_df = pd.read_csv(os.path.join(constants.RAW_CSV_FILES_PATH, constants.RAW_PROV_CSV_FILENAME), header=None)
    raw_prov_df.columns = ['dimProviderID', 'ProviderName']
    raw_prov_df = raw_prov_df.dropna()
    raw_prov_df['ProvName'] = raw_prov_df.apply(lambda x: ''.join(random.sample(x.loc['ProviderName'], len(x.loc['ProviderName']))).strip(), axis=1)
    raw_prov_df = raw_prov_df.drop(columns=['ProviderName'])
    raw_prov_df.to_csv(os.path.join(constants.CLEAN_CSV_FILES_PATH, constants.CLEAN_PROV_CSV_FILENAME), index=False)

    # SERVICE CODES FILE
    raw_serv_df = pd.read_csv(os.path.join(constants.RAW_CSV_FILES_PATH, constants.RAW_SERV_CSV_FILENAME))
    raw_serv_df = raw_serv_df.dropna()
    raw_serv_df.to_csv(os.path.join(constants.CLEAN_CSV_FILES_PATH, constants.CLEAN_SERV_CSV_FILENAME), index=False)

    # TRANSACTIONS FILE
    raw_tran_df = pd.read_csv(os.path.join(constants.RAW_CSV_FILES_PATH, constants.RAW_TRAN_CSV_FILENAME))
    raw_tran_df = raw_tran_df.dropna()
    tranids = pd.DataFrame(raw_tran_df['tid'].unique())
    tranids.columns = ['tid']
    tranids['id'] = tranids.index + 1
    raw_tran_df = raw_tran_df.merge(tranids, how='inner', left_on=['tid'], right_on=['tid'])
    raw_tran_df = raw_tran_df.drop(columns=['tid'])
    raw_tran_df = raw_tran_df.rename(columns={'servprov': 'dimProviderID', 'diagcode': 'dimDiagnosisID', 'servcode': 'dimServiceCodeID', 'id': 'tid'})
    raw_tran_df.to_csv(os.path.join(constants.CLEAN_CSV_FILES_PATH, constants.CLEAN_TRAN_CSV_FILENAME), index=False)

