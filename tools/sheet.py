import sys, os
sys.path.insert(0,'/home/user/Powerpoint/src')
import importlib
import theme, emit_svg, preview
from layouts import _base as B
from PIL import Image

def sheet(keys, out='/tmp/sheet.png', palette='midnight', content=None, cols=2, width=760):
    p = theme.PALETTES[palette]
    imgs=[]
    for k in keys:
        fn=B.get(k)
        c = content or {}
        nodes = fn(p, c, {"page":1,"total":12})
        svg = emit_svg.render_svg(nodes, theme.W, theme.H, p["bg"])
        emit_svg.svg_to_png(svg, f'/tmp/_s_{k}.png', width=width)
        imgs.append(Image.open(f'/tmp/_s_{k}.png').convert('RGB'))
    h = imgs[0].height
    rows = (len(imgs)+cols-1)//cols
    sheet = Image.new('RGB',(cols*width, rows*h),'white')
    for i,im in enumerate(imgs):
        sheet.paste(im, ((i%cols)*width, (i//cols)*h))
    sheet.save(out)
    return out
