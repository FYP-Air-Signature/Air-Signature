from tkPDFViewer import tkPDFViewer as pdf

class ShowPdf(pdf.ShowPdf):
    def goto(self, page):
        try:
            self.text.see(self.img_object_li[page])
        except IndexError:
            if self.img_object_li:
                self.text.see(self.img_object_li[-1])

    def find(self, x, y):
        self.text.scan_dragto(x, y)