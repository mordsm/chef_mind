"""Additive catalog expansion: existing version-1 records remain valid."""
from pathlib import Path
from copy import deepcopy
import json

path=Path(__file__).resolve().parents[1]/'backend/app/static/report/actions.json'
config=json.loads(path.read_text(encoding='utf-8'))
base={action['id']:action for action in config['actions']}
for id,label,icon,equipment,duration in [
    ('grill','לצלות בגריל','🔥','grill',10),('roast','לצלות בתנור','♨️','oven',30),('bake','לאפות','🥧','oven',30),
    ('fry','לטגן','🍳','pan',5),('boil','להרתיח','🫕','pot',10),('steam','לאדות','☁️','steamer',10)]:
    action=deepcopy(base['cook']);action.update(id=id,label=label,icon=icon)
    action['fields'][1]['default']=duration
    action['fields'][2].update(default=equipment,options=[{'id':id,'label':label} for id,label in [('pot','סיר'),('pan','מחבת'),('oven','תנור'),('grill','גריל'),('steamer','סיר אידוי')]])
    base[id]=action
for id,label,icon,duration in [('stir','לערבב','🥄',2),('wait','להמתין / להניח לנוח','⏳',5)]:
    field=deepcopy(base['cook']['fields'][1]);field.update(default=duration,presets=[1,2,5,10,15])
    base[id]={'id':id,'label':label,'icon':icon,'auto_timer':True,'fields':[field]}
action=deepcopy(base['add']);action.update(id='season',label='לתבל',icon='🧂');action['fields'][0]['default']='salt';action['fields'][2]['default']='tsp';base['season']=action
base['measure']={'id':'measure','label':'למדוד טמפרטורה','icon':'🌡️','auto_timer':False,'fields':[
    {'id':'temperature','label':'מדידה אמיתית בפנים המזון °C','type':'number','nullable':True,'default':None,'presets':[],'min':-50,'max':300,'step':0.1}]}
for action in base.values():
    action['group']='הכנה ותוספות' if action['id'] in ('cut','add','season','stir') else 'בדיקה והמתנה' if action['id'] in ('measure','wait') else 'חימום ובישול'
config['actions']=list(base.values())
path.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"Configured {len(base)} structured actions.")
