import sys

def save(file, text):
    with open(file + '.txt' , 'w' , encoding="utf-8") as file:
        file.write(text)
    
def tika(path):
    from tika import parser
    raw = parser.from_file(path)
    #print(raw['content'])
    save('tika', raw['content'] )


from PyPDF2 import PdfFileReader
# get_doc_info.py
def get_info(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
        print(number_of_pages)
    print(info)
 
    author = info.author
    creator = info.creator
    producer = info.producer
    subject = info.subject
    title = info.title

# extracting_text.py
def text_extractor(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
 
        # get the first page
        page = pdf.getPage(10)
        #print(page)
        #print('Page type: {}'.format(str(type(page))))
 
        text = page.extractText()
        
        save("PyPDF2", text)
    
        print(type( text ))
 
 
if __name__ == '__main__':
    path = 'operations_GSOP.pdf'
    tika(path)
    #sys.exit(0)
    get_info(path)
    text_extractor(path)