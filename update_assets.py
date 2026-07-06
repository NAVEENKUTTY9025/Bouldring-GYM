import os
import re
import glob
import random

# Mapping of emojis to Lucide icons
emoji_to_lucide = {
    '🏔️': '<i data-lucide="mountain"></i>',
    '🧗': '<i data-lucide="footprints"></i>',
    '💪': '<i data-lucide="dumbbell"></i>',
    '⏱️': '<i data-lucide="clock"></i>',
    '🎯': '<i data-lucide="target"></i>',
    '🎉': '<i data-lucide="party-popper"></i>',
    '🗓️': '<i data-lucide="calendar"></i>',
    '🏆': '<i data-lucide="trophy"></i>',
    '🎶': '<i data-lucide="music"></i>',
    '📊': '<i data-lucide="bar-chart-2"></i>',
    '🏋️': '<i data-lucide="dumbbell"></i>',
    '🧠': '<i data-lucide="brain"></i>',
    '📅': '<i data-lucide="calendar-days"></i>',
    '👨‍🏫': '<i data-lucide="users"></i>',
    '💳': '<i data-lucide="credit-card"></i>',
    '📸': '<i data-lucide="camera"></i>',
    '🌓': '<i data-lucide="moon"></i>',
    '📱': '<i data-lucide="smartphone"></i>',
    '📬': '<i data-lucide="mail"></i>',
    '📞': '<i data-lucide="phone"></i>',
    '❓': '<i data-lucide="help-circle"></i>',
    '📍': '<i data-lucide="map-pin"></i>',
    '🕒': '<i data-lucide="clock"></i>',
    '🪨': '<i data-lucide="mountain-snow"></i>',
    '🤝': '<i data-lucide="handshake"></i>'
}

lucide_script = """    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
        lucide.createIcons();
    </script>
</body>"""

# We have exactly 21 images in images/.
all_images = [
    'images/a1.webp', 'images/ab2.avif', 'images/ab3.webp', 'images/ab4.avif',
    'images/c1.jpg', 'images/c2.avif', 'images/c3.avif', 'images/c4.avif',
    'images/c5.avif', 'images/c6.avif', 'images/e1.avif', 'images/e2.webp',
    'images/e3.webp', 'images/i1.avif', 'images/i2.avif', 'images/i3.avif',
    'images/i4.avif', 'images/i5.avif', 'images/t1.avif', 'images/t2.avif',
    'images/t3.avif'
]
random.shuffle(all_images)
used_images = set()

html_files = glob.glob('*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace Emojis
    for emoji, lucide_tag in emoji_to_lucide.items():
        content = content.replace(emoji, lucide_tag)
        
    # 2. Add Lucide script if not present
    if "lucide.createIcons()" not in content:
        content = content.replace('</body>', lucide_script)
        
    # 3. Deduplicate images
    def image_replacer(match):
        img_src = match.group(1)
        if img_src in used_images:
            # Need a new image
            available = [img for img in all_images if img not in used_images]
            if not available:
                # Reuse if we ran out
                new_src = random.choice(all_images)
            else:
                new_src = available[0]
            used_images.add(new_src)
            return f'src="{new_src}"'
        else:
            used_images.add(img_src)
            return match.group(0)

    # Regex to find src="images/..."
    content = re.sub(r'src="(images/[^"]+)"', image_replacer, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Successfully replaced emojis with Lucide icons and deduplicated images across all HTML files.")
