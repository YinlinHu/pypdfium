
import sys
from PIL import Image

import ctypes
import pypdfium as PDFIUM
PDFIUM.FPDF_InitLibraryWithConfig(PDFIUM.FPDF_LIBRARY_CONFIG(2, None, None, 0))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: demo.py somefile.pdf")
        exit(0)

    fname = sys.argv[1]

    doc = PDFIUM.FPDF_LoadDocument(fname, None) # load document
    page_count = PDFIUM.FPDF_GetPageCount(doc)  # get page counts
    assert(page_count >= 1)

    page = PDFIUM.FPDF_LoadPage(doc, 0) # load the first page
    width = int(PDFIUM.FPDF_GetPageWidthF(page) + 0.5) # get page width
    height = int(PDFIUM.FPDF_GetPageHeightF(page) + 0.5) # get page height
    
    # render to bitmap
    bitmap = PDFIUM.FPDFBitmap_Create(width, height, 0)
    PDFIUM.FPDFBitmap_FillRect(bitmap, 0, 0, width, height, 0xFFFFFFFF)
    PDFIUM.FPDF_RenderPageBitmap(
        bitmap, page, 0, 0, width, height, 0, 
        PDFIUM.FPDF_LCD_TEXT | PDFIUM.FPDF_ANNOT
        )
    
    # retrieve data from bitmap
    buffer = PDFIUM.FPDFBitmap_GetBuffer(bitmap)
    buffer_ = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte * (width * height * 4)))

    img = Image.frombuffer("RGBA", (width, height), buffer_.contents, "raw", "BGRA", 0, 1)
    img.save("out.png")

    if bitmap is not None:
        PDFIUM.FPDFBitmap_Destroy(bitmap)
    PDFIUM.FPDF_ClosePage(page)
    
    PDFIUM.FPDF_CloseDocument(doc)
