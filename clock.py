import math
from PIL import Image, ImageFont, ImageDraw, ImageColor
import datetime
import dataclasses
import yaml
from zoneinfo import ZoneInfo
import bisect
import re

def statusimg(remain, text):

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


 if remain is not None:
   ring(remain)  

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


def annotatedstatusimg(timeleft:datetime.timedelta, totaltime:datetime.timedelta, where:str, detail:str=''):

 if timeleft.days >= 14:
   w = timeleft.days/7
   if int(w)==w:
     text = f'{w:.0f} weeks left\nuntil {where}'
   else:
     text = f'{w:.1f} weeks left\nuntil {where}'
 elif timeleft.days > 2:
   d=timeleft.days
   text = f'{d} days left\nuntil {where}'
 elif timeleft.total_seconds()>3600:
   text = f'{timeleft.total_seconds()/3600:.1f} hours left\nuntil {where}'
 elif timeleft.total_seconds()>0:
   text = f'{timeleft.total_seconds()//60} minutes left\nuntil {where}'
 else:
   text = f'Go to {where}'

 if detail:
    text += f'\n{detail}'

 if totaltime and timeleft.total_seconds()>0:
   remain=timeleft/totaltime
 else:
   remain=0
 return statusimg(remain, text)




@dataclasses.dataclass
class Event:
    name: str
    when: datetime.datetime
    length: datetime.timedelta
    fromwhen: datetime.datetime=None
    detail: str=None

    @property
    def end(self) -> datetime.datetime:
        return self.when + self.length
 
class CountdownClock:
  def __init__(self, config):
    timezonestr = config.get('timezone', 'America/Chicago')
    self.timezone=ZoneInfo(timezonestr)


    events = []
    for e in config.get('events', []):
      name=e['name']

      detail=e.get('detail')

      when=e['when']
      if when.tzinfo is None:
        when=when.replace(tzinfo=self.timezone)

      length=e.get('length', '0')
      if type(length) == int:
        length=datetime.timedelta(days=length)
      else:
        m=re.match(r'^(\d+)\s*(d|days|w|weeks|wks|h|hours|hrs|m|minutes|min|mins|s|sec|secs)$', length, re.I)
        num=int(m.group(1))
        unit={'h':'hours', 'm': 'minutes', 's': 'seconds', 'd': 'days', 'w':'weeks'}.get(m.group(2)[0].lower(), 'd')
        length=datetime.timedelta(**{unit: num}) 

      fromwhen=e.get('count down from')
      
      events.append(Event(name, when, length, fromwhen, detail))

    events=sorted(events, key=lambda e: e.when)

    #now that they are in order, set the fromwhen values to the previous end if we aren't given a value
    self.events=[]
    previousend=None
    for e in events:
      if e.fromwhen is None:
        self.events.append(dataclasses.replace(e, fromwhen=previousend))
      else:
        self.events.append(e)
      previousend=e.end

  @classmethod
  def fromConfigYaml(cls, name="dates.yaml"):
    with open(name, 'r') as f:
      config = yaml.safe_load(f)

    return cls(config)


  def GetRelevantEvent(self, when=None):
    if when is None:
      when=datetime.datetime.now(tz=self.timezone)

    n=bisect.bisect(self.events, when, key=lambda e: e.when) 
    #back up in to still occuring events
    while n and self.events[n-1].end > when:
      n-=1
    if n >= len(self.events):
      return None
    return self.events[n]
    

  def GetStatusImage(self, when=None):
     e = self.GetRelevantEvent(when)
     if e is None:
       return None
     return annotatedstatusimg(e.when-when, 0 if e.fromwhen is None else (e.when-e.fromwhen), e.name, e.detail)


    

if __name__ == '__main__':
 c=CountdownClock.fromConfigYaml()

 size = (1000,1000)
 image = Image.new('RGB', size, 'white')

 for i in range(88):
  today = datetime.datetime(2025, 1, 3, tzinfo=c.timezone) + datetime.timedelta(days=88-i)
  print(today)
  im=c.GetStatusImage(today)
  if im is not None:
    image.paste(im, (100*(9-i%10), 100*(9-i//10)))
  
 image.show()  

# image = dater()
# image.show()  
