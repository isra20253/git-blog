import os
import base64

# Script utilitaire : crée un placeholder PNG minimal (1×1 transparent)
# dans `media/profile_pics/default.png` lorsque celui-ci est absent.
# Utile si vous avez cloné le dépôt sans fichiers medias.
PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="
)


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    media_dir = os.path.join(repo_root, 'media')
    profile_dir = os.path.join(media_dir, 'profile_pics')
    os.makedirs(profile_dir, exist_ok=True)

    out_path = os.path.join(profile_dir, 'default.png')
    if os.path.exists(out_path):
        print(f"Default image already exists at: {out_path}")
        return

    data = base64.b64decode(PNG_BASE64)
    with open(out_path, 'wb') as f:
        f.write(data)
    print(f"Wrote default image to: {out_path}")


if __name__ == '__main__':
    main()
