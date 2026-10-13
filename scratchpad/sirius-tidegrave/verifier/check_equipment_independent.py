import json,math,itertools
from pathlib import Path
import numpy as np
R=Path('D:/Unity/Valhalla/Sculpture/works');BASE='sirius-tidegrave-01m';A=R/(BASE+'-assembly');OUT=Path(__file__).parent
def cells(w):return {tuple(map(int,k.split(','))) for k in json.loads((R/w/'sculpt_cache.json').read_text(encoding='utf-8'))['voxels']}
links=json.loads((A/'links.json').read_text(encoding='utf-8'))['links'];solid=set();decks=set();offsets={}
for l in links:
 if l['enabled']:
  at=tuple(l['at']);offsets[l['work']]=at;cc={tuple(q[j]+at[j] for j in range(3)) for q in cells(l['work'])};solid.update(cc)
  if '-deck-' in l['work']:decks.update(cc)
models=[]
for w,offset in offsets.items():
 f=R/w/'models.json'
 if f.exists():
  for m in json.loads(f.read_text(encoding='utf-8'))['models']:
   if m.get('meta',{}).get('kind') in ('powder','wheel','binnacle','capstan'):models.append((w,offset,m))
f=A/'models.json'
if f.exists():
 for m in json.loads(f.read_text(encoding='utf-8'))['models']:
  if m.get('meta',{}).get('kind')=='rudder':models.append((BASE+'-assembly',(0,0,0),m))
corners=np.array(list(itertools.product((0.,1.),repeat=3)));checks=[]
for w,offset,m in models:
 ang=math.radians(m['rotate'][2]);rot=np.array([[math.cos(ang),-math.sin(ang),0],[math.sin(ang),math.cos(ang),0],[0,0,1.]])
 hits=set();bounds=[]
 for q in cells(m['work']):
  vv=((np.array(q)+corners-np.array(m['pivot']))*np.array(m['scale']))@rot.T+np.array(m['at'])+offset
  lo=vv.min(axis=0);hi=vv.max(axis=0);bounds.extend([lo,hi])
  for qq in itertools.product(*(range(math.floor(lo[j]+1e-7),math.ceil(hi[j]-1e-7)) for j in range(3))):
   if qq in solid:hits.add(qq)
 checks.append({'owner':w,'name':m['name'],'kind':m['meta']['kind'],'source':m['work'],'hits':len(hits),'examples':list(hits)[:8],'bounds':[[min(q[j] for q in bounds),max(q[j] for q in bounds)] for j in range(3)]})
verts=[];group=None;ii={}
for line in (OUT/'equipment_actual.obj').read_text(encoding='utf-8').splitlines():
 if line.startswith('v '):x,z,y=map(float,line.split()[1:4]);verts.append((x,y,z))
 elif line.startswith('o '):group=line[2:];ii[group]=set()
 elif line.startswith('f ') and group and 'steer-' in group:ii[group].update(int(t.split('/')[0])-1 for t in line.split()[1:])
steer=[]
for g,indices in ii.items():
 if 'steer-' not in g:continue
 h=set()
 for i in indices:
  q=tuple(math.floor(n) for n in verts[i])
  if q in decks:h.add(q)
 steer.append({'name':g,'deck_hits':len(h),'examples':list(h)[:12]})
orn=cells(BASE+'-ornament');old=solid-orn
root_contacts=sum(any((q[0]+dx,q[1]+dy,q[2]+dz) in old for dx,dy,dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))) for q in orn)
out={'equipment_model_count':len(checks),'checks':checks,'steering_deck_vertex_contacts':steer,'ornament_cells':len(orn),'ornament_cells_touching_prior_structure':root_contacts,'ornament_y120_mirror_difference':sum((x,240-y,z) not in orn for x,y,z in orn)}
(OUT/'equipment_metrics.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('equipment',len(checks),'model collisions',[(c['kind'],c['name'],c['hits'],c['examples']) for c in checks if c['hits']]);print('steering',steer);print('orn',len(orn),'root contacts',root_contacts,'mirror',out['ornament_y120_mirror_difference'])
