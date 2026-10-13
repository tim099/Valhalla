import json
from pathlib import Path
import numpy as np
from scipy.ndimage import binary_propagation,generate_binary_structure
R=Path('D:/Unity/Valhalla/Sculpture/works');D=R/'sirius-tidegrave-01m/design'
def replay(work):
 v={}
 for f in sorted((R/work/'events').rglob('*.json')):
  e=json.loads(f.read_text(encoding='utf-8'))
  for x,y,z,c in e.get('placed_colored',[]):v[x,y,z]=c
  for q in e.get('carved_voxels',[]):v.pop(tuple(q),None)
 return v
shell=replay('sirius-tidegrave-01m');coords=set(shell);parts={}
links=json.loads((R/'sirius-tidegrave-01m-assembly/links.json').read_text(encoding='utf-8'))['links']
for l in links:
 if l['enabled'] and l['work']!='sirius-tidegrave-01m':parts[l['name']]=replay(l['work']);coords.update(parts[l['name']])
rep=json.loads((D/'verify_decks.json').read_text(encoding='utf-8'));checks=[]
for s in rep['stairs']:
 anchors={}
 for name,p in s['points'].items():
  x,y,z=p
  anchors[name]={'point_air':(x,y,z) not in coords,'support_below':(x,y,z-1) in coords,'vertical20_clear':all((x,y,z+dz) not in coords for dz in range(20)),'body20_clear':all((x+dx,y+dy,z+dz) not in coords for dx in range(-2,3) for dy in range(-2,3) for dz in range(20))}
 a=s['points']['head'][0];b=s['points']['foot'][0];run=[]
 for x in range(min(a,b),max(a,b)+1):
  zz=[z for z in range(s['from_z'],s['to_z']+1) if (x,120,z) in coords]
  run.append(max(zz) if zz else None)
 checks.append({'name':s['name'],'anchors':anchors,'centerline_support_gap_count':sum(z is None for z in run),'support_gap_x':[min(a,b)+i for i,z in enumerate(run) if z is None],'max_adjacent_tread_height_cells':max(abs(v-u) for u,v in zip(run,run[1:]) if u is not None and v is not None)})
mask=np.zeros((800,241,53),bool)
for x,y,z in shell:
 if z<=52:mask[x,y,z]=True
water=np.zeros_like(mask);water[0,:,:]=True;water[-1,:,:]=True;water[:,0,:]=True;water[:,-1,:]=True;water[:,:,0]=~mask[:,:,0]
wet=binary_propagation(water,structure=generate_binary_structure(3,1),mask=~mask)
probe={str(q):bool(wet[q]) for q in ((350,120,30),(350,100,30),(400,120,40),(250,120,40))}
out={'shell_cells':len(shell),'part_cells':{k:len(v) for k,v in parts.items()},'shell_underwater_outside_flood_probes_wet':probe,'stairs':checks}
Path(__file__).with_name('decks_metrics.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out,indent=2))
