from PIL import Image

# 打开PNG图片并转换为ICO格式
img = Image.open('cmd.png')
# 可以根据需要调整尺寸，如 (32, 32), (64, 64) 等
img.save('cmd.ico', format='ICO', sizes=[(256, 256)])

# 打开PNG图片并转换为ICO格式
img = Image.open('web.png')
# 可以根据需要调整尺寸，如 (32, 32), (64, 64) 等
img.save('web.ico', format='ICO', sizes=[(256, 256)])