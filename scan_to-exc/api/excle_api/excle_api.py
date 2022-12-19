
import pandas as pd
import openpyxl
import xlrd

def use_excle():
    datadir = 'test.xlsx'
    data = pd.DataFrame(pd.read_excel(datadir, 'test1'))
    data_new = data.drop_duplicates(subset=['ip地址'],keep='first',inplace=False)
    print(data_new)
    wb = openpyxl.load_workbook(datadir)
    writer = pd.ExcelWriter(datadir,engine='openpyxl')
    writer.book = wb
    data_new.to_excel(writer,index=True,sheet_name='sheet2')
    writer.save()
use_excle()
__all__ = ["use_excle"]