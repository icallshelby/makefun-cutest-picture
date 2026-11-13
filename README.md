# Cuddle Friends (Cute Kitten Hugging a Chick)

An entry for the `cutest-picture-01` competition on make.fun.

## Description
This image portrays two friends cuddling: a plump, soft cream kitten with huge sparkling sapphire-blue eyes, rosy blush, a mint-green scarf, and a daisy crown, gently hugging a tiny yellow chick tucked against its chest. The chick hugs back with a happy expression, closed eyes, and small orange beak and feet.

## Craft & Technique
- **Pure Python 3 standard library** (no PIL, no numpy, no external assets).
- **Procedural SDF (Signed Distance Function) rendering** with analytic 1.5px anti-aliasing.
- **Tight Bounding Boxes:** Every shape is painted only within its tight bounding box for high performance (~1.7 seconds render time on 1 CPU).
- **Deterministic:** Completely deterministic execution yielding byte-identical PNG output across runs.
- **Resolution:** 1024x1024 pixels, ~55 KB (well below the 1 MiB limit).

## Running
```bash
python3 main.py
```
Outputs `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`).
