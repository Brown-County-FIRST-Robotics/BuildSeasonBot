import math
from PIL import Image, ImageFont, ImageDraw, ImageColor
import datetime



def statusimg(v, text):

 size = (1000,1000)


 def s(*pcts):
   r =  tuple(int(v*(size[i%2]/100)+.5) for i,v in enumerate(pcts))
   if len(pcts) == 1:
     return r[0]
   return r


 image = Image.new('RGB', size, 'white')
 draw = ImageDraw.Draw(image)  

  

 #draw.ellipse(s(1, 1, 99, 99), fill = 'gray')
 #draw.ellipse(s(10, 10, 90, 90), fill = 'white')
 draw.arc(s(1, 1, 99, 99), width=s(9), start = (-.25)*360, end = (.75-.25)*360, fill ="gray") 
 draw.arc(s(1, 1, 99, 99), width=s(9), start = (.25-.25)*360, end = (-.25)*360, fill ="gray") 



 def ring(v):
  def pwl(a, i):
   lastai = None
   for ai, v in a:
     if i<ai:
       if lastai is None:
         return v
       return (i-lastai)/(ai-lastai)*(v-lastv)+lastv
     lastai=ai
     lastv=v
   return lastv   

  hue=[(.25, 0), (.25, 48), (.5, 60), (1, 120)]
  sat=[(0, 100), ]
  value=[(0, 0), (.25, 100), (.25, 65), (.5, 100)]

  color = ImageColor.getrgb(f"hsv({pwl(hue, v)}, {pwl(sat, v)}%, {pwl(value, v)}%)")
 
  def circat(v):
    x = 50 + math.cos(math.pi*2*(v-.25)) * (49-4.5)
    y = 50 + math.sin(math.pi*2*(v-.25)) * (49-4.5)

    draw.ellipse(s(x-4.5, y-4.5, x+4.5, y+4.5), fill = color)

  draw.arc(s(1, 1, 99, 99), width=s(9), start = (-.25)*360, end = (v-.25)*360, fill =color) 
  circat(0)
  circat(v)



 ring(v)  

 sz=1
 while 1:
  font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', sz)
  sl=None
  for l in text.split('\n'):
   sl1 = draw.textlength(l, font)
   if sl is None or sl1 > sl:
     sl=sl1
  if sl > s(75):
   font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', sz-1)
   break
  sz+=1

 draw.text(s(50, 50), text, font=font,  anchor='ms', fill='black', align ="center")


 image = image.resize(s(10, 10), resample=Image.LANCZOS)
 return image


def timer(days, total, where):

 if days > 14:
   text = f'{days/7:.1f} weeks left\nuntill {where}'
 elif days > 1:
   text = f'{days} days left\nuntill {where}'
 elif days == 1:
   text = f'1 day left\nuntill {where}'
 else:
   text = f'Go to {where}.'

 return statusimg(days/total, text)

 
def dater(today=None):
  if today is None:
    today = datetime.date.today()
  kickoff = datetime.date(2024, 1, 6)
  sussex = datetime.date(2024, 2, 18) 
  duluth = datetime.date(2024, 2, 28) 
  lacrosse = datetime.date(2024, 4, 3) 

  if today <= sussex:
   return timer((sussex-today).days, (sussex-kickoff).days, 'Sussex')
  elif today <= duluth:
   return timer((duluth-today).days, (duluth-kickoff).days, 'Duluth')
  else:
   return timer((lacrosse-today).days, (lacrosse-kickoff).days, 'Lacrosse')


if __name__ == '__main__':
 size = (1000,1000)
 image = Image.new('RGB', size, 'white')

 for i in range(88):
  today = datetime.date(2024, 1, 6) + datetime.timedelta(days=88-i)
  print(today)
  im=dater(today)
  image.paste(im, (100*(9-i%10), 100*(9-i//10)))
  
 image.show()  

# image = dater()
# image.show()  
