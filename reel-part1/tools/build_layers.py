"""Write every scene layer as SVG (assets/svg) and rasterise it (assets/layers) in 3 boil variants."""
import os, re, sys, json
from concurrent.futures import ProcessPoolExecutor
import cairosvg
sys.path.insert(0, os.path.dirname(__file__))
import art

R = 1.0  # raster scale (1 world unit = 1 px)
VARIANTS = 3

def job(name):
    meta = {}
    for v in range(VARIANTS):
        layers = art.SCENES[name](1000 + v * 17)
        for lname, (svg, depth) in layers.items():
            base = f"{name}__{lname}__v{v}"
            if v == 0:
                open(f"assets/svg/{name}__{lname}.svg", "w").write(svg)
            w = float(re.search(r'width="([\d.]+)"', svg).group(1))
            cairosvg.svg2png(bytestring=svg.encode(), write_to=f"assets/layers/{base}.png", output_width=int(w * R))
            meta[lname] = depth
    return name, meta

if __name__ == "__main__":
    os.makedirs("assets/layers", exist_ok=True); os.makedirs("assets/svg", exist_ok=True)
    names = sys.argv[1:] or list(art.SCENES)
    with ProcessPoolExecutor(4) as ex:
        for name, meta in ex.map(job, names):
            print(name, meta)
