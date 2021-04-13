# PyPDFium reboot

A simple, ctypes-based Python 3 binding to [PDFium](https://opensource.google/projects/pdfium), the lean and liberal-licensed PDF rendering library developed by Google for the Chromium project.

This is an effort to take over development for the original PyPDFium which became unmaintained in mid 2020.

## Quick start

```python
import sys
from PIL import Image

import ctypes
import pypdfium as pdfium

# this line is very important, otherwise it won't work
pdfium.FPDF_InitLibraryWithConfig(pdfium.FPDF_LIBRARY_CONFIG(2, None, None, 0))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: demo.py somefile.pdf")
        exit(0)

    fname = sys.argv[1]

    doc = pdfium.FPDF_LoadDocument(fname, None) # load document
    page_count = pdfium.FPDF_GetPageCount(doc)  # get page counts
    assert(page_count >= 1)

    page = pdfium.FPDF_LoadPage(doc, 0) # load the first page
    width = int(pdfium.FPDF_GetPageWidthF(page) + 0.5) # get page width
    height = int(pdfium.FPDF_GetPageHeightF(page) + 0.5) # get page height
    
    # render to bitmap
    bitmap = pdfium.FPDFBitmap_Create(width, height, 0)
    pdfium.FPDFBitmap_FillRect(bitmap, 0, 0, width, height, 0xFFFFFFFF)
    pdfium.FPDF_RenderPageBitmap(
        bitmap, page, 0, 0, width, height, 0, 
        pdfium.FPDF_LCD_TEXT | pdfium.FPDF_ANNOT
        )
    
    # retrieve data from bitmap
    buffer = pdfium.FPDFBitmap_GetBuffer(bitmap)
    buffer_ = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte * (width * height * 4)))

    img = Image.frombuffer("RGBA", (width, height), buffer_.contents, "raw", "BGRA", 0, 1)
    img.save("out.png")

    if bitmap is not None:
        pdfium.FPDFBitmap_Destroy(bitmap)
    pdfium.FPDF_ClosePage(page)
    
    pdfium.FPDF_CloseDocument(doc)

```

## Notes

* Verified to run on 64bit Windows and Linux, and hoped to work on macOS Intel

* PDFium binaries are downloaded and extracted automatically from https://github.com/bblanchon/pdfium-binaries using `update_bindings.py`

* The `pypdfium.py` file is generated by [ctypesgen](https://github.com/davidjamesca/ctypesgen)

* [API documentation](https://developers.foxitsoftware.com/resources/pdf-sdk/c_api_reference_pdfium/group___f_p_d_f_i_u_m.html)

* A [PDF manager](https://github.com/YinlinHu/kuafu) based on PyPDFium and PyQt5


## TODO

* Building platform-specific wheels that only contain a single compiled library

* Windows 32bit support

* macOS ARM support

* Upstream request to build binaries for more platforms, e. g. 32bit Linux (i386, armhf) or 64bit Linux ARM
