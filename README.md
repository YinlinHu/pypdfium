# PyPDFium

A simple, ctypes-based Python 3 binding to [PDFium](https://opensource.google/projects/pdfium), the lean and liberal-licensed PDF rendering library developed by Google for the Chromium project.

## Installation
```bash
python3 -m pip install pypdfium
```

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

* Believed to be working on 64bit Windows, Mac OS X and Linux.

* PDFium binaries are downloaded and extracted automatically from https://github.com/bblanchon/pdfium-binaries

* To update PyPDFium, simply run the `update_bindings.py` script (which only works on Linux so far)

* The `pypdfium.py` file is generated by [ctypesgen](https://github.com/davidjamesca/ctypesgen)

* Python wheels ready for installation or distribution are built with `python3 setup.py bdist_wheel`; the installable file will be written to `/dist`

* [API documentation](https://developers.foxitsoftware.com/resources/pdf-sdk/c_api_reference_pdfium/group___f_p_d_f_i_u_m.html)

* A [PDF manager](https://github.com/YinlinHu/kuafu) based on PyPDFium and PyQt5
