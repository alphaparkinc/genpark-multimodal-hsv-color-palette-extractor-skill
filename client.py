import math, sys
sys.stdout.reconfigure(encoding='utf-8')

class MultimodalHsvColorPaletteExtractorClient:
    """
    Multimodal visual aesthetic analyzer. Quantizes pixel RGB values into an HSV color space,
    extracts the top dominant color clusters, and calculates WCAG 2.1 contrast ratios.
    """
    def __init__(self):
        pass

    def rgb_to_hsv(self, r, g, b):
        r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
        cmax = max(r_norm, g_norm, b_norm)
        cmin = min(r_norm, g_norm, b_norm)
        delta = cmax - cmin

        if delta == 0:
            h = 0
        elif cmax == r_norm:
            h = (60 * ((g_norm - b_norm) / delta) + 360) % 360
        elif cmax == g_norm:
            h = (60 * ((b_norm - r_norm) / delta) + 120) % 360
        else:
            h = (60 * ((r_norm - g_norm) / delta) + 240) % 360

        s = 0 if cmax == 0 else (delta / cmax)
        v = cmax
        return round(h, 1), round(s, 3), round(v, 3)

    def calculate_relative_luminance(self, r, g, b):
        def srgb_linear(c):
            c_norm = c / 255.0
            return c_norm / 12.92 if c_norm <= 0.04045 else (((c_norm + 0.055) / 1.055) ** 2.4)
        return 0.2126 * srgb_linear(r) + 0.7152 * srgb_linear(g) + 0.0722 * srgb_linear(b)

    def calculate_contrast_ratio(self, lum1, lum2):
        l_high = max(lum1, lum2)
        l_low = min(lum1, lum2)
        return round((l_high + 0.05) / (l_low + 0.05), 2)

    def extract_palette(self, rgb_pixel_tuples, top_k=4):
        if not rgb_pixel_tuples:
            return {"status": "error", "message": "Empty pixel array"}

        # 3D color histogram quantization (4-bit bins per channel = 16x16x16 = 4096 bins)
        bins = {}
        for r, g, b in rgb_pixel_tuples:
            bin_key = (r // 16, g // 16, b // 16)
            if bin_key not in bins:
                bins[bin_key] = {"count": 0, "sum_r": 0, "sum_g": 0, "sum_b": 0}
            bins[bin_key]["count"] += 1
            bins[bin_key]["sum_r"] += r
            bins[bin_key]["sum_g"] += g
            bins[bin_key]["sum_b"] += b

        sorted_bins = sorted(bins.values(), key=lambda x: x["count"], reverse=True)
        total_pixels = len(rgb_pixel_tuples)

        extracted_colors = []
        for b_data in sorted_bins[:top_k]:
            avg_r = int(b_data["sum_r"] / b_data["count"])
            avg_g = int(b_data["sum_g"] / b_data["count"])
            avg_b = int(b_data["sum_b"] / b_data["count"])
            hex_code = f"#{avg_r:02x}{avg_g:02x}{avg_b:02x}".upper()
            h, s, v = self.rgb_to_hsv(avg_r, avg_g, avg_b)
            lum = self.calculate_relative_luminance(avg_r, avg_g, avg_b)
            
            contrast_white = self.calculate_contrast_ratio(lum, 1.0)
            contrast_black = self.calculate_contrast_ratio(lum, 0.0)

            extracted_colors.append({
                "hex": hex_code,
                "rgb": [avg_r, avg_g, avg_b],
                "hsv": {"hue_deg": h, "saturation": s, "value": v},
                "frequency_share_pct": round((b_data["count"] / total_pixels) * 100.0, 2),
                "relative_luminance": round(lum, 4),
                "contrast_against_white": contrast_white,
                "contrast_against_black": contrast_black,
                "wcag_aa_compliant_white": contrast_white >= 4.5,
                "wcag_aa_compliant_black": contrast_black >= 4.5
            })

        return {
            "status": "success",
            "total_pixels_analyzed": total_pixels,
            "palette_size": len(extracted_colors),
            "dominant_palette": extracted_colors
        }
