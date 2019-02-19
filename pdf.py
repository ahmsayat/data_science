import sys, csv

def save(file, text):
    with open(file + '.txt', 'w') as file:
        file.write(text)

def csv( row ):
    with open('data.csv', 'a') as f:
        f.write(row)
        f.write('\n')

def xml(s):
    import lxml.html
    page = lxml.html.fromstring( s )
    print(page)
    pages = page.body
    
    print( pages[2][2].text_content() )
    
    for child in pages[2]:
         csv( ( child.text_content().strip() ) )
    
    save("xml", s)
    #title = page.xpath('//head/title/text()')[0]

def pdfrw(path):
    from pdfrw import PdfReader
    x = PdfReader(path)
    print(x.keys(), x.Info, x.Root.keys())
    #print( x.pages[0].Contents.stream )
    
def tika(path):
    from tika import parser
    parsedPDF = parser.from_file(path , xmlContent=True)
    #print(raw['content'])
    fulltext = parsedPDF['content']
    
    metadata_dict = parsedPDF['metadata']
    '''
    title = metadata_dict['title']
    author = metadata_dict['Author'] # capturing all the names from lets say 15 pages. Just want it to capture from first page 
    '''
    pages = metadata_dict['xmpTPg:NPages']
    print("tika parsed pages : ", pages)
    save('tika', fulltext )
    xml(fulltext)

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
        page = pdf.getPage(2)
        #print(page)
        #print('Page type: {}'.format(str(type(page))))
 
        text = page.extractText()
        
        save("PyPDF2", text)
    
        print(type( text ))
 
 
if __name__ == '__main__':
    path = 'Voskero Oil Samples/AB03_001_2016-02-24_GBO.pdf'
    #pdfrw(path) #browse internal pdf structure sepecifications and streams
    
    tika(path)
    
    sys.exit(0)
    
    get_info(path)
    text_extractor(path)