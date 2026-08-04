import os
import tempfile
from PIL import Image, ImageDraw, ImageFont
from typing import Optional


class ImageHandler:
    """
    Handles finding, cropping, resizing, and generating placeholder avatars for student photos.
    """

    def __init__(self, image_folder: Optional[str] = None):
        self.image_folder = image_folder or ""
        self.temp_dir = os.path.join(tempfile.gettempdir(), "mentor_report_avatars")
        self._cache = {}

    def set_image_folder(self, folder_path: str):
        self.image_folder = folder_path
        self._cache.clear()

    def get_student_image(self, reg_no: str, name: str, image_filename: str = "") -> str:
        """
        Locates student photo or generates a clean fallback avatar.
        Returns absolute path to usable PNG image file.
        """
        cache_key = f"{reg_no}_{name}_{image_filename}"
        if cache_key in self._cache and os.path.exists(self._cache[cache_key]):
            return self._cache[cache_key]

        img_path = self._resolve_student_image(reg_no, name, image_filename)
        self._cache[cache_key] = img_path
        return img_path

    def _resolve_student_image(self, reg_no: str, name: str, image_filename: str = "") -> str:
        # 1. Check direct image_filename in folder
        if self.image_folder and os.path.exists(self.image_folder):
            candidates = []
            if image_filename:
                candidates.append(image_filename)
                candidates.append(os.path.basename(image_filename))

            # Also check reg_no extensions (.png, .jpg, .jpeg)
            candidates.extend([
                f"{reg_no}.png", f"{reg_no}.jpg", f"{reg_no}.jpeg",
                f"{reg_no.lower()}.png", f"{reg_no.lower()}.jpg",
                f"{name.replace(' ', '_')}.png", f"{name.replace(' ', '_')}.jpg"
            ])

            for cand in candidates:
                full_path = os.path.join(self.image_folder, cand)
                if os.path.isfile(full_path):
                    return self._prepare_cropped_image(full_path, reg_no)

        # 2. Fallback: Generate custom avatar with student initials
        return self._generate_initials_avatar(reg_no, name)

    def _prepare_cropped_image(self, image_path: str, reg_no: str) -> str:
        """
        Resizes and crops image to standard square 300x300 for slide layout.
        """
        out_path = os.path.join(self.temp_dir, f"photo_{reg_no}.png")
        if os.path.exists(out_path):
            return out_path

        try:
            with Image.open(image_path) as img:
                img = img.convert("RGB")

                # Center crop to square
                width, height = img.size
                min_dim = min(width, height)
                left = (width - min_dim) / 2
                top = (height - min_dim) / 2
                right = (width + min_dim) / 2
                bottom = (height + min_dim) / 2

                img_cropped = img.crop((left, top, right, bottom))
                img_resized = img_cropped.resize((300, 300), Image.Resampling.LANCZOS)
                img_resized.save(out_path, "PNG")
                return out_path
        except Exception:
            return self._generate_initials_avatar(reg_no, "Student")

    def _generate_initials_avatar(self, reg_no: str, name: str) -> str:
        """
        Creates a clean 300x300 circular modern avatar with student initials.
        """
        out_path = os.path.join(self.temp_dir, f"avatar_{reg_no}.png")
        
        # Calculate initials
        name_parts = [p for p in name.split() if p]
        if len(name_parts) >= 2:
            initials = f"{name_parts[0][0]}{name_parts[1][0]}".upper()
        elif len(name_parts) == 1:
            initials = f"{name_parts[0][0]}".upper()
        else:
            initials = "ST"

        img = Image.new("RGB", (300, 300), color=(241, 245, 249))
        draw = ImageDraw.Draw(img)

        # Background circular color based on hash of reg_no
        color_palette = [
            (99, 102, 241),   # Indigo
            (59, 130, 246),   # Blue
            (16, 185, 129),   # Emerald
            (139, 92, 246),   # Purple
            (236, 72, 153),   # Pink
            (245, 158, 11)    # Amber
        ]
        bg_color = color_palette[hash(reg_no) % len(color_palette)]

        # Draw circle
        draw.ellipse([(20, 20), (280, 280)], fill=bg_color)

        # Draw Text Initials
        try:
            font = ImageFont.truetype("arial.ttf", 100)
        except IOError:
            font = ImageFont.load_default()

        # Center text box
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (300 - text_width) / 2
        y = (300 - text_height) / 2 - 10
        draw.text((x, y), initials, fill=(255, 255, 255), font=font)

        img.save(out_path, "PNG")
        return out_path
