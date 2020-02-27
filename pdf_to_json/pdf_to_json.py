# Copyright (C) 2020 Antoine Carme <Antoine.Carme@Laposte.net>
# All rights reserved.

# This file is part of the Python pdf_to_json library and is made available under
# the terms of the 3 Clause BSD license

# https://github.com/antoinecarme/pdf_to_json

import gi
gi.require_version('Poppler', '0.18')
from gi.repository import Gio, GLib, Poppler

class pdf_to_json_converter:

    def __init__(self):
        self.mImageHashOnly = False
        self.mDocument = None
        pass

    def convert(self, uri):
        lDocument = self.parse_doc(uri)
        lDict = self.get_doc_summary(lDocument)
        self.mDocument = lDocument
        return lDict
    
    def parse_doc(self, uri):
        data = None
        import urllib.request
        with urllib.request.urlopen(uri) as response:
            data = response.read()

        input_stream = Gio.MemoryInputStream.new_from_bytes(GLib.Bytes(data))
        document = Poppler.Document.new_from_stream(input_stream, -1, None, None)
        return document

    def get_doc_summary(self, iDoc):
        lDict = {}

        lDict_M = {}
        lDict_M["Title"] = iDoc.get_title()
        # lDict["ID"] = iDoc.get_id()
        lDict_M["Author"] = iDoc.get_author()
        lDict_M["Creator"] = iDoc.get_creator()
        lDict_M["Creation_Date"] = iDoc.get_creation_date()
        lDict_M["Modification_Date"] = iDoc.get_modification_date()
        lDict_M["PDF_Version"] = (iDoc.get_pdf_version_string(), iDoc.get_pdf_subtype_string())
        lDict["MetaData"] = lDict_M
        
        N = iDoc.get_n_pages()
        lPages = {}
        for p in range(N):
            lPage_Dict = {}
            page = iDoc.get_page(p)
            lPages[p] = page
            lPage_Dict["Label"] = page.get_label()
            lPage_Dict["Index"] = page.get_index()
            lPage_Dict["Size"] = page.get_size()
            x = []
            for p_attribute in page.get_text_attributes():
                col = p_attribute.color
                dict1 = {"color":(col.red , col.green, col.blue) , 
                         "font":(p_attribute.font_name , round(p_attribute.font_size , 3))}
                x = x + [str(dict1)]
            lPage_Dict["Attributes"] = list(set(x))
            lPage_Dict["Text"] = page.get_text()
            lPage_Dict["Image"] = self.render_page(page)
            lPage_Dict["Embedded_Images"] = self.extract_images(page)
            lPages[p] = lPage_Dict
        lDict["Pages"] = lPages
        return lDict

    def surface_to_png_base_64(self, surface):
        import io, base64
        buff = io.BytesIO()
        surface.write_to_png(buff)
        base64_encoded = base64.b64encode(buff.getvalue()).decode("utf-8")
        encoded = '<img src=\"data:image/png;base64,' + base64_encoded
        encoded = encoded + '\" border=\"0\" align=\"center\"> </img>'
        return encoded
    
    def extract_images(self , iPage):
        images = {}
        lMapping = iPage.get_image_mapping()
        for lMap in lMapping:
            area = (lMap.area.x1, lMap.area.y1, lMap.area.x2, lMap.area.y2)
            surf = iPage.get_image(lMap.image_id)
            lImage = self.surface_to_png_base_64(surf)
            lDict = {"area" : area , "image" : lImage}
            images[lMap.image_id] = lDict
        return images
    
    def hash_string(self, x):
        import hashlib
        md5_1 = hashlib.md5()
        md5_1.update(x)
        lHash = md5_1.hexdigest()
        return lHash

                      
    def render_page(self, iPage):
        import cairo
        lResolution = 300
        width, height = iPage.get_size()
        lFactor = lResolution / 72.0 #  DPI / 72
        width, height = int(width * lFactor), int(height * lFactor)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        surface.set_fallback_resolution(lResolution, lResolution)
        cr = cairo.Context(surface)
        fo = cairo.FontOptions()
        fo.set_antialias(cairo.ANTIALIAS_GOOD )
        cr.set_font_options(fo)
        cr.scale(lFactor, lFactor)
        iPage.render(cr)
        cr.show_page()

        encoded = self.surface_to_png_base_64(surface)
        lOutput = encoded
        if(self.mImageHashOnly):
            lOutput = self.hash_string(encoded.encode())
        return lOutput
                      

