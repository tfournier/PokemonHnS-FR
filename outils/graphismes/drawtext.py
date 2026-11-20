import sys; sys.path.insert(0,'/tmp'); sys.path.insert(0,'/home/claude/scripts')
import gamefont, numpy as np
def put(S, x, y_ink, text, font, fg, sh, bg, clear=None):
    """Draw text so that the first ink row lands on y_ink. clear=(x0,x1,y0,y1) cleared first (only fg/sh pixels)."""
    if clear:
        x0,x1,y0,y1=clear
        reg=S[y0:y1,x0:x1]; lo=reg&15
        m=(lo==fg)|(lo==sh)
        reg[m]=(reg[m]&0xF0)|bg
    r=font.render(text); y=y_ink-3
    for yy in range(r.shape[0]):
        for xx in range(r.shape[1]):
            v=r[yy,xx]
            if v in (1,2):
                p=S[y+yy,x+xx]; S[y+yy,x+xx]=(p&0xF0)|(fg if v==1 else sh)
    return r.shape[1]
