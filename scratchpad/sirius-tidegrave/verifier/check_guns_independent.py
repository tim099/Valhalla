import json,math,itertools
from pathlib import Path
import numpy as np
R=Path('D:/Unity/Valhalla/Sculpture/works');BASE='sirius-tidegrave-01m';OUT=Path(__file__).parent
def cells(w):
 c=json.loads((R/w/'sculpt_cache.json').read_text(encoding='utf-8'));return {tuple(map(int,k.split(','))) for k in c['voxels']},c.get('last_event_file')
links=json.loads((R/(BASE+'-assembly')/'links.json').read_text(encoding='utf-8'))['links'];solid=set();marks={}
for l in links:
 if l['enabled']:
  c,m=cells(l['work']);solid.update(c);marks[l['work']]=m
guns=[]
for frame in ('lower','upper','weather'):
 w=BASE+'-deck-'+frame
 models=json.loads((R/w/'models.json').read_text(encoding='utf-8'))['models']
 for m in models:
  if m.get('meta',{}).get('kind')=='gun':guns.append((frame,m))
res=[];corners=np.array(list(itertools.product((0.,1.),repeat=3)))
for frame,m in guns:
 src,mark=cells(m['work']);ang=math.radians(m['rotate'][2]);rot=np.array([[math.cos(ang),-math.sin(ang),0],[math.sin(ang),math.cos(ang),0],[0,0,1.]])
 pivot=np.array(m['pivot']);at=np.array(m['at']);scale=np.array(m['scale'])
 def trans(p):return ((np.array(p)-pivot)*scale)@rot.T+at
 hits=set();bbox=[]
 for cell in src:
  vs=trans(np.array(cell)+corners);lo=vs.min(axis=0);hi=vs.max(axis=0);bbox.extend([lo,hi])
  for q in itertools.product(*(range(math.floor(lo[j]+1e-7),math.ceil(hi[j]-1e-7)) for j in range(3))):
   if q in solid:hits.add(q)
 anchors={a['name']:trans(np.array(a['at'])+.5).tolist() for a in json.loads((R/m['work']/'anchors.json').read_text(encoding='utf-8'))['anchors']}
 mu=anchors['muzzle'];br=anchors['breech'];direction=np.array(mu)-np.array(br);direction/=np.linalg.norm(direction)
 obstruct=[]
 for t in np.arange(0,200,.5):
  q=tuple(np.floor(np.array(mu)+direction*t).astype(int))
  if q in solid:obstruct.append(q)
 res.append({'frame':frame,'name':m['name'],'source':m['work'],'scale':m['scale'],'muzzle':mu,'breech':br,'cube_volume_collision_count':len(hits),'collision_examples':list(hits)[:5],'outbound_20m_ray_obstruction_count':len(set(obstruct)),'obstruction_examples':list(set(obstruct))[:5]})
ropes=json.loads((R/(BASE+'-assembly')/'ropes.json').read_text(encoding='utf-8'))['ropes'];sheets={r.get('meta',{}).get('sail') for r in ropes if r.get('meta',{}).get('kind')=='sheet'}
out={'watermarks':marks,'count':len(res),'guns':res,'rig_prior_missing_sheets_now_present':{'jib':'jib'in sheets,'mizzen-lateen':'mizzen-lateen'in sheets},'notes':'axis-aligned 0/180/-90 rotations; exact voxel-cube interior overlap, touching surfaces excluded. source cache read independently, no author checker.'}
(OUT/'guns_metrics.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('guns',len(res),'collision guns',sum(r['cube_volume_collision_count']>0 for r in res),'ray obstruction guns',sum(r['outbound_20m_ray_obstruction_count']>0 for r in res),'sheets',out['rig_prior_missing_sheets_now_present']);print([(r['frame'],r['name'],r['collision_examples'],r['obstruction_examples']) for r in res if r['cube_volume_collision_count'] or r['outbound_20m_ray_obstruction_count']])
