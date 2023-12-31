import os, pandas as pd, numpy as np
from getpass import getuser
from tqdm import tqdm
os.system('cls'); input(f"renaming.py")

path = f'C:/Users/{getuser()}/OneDrive/BBP/Images IBO Cleaned/'
ParametersCSV = pd.read_csv(open('Data/parameters.csv'))

ParentDirs = list(set(ParametersCSV['SellerID']))
ParentDirs.sort()
# Titles for report
deleted_files_csv = open(f'C:/Users/{getuser()}/OneDrive/Diego Monroy/PROGRAMACION/BBP/RenameTool/Data/deleted_files.csv','a')
np.savetxt(deleted_files_csv,['FileName,Extension,FileNameCleaned'],fmt='%s',delimiter=',')
deleted_files_csv.close()

for ParentDir in ParentDirs:
    os.chdir(f'{path}{ParentDir}')

    # Lista de directorios
    DirList = pd.DataFrame(columns=['FileName','Extension','FileNameCleaned'])
    for file in os.listdir(): 
        file = os.path.splitext(file)
        file = [file[0],file[1],(file[0])[:-3] if (file[0])[-3:] == '-AS' else file[0]]
        DirList.loc[len(DirList.index)] = file

    print(f'{"*"*10} Head of DirList "{ParentDir}" {"*"*10}\n{DirList.head()}\n{len(DirList)}\n\n')
    
    delete_row_df = []
    save_files = []


    # bucle que evalua si el archivo se tiene que guardar o eliminar dependiendo de -AS / -BS
    for row in DirList.itertuples():
        if row.FileName[-3:] == '-AS':
            save_files.append(f'{row.FileName}{row.Extension}')
            os.rename(f'{row.FileName}{row.Extension}',f'{row.FileNameCleaned}{row.Extension}')
        else:
            deleted_files_csv = open(f'C:/Users/{getuser()}/OneDrive/Diego Monroy/PROGRAMACION/BBP/RenameTool/Data/deleted_files.csv','a')
            np.savetxt(deleted_files_csv,[f'{row.FileName},{row.Extension},{row.FileNameCleaned}'],fmt='%s',delimiter=',')
            deleted_files_csv.close()
            delete_row_df.append(row.Index)
            os.remove(f'{row.FileName}{row.Extension}')


    # Creacion de DirList limpia
    DirList_cleaned = DirList.drop(delete_row_df,axis=0)
    print(f'{"*"*10} Head of DirList_cleaned "{ParentDir}" {"*"*10}\n{DirList_cleaned.head()}\n{len(DirList_cleaned)}\n\n')

    


    df = ParametersCSV.query(f"SellerID == {ParentDir}")
    print(f'{"*"*10} Head of ParametersCSV filtered {"*"*10}\n{df.head()}\n\n')
    for row in DirList_cleaned.itertuples():
        if not(row.FileNameCleaned in list(df["ClientFaceID"])):
            deleted_files_csv = open(f'C:/Users/{getuser()}/OneDrive/Diego Monroy/PROGRAMACION/BBP/RenameTool/Data/deleted_files.csv','a')
            np.savetxt(deleted_files_csv,[f'{row.FileName},{row.Extension},{row.FileNameCleaned}'],fmt='%s',delimiter=',')
            deleted_files_csv.close()
            os.remove(f'{row.FileNameCleaned}{row.Extension}')

    os.system('cls')
