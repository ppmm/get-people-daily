#-*- coding:utf-8 -*-

import requests
import os
import sys
import getopt
from PyPDF2 import PdfFileMerger

class Paper(object):
    
    def __init__(self, year, month, day):
        self.year = '%04d' % year
        self.month = '%02d' % month
        self.day = '%02d' % day
        self.base_url = 'http://paper.people.com.cn/rmrb/page/'
        self.paper_name = '人民日报-'+self.year+'年'+self.month+'月'+self.day+'日.pdf'

    def get_pdf(self,url,filename):
        r = requests.get(url)
        if not r.ok:
            return r.ok
        with open(filename, "wb") as f:
            f.write(r.content)
        print('Save Page: '+filename)
        return r.ok

    def get_page(self,pagenum):
        pagenum = '%02d' % pagenum
        d = self.year+self.month+self.day
        p =d+'/rmrb'+d+pagenum+'.pdf'
        if not os.path.exists(d):
            os.mkdir(d)
        pageurl = ''.join([
                self.base_url,self.year,'-',
                self.month,'/',self.day,'/',
                pagenum,'/rmrb',self.year,
                self.month,self.day,pagenum,'.pdf'])
        return self.get_pdf(pageurl,p),p

    def merge_pages(self,pdfs,o):
        m = PdfFileMerger()
        for pdf in pdfs:
            m.append(pdf)
        m.write(o)
        m.close()
                

    def get_paper(self):
        i = 1
        l = []
        while True:
            ok,p = self.get_page(i)
            if not ok:
                break
            l.append(p)
            i += 1
        #self.merge_pages(l,d+'/'self.paper_name)

def main():
    opts, args = getopt.getopt(sys.argv[1:],'d:',['date='])
    for o, a in opts:
        if o in ['-d','--date']:
            x = a.split('.')
            year = int(x[0])
            month = int(x[1])
            day = int(x[2])
    p = Paper(year,month,day)
    p.get_paper()


if __name__ == '__main__':
    main()
