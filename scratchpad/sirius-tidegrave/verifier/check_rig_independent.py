import json, math
from pathlib import Path
import numpy as np
R=Path('D:/Unity/Valhalla/Sculpture/works');A=R/'sirius-tidegrave-01m-assembly';OUT=Path(__file__).parent
def replay(w):
 v=set()
 for f in sorted((R/w/'events').rglob('*.json')):
  e=json.loads(f.read_text(encoding='utf-8'));v.update(tuple(t[:3]) for t in e.get('placed_colored',[]));v.difference_update(tuple(t) for t in e.get('carved_voxels',[]))
 return v
shell=replay('sirius-tidegrave-01m');masts=set().union(*(replay('sirius-tidegrave-01m-mast-'+m) for m in ('fore','main','mizzen')))
vertices=[];groups={};g=None
for line in (OUT/'rig_actual.obj').read_text(encoding='utf-8').splitlines():
 if line.startswith('v '):
  x,z,y=map(float,line.split()[1:4]);vertices.append((x,y,z))
 elif line.startswith('o '):g=line[2:];groups[g]=set()
 elif line.startswith('f ') and g:
  groups[g].update(int(v.split('/')[0])-1 for v in line.split()[1:])
reports=[]
for g,ii in groups.items():
 if not g.startswith(('rope_','sail_')):continue
 pts=[vertices[i] for i in ii];shellhits=[];masthits=[]
 for p in pts:
  q=tuple(math.floor(n) for n in p)
  if q in shell:shellhits.append(q)
  if q in masts:masthits.append(q)
 reports.append({'object':g,'vertex_count':len(pts),'bounds':[[min(p[j] for p in pts),max(p[j] for p in pts)] for j in range(3)],'shell_vertex_hits':len(set(shellhits)),'shell_examples':list(set(shellhits))[:5],'mast_vertex_hits':len(set(masthits)),'mast_examples':list(set(masthits))[:5]})
sails=json.loads((A/'sails.json').read_text())['sails'];ropes=json.loads((A/'ropes.json').read_text())['ropes'];sheets={r.get('meta',{}).get('sail') for r in ropes if r.get('meta',{}).get('kind')=='sheet'}
out={'method':'actual exported OBJ vertex samples mapped x,z,y back to sculpt x,y,z; no continuous triangle intersection certificate','sails_without_sheet':[s['name'] for s in sails if s.get('meta',{}).get('kind')=='sail' and s['name'] not in sheets],'objects_with_shell_hits':[r for r in reports if r['shell_vertex_hits']], 'sails_with_mast_hits':[r for r in reports if r['object'].startswith('sail_') and r['mast_vertex_hits']],'all_meshes':reports,'negative_control':'unverified, no shifted rig export provided'}
(OUT/'rig_metrics.json').write_text(json.dumps(out,indent=2)+'\n');print('missing sheet',out['sails_without_sheet']);print('shell hits',[(r['object'],r['shell_vertex_hits'],r['shell_examples']) for r in out['objects_with_shell_hits']]);print('sail mast hits',[(r['object'],r['mast_vertex_hits'],r['mast_examples']) for r in out['sails_with_mast_hits']])
