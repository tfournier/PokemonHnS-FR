import re
from PIL import Image
import numpy as np
ROOT='/home/claude/pokemonhns-development/pokehns-expansion/'
def charmap():
    cm={}
    for line in open(ROOT+'charmap.txt',encoding='utf-8'):
        line=line.split('@')[0].strip()
        m=re.match(r"'(.+)'\s*=\s*([0-9A-Fa-f]{2})$",line)
        if m and m.group(1) not in cm: cm[m.group(1).replace("\\'","'")]=int(m.group(2),16)
    return cm
def widths(name):
    src=open(ROOT+'src/fonts.c').read()
    m=re.search(r'%s\[\]\s*=\s*\{(.*?)\};'%name,src,re.S)
    return [int(x,0) for x in re.findall(r'0x[0-9A-Fa-f]+|\d+',re.sub(r'//.*','',m.group(1)))]
class Font:
    def __init__(self,png='latin_normal',wname='gFontNormalLatinGlyphWidths',h=16):
        self.im=np.array(Image.open(ROOT+'graphics/fonts/%s.png'%png)); self.w=widths(wname); self.cm=charmap(); self.h=h
    def glyph(self,ch):
        c=self.cm[ch]; x0=(c%16)*16; y0=(c//16)*16
        return self.im[y0:y0+self.h,x0:x0+self.w[c]]
    def render(self,text):
        gs=[self.glyph(c) for c in text]
        return np.hstack(gs)
