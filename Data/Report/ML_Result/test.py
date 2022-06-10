
from contextlib import suppress
import os
import comtypes
import ntpath
from pdf2jpg import pdf2jpg
import win32com.client
from comtypes.client import CreateObject

def word_to_pdf(file):
#파라미터로 pdf 파일의 절대경로를 받는다.
    dest = os.path.dirname(file)

    word = comtypes.client.CreateObject('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(file)

    file_name = ntpath.basename(file)
    output_file_path = os.path.join(dest, file_name + ".pdf")
    doc.SaveAs(output_file_path, FileFormat=17)
    doc.Close()
    return output_file_path

def pdf_to_jpg(file):
#파라미터로 pdf 파일의 절대경로를 받는다.
    dest = os.path.dirname(file)
    if not os.path.isdir(dest):
        os.mkdir(dest)
    pdf2jpg.convert_pdf2jpg(file, dest, dpi = 300, pages ='ALL')
    #pdf가 여러 장으로 되어있다면 모든 장을 jpg로 바꾼다.

def word_to_jpg(file):
    with suppress(KeyError): pdf_to_jpg(word_to_pdf(file))

word_to_jpg('C:/Users/areum/Desktop/POC시연자료/test.docx')

