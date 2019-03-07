import sys, csv, io, os

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

from PyPDF2 import PdfFileReader, PdfFileWriter
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
 
def PyPDF2(path):
    get_info(path)
    text_extractor(path)

def pdf_splitter(path):
    for index in range(3): #split first 3 pages
        with open(path, 'rb') as act_mls:
            reader = PdfFileReader(act_mls)
            writer = PdfFileWriter()
            writer.addPage(reader.getPage(index))
            with open( 'subpage' + str(index) + '.pdf' , 'wb') as out_pdf:
                writer.write(out_pdf)

def ImagesInsidePdf( path ):
    import fitz
    doc = fitz.open( path )
    for i in range( len(doc) ):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.writePNG("p%s-%s.png" % (i, xref))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("p%s-%s.png" % (i, xref))
                pix1 = None
            pix = None

#extract images from a pdf:
def minecart( path ):
    import minecart

    pdffile = open( path , 'rb')
    doc = minecart.Document(pdffile)

    page = doc.get_page(0) # getting a single page

    #iterating through all pages
    for page in doc.iter_pages():
        im = page.images[0].as_pil()  # requires pillow
        display(im)
        
    
def PdfToImagesWand( path ):
    from wand.image import Image as Img #ImageMagick not installed
    with Img(filename=path, resolution=300) as img:
        img.compression_quality = 99
        img.save(filename='image_name.jpg')

def pdf2image( path ):
    import pdf2image #poppler not installed
    pages = pdf2image.convert_from_path( path , 500)
    for i, page in enumerate(pages):
        page.save('page%d.jpg' %i, 'JPEG')

#from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders

def OCR_WAND( img ):
    # begin OCR
    #tool = pyocr.get_available_tools()[0]
    #lang = tool.get_available_languages()
    txt = tool.image_to_string( PI.open( io.BytesIO(img) ) , lang=lang , builder=pyocr.builders.TextBuilder() )
    print( txt.encode('ascii','ignore') )

#Erors: pytesseract.pytesseract.TesseractError:
def OCR( img ):
    try:
        from PIL import Image
    except ImportError:
        import Image
    import pytesseract
    
    os.environ["PATH"] += os.pathsep + "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
    os.environ["PATH"] += os.pathsep + "C:\\Program Files (x86)\\Tesseract-OCR"
    os.environ["PATH"] += os.pathsep + "C:\\Program Files (x86)\\Tesseract-OCR\tessdata"
    
    text = pytesseract.image_to_string( Image.open(img) )
    print( pytesseract.image_to_string( Image.open(img) ) )

def pdf2jpg( path ): #bad
    from pdf2jpg import pdf2jpg
    
    # To convert single page
    result = pdf2jpg.convert_pdf2jpg( path , "" , pages="1")
    print(result)
    
    return

    # To convert multiple pages
    result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, pages="1,0,3")
    print(result)

    # to convert all pages
    result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, pages="ALL")
    print(result)
    
# onlineocr.net API 
def api( path ):
    sys.argv.append( path )
    import SampleOCRProjectREST as api
    print( FilePath )
    return
    
    #api.main( path ) #useless...by importing a script, it run

def microsoft( path ):
    import http.client, urllib.request, urllib.parse, urllib.error, base64
    
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '{subscription key}',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'language': 'unk',
        'detectOrientation ': 'true',
    })

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/ocr?%s" % params, open( path , 'rb'), headers)
        response = conn.getresponse()
        data = response.read()
        print( data )
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def TRIE():
    pass

def RADIX():#PAT/SUFFIX
    pass
    
def coprimes_maxflow():
    A = [2, 5, 6, 7]
    B = [4, 9, 10, 12]
    #res = 3
    #answer is create a graph where primes are middle nodes connecting pair(a,b) then run max-flow algorithm


if __name__ == '__main__':
    path = 'Voskero Oil Samples/AB03_001_2016-02-24_GBO.pdf'
    #pdfrw(path) #browse internal pdf structure sepecifications and streams
    #tika(path) #extracts pdf text to xml
    #PyPDF2(path) ##extracts pdf text but low quality
    #OCR( "1.jpg" )
    #api( "1.jpg" )
    
    #microsoft( path )
    
    sys.exit(0)