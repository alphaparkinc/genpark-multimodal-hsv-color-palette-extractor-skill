import sys, json
from client import MultimodalHsvColorPaletteExtractorClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    client = MultimodalHsvColorPaletteExtractorClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-multimodal-hsv-color-palette-extractor-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    pixels = req.get("pixels", [[30, 40, 50], [255, 100, 50]])
    k = req.get("top_k", 4)
    res = client.extract_palette(pixels, top_k=k)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
