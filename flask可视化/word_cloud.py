from wordcloud import WordCloud
import jieba
from  matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import sqlite3

con = sqlite3.connect("movie.db")
cur = con.cursor()
sql = "select introduction from movie250"
data = cur.execute(sql)
text = ""
for item in data:
    text += item[0]

cut = jieba.cut(text)
string = ' '.join(cut)

img = Image.open(r'.\static\assets\img\man.jpg')
img_array = np.array(img)
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path="msyh.ttc"
)
wc.generate_from_text(string)

fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
plt.savefig(r'.\static\assets\img\world_cloud.jpg', dpi=450)