from client import MultimodalHsvColorPaletteExtractorClient
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    client = MultimodalHsvColorPaletteExtractorClient()
    print("=== MULTIMODAL HSV COLOR PALETTE EXTRACTOR ===")
    
    # Synthetic pixel stream simulating a modern dark-mode brand card with vibrant accents
    pixels = []
    pixels += [(20, 24, 33)] * 500   # Deep slate background
    pixels += [(59, 130, 246)] * 250  # Vibrant blue accent
    pixels += [(245, 158, 11)] * 150  # Warm amber highlight
    pixels += [(243, 244, 246)] * 100 # Near-white text
    
    res = client.extract_palette(pixels, top_k=4)
    print(f"Analyzed {res['total_pixels_analyzed']} pixels -> Extracted {res['palette_size']} Dominant Swatches:")
    print()
    
    for i, c in enumerate(res['dominant_palette'], 1):
        print(f"{i}. Hex: {c['hex']} | Share: {c['frequency_share_pct']}% | HSV: ({c['hsv']['hue_deg']}deg, {c['hsv']['saturation']}, {c['hsv']['value']})")
        print(f"   Contrast: White={c['contrast_against_white']}:1 (AA: {c['wcag_aa_compliant_white']}), Black={c['contrast_against_black']}:1 (AA: {c['wcag_aa_compliant_black']})")

if __name__ == "__main__":
    main()
