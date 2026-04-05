from PIL import Image
import os

def remove_green_background(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # Green chroma key: low R, high G, low B
        # item[0]=R, item[1]=G, item[2]=B, item[3]=A
        if item[0] < 100 and item[1] > 150 and item[2] < 100:
            new_data.append((255, 255, 255, 0))  # Transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Saved: {output_path}")

input_img = r"C:\Users\kiyom\.gemini\antigravity\brain\2d8bc1a5-3e89-4b40-a7cd-47f6c5bea66f\creator_catalyst_green_mascot_1775397911066.png"
output_img = r"c:\dev\Creator-Catalyst\Creator_Catalyst_icon_transparent.png"
remove_green_background(input_img, output_img)
