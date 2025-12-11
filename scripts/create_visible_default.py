from PIL import Image, ImageDraw, ImageFont
import os


def main():
    # Génère un placeholder visible (300x300) avec texte "No Image"
    # et l'écrit dans `media/profile_pics/default.png`.
    # Utile pour avoir un visuel par défaut plus lisible que le 1×1.
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    media_dir = os.path.join(repo_root, 'media')
    profile_dir = os.path.join(media_dir, 'profile_pics')
    os.makedirs(profile_dir, exist_ok=True)

    out_path = os.path.join(profile_dir, 'default.png')

    # Create a 300x300 image with a simple placeholder design
    size = (300, 300)
    color = (70, 130, 180)  # steelblue
    img = Image.new('RGBA', size, color)

    draw = ImageDraw.Draw(img)
    text = "No Image"
    try:
        # Try to load a default truetype font; fallback if not available
        font = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font = ImageFont.load_default()

    # Compute text size in a Pillow-version compatible way
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except Exception:
        try:
            text_width, text_height = draw.textsize(text, font=font)
        except Exception:
            text_width, text_height = font.getsize(text)

    text_position = ((size[0]-text_width)//2, (size[1]-text_height)//2)

    draw.text(text_position, text, fill=(255,255,255), font=font)

    img.save(out_path)
    print(f"Wrote visible default image to: {out_path}")


if __name__ == '__main__':
    main()
