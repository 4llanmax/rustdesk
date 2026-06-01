import os
from PIL import Image

def resize_and_save(src_path, dest_path, size):
    print(f"Resizing to {size} -> {dest_path}")
    img = Image.open(src_path)
    # Ensure high quality scaling
    resized = img.resize(size, Image.Resampling.LANCZOS)
    resized.save(dest_path)

def create_ico(src_path, dest_path):
    print(f"Generating multi-resolution ICO -> {dest_path}")
    img = Image.open(src_path)
    # Windows standard sizes for ICO files
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(dest_path, format="ICO", sizes=sizes)

def main():
    src_logo = r"C:\Users\Allan Max\.gemini\antigravity\brain\b38597f1-5d0a-405f-bad1-0ef82b2002f0\dottcon_logo_1780342504397.png"
    workspace = r"C:\Users\Allan Max\.gemini\antigravity\worktrees\rustdesk\brand-rebrand-github-actions"

    # Define all destination paths and sizes
    targets = [
        (os.path.join(workspace, "res", "32x32.png"), (32, 32)),
        (os.path.join(workspace, "res", "64x64.png"), (64, 64)),
        (os.path.join(workspace, "res", "128x128.png"), (128, 128)),
        (os.path.join(workspace, "res", "128x128@2x.png"), (256, 256)),
        (os.path.join(workspace, "res", "icon.png"), (256, 256)),
        (os.path.join(workspace, "res", "mac-icon.png"), (512, 512)),
        # Tray icons
        (os.path.join(workspace, "res", "mac-tray-dark-x2.png"), (36, 36)),
        (os.path.join(workspace, "res", "mac-tray-light-x2.png"), (36, 36)),
    ]

    # Resize all PNGs
    for dest_path, size in targets:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        resize_and_save(src_logo, dest_path, size)

    # Generate ICO file
    ico_path = os.path.join(workspace, "res", "icon.ico")
    create_ico(src_logo, ico_path)
    
    # Generate tray-icon.ico if applicable (usually smaller)
    tray_ico_path = os.path.join(workspace, "res", "tray-icon.ico")
    resize_and_save(src_logo, tray_ico_path, (32, 32))

    # Rebrand flutter asset icon if needed (we can write icon.png or icon.svg)
    # The flutter app uses the assets folder
    flutter_icon_png = os.path.join(workspace, "flutter", "assets", "icon.png")
    os.makedirs(os.path.dirname(flutter_icon_png), exist_ok=True)
    resize_and_save(src_logo, flutter_icon_png, (256, 256))
    
    print("All assets successfully resized and written!")

if __name__ == "__main__":
    main()
