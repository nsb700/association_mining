import os
import pandas as pd
from ConstantsNamespace import AssociationMiningConstantsNamespace


if __name__ == "__main__":

    constants = AssociationMiningConstantsNamespace()

    tran_df = pd.read_csv(os.path.join(constants.CLEAN_CSV_FILES_PATH, constants.CLEAN_TRAN_CSV_FILENAME))

    # ASSOCIATIONS FROM DIAGNOSES TO SERVICES

    total_tcount = len(tran_df['tid'].unique())
    diag_tcount_df = tran_df.groupby(['dimDiagnosisID'], as_index=False).agg(diag_tcount=('tid', 'nunique'))
    serv_tcount_df = tran_df.groupby(['dimServiceCodeID'], as_index=False).agg(serv_tcount=('tid', 'nunique'))
    diag_serv_tcount_df = tran_df.groupby(['dimDiagnosisID', 'dimServiceCodeID'], as_index=False).agg(diag_serv_tcount=('tid', 'nunique'))


    tran_df['T'] = total_tcount
    tran_df = tran_df.merge(diag_tcount_df, how='inner', on=['dimDiagnosisID'])
    tran_df = tran_df.merge(serv_tcount_df, how='inner', on=['dimServiceCodeID'])
    tran_df = tran_df.merge(diag_serv_tcount_df, how='inner', on=['dimDiagnosisID', 'dimServiceCodeID'])


    tran_df['support_diag_serv'] = tran_df['diag_serv_tcount'] / tran_df['T']
    tran_df['confidence_diag_serv'] = tran_df['diag_serv_tcount'] / tran_df['diag_tcount']
    tran_df['expected_confidence_diag_serv'] = tran_df['serv_tcount'] / tran_df['T']
    tran_df['lift_diag_serv'] = tran_df['confidence_diag_serv'] / tran_df['expected_confidence_diag_serv']

    # ASSOCIATIONS FROM DIAGNOSES AND PROVIDERS TO SERVICES

    diag_prov_tcount_df = tran_df.groupby(['dimDiagnosisID', 'dimProviderID'], as_index=False).agg(diag_prov_tcount=('tid', 'nunique'))
    diag_prov_serv_tcount_df = tran_df.groupby(['dimDiagnosisID', 'dimProviderID', 'dimServiceCodeID'], as_index=False).agg(diag_prov_serv_tcount=('tid', 'nunique'))

    tran_df = tran_df.merge(diag_prov_tcount_df, how='inner', on=['dimDiagnosisID', 'dimProviderID'])
    tran_df = tran_df.merge(diag_prov_serv_tcount_df, how='inner', on=['dimDiagnosisID', 'dimServiceCodeID', 'dimProviderID'])

    tran_df['support_diag_prov_serv'] = tran_df['diag_prov_serv_tcount'] / tran_df['T']
    tran_df['confidence_diag_prov_serv'] = tran_df['diag_prov_serv_tcount'] / tran_df['diag_prov_tcount']
    tran_df['expected_confidence_diag_prov_serv'] = tran_df['serv_tcount'] / tran_df['T']
    tran_df['lift_diag_prov_serv'] = tran_df['confidence_diag_prov_serv'] / tran_df['expected_confidence_diag_prov_serv']

    tran_df['percentile_support_diag_serv'] = tran_df.groupby(['dimDiagnosisID'])['support_diag_serv'].transform('rank', pct=True)
    tran_df['percentile_confidence_diag_serv'] = tran_df.groupby(['dimDiagnosisID'])['confidence_diag_serv'].transform('rank', pct=True)
    tran_df['percentile_expected_confidence_diag_serv'] = tran_df.groupby(['dimDiagnosisID'])['expected_confidence_diag_serv'].transform('rank', pct=True)

    tran_df['percentile_support_diag_prov_serv'] = tran_df.groupby(['dimDiagnosisID', 'dimProviderID'])['support_diag_prov_serv'].transform('rank', pct=True)
    tran_df['percentile_confidence_diag_prov_serv'] = tran_df.groupby(['dimDiagnosisID', 'dimProviderID'])['confidence_diag_prov_serv'].transform('rank', pct=True)
    tran_df['percentile_expected_confidence_diag_prov_serv'] = tran_df.groupby(['dimDiagnosisID', 'dimProviderID'])['expected_confidence_diag_prov_serv'].transform('rank', pct=True)

    tran_df.to_csv(os.path.join(constants.CLEAN_CSV_FILES_PATH, 'tran_df.csv'), index=False)
