import json
from pathlib import Path
R=Path('D:/Unity/Valhalla/Sculpture/works');BASE='sirius-tidegrave-01m'
def replay(w):
 v={};history=[]
 for f in sorted((R/w/'events').rglob('*.json')):
  e=json.loads(f.read_text(encoding='utf-8'));before=dict(v) if e['op']=='carve' else None
  for x,y,z,c in e.get('placed_colored',[]):v[x,y,z]=c
  for q in e.get('carved_voxels',[]):v.pop(tuple(q),None)
  if before is not None:history.append({'event':f.name,'removed':len(before)-len(v),'retained_color_changes':sum(v.get(k)!=c for k,c in before.items() if k in v)})
 return v,history
hull,hist=replay(BASE);coords=set(hull)
for w in ('lower','upper','weather','quarter','poop','forecastle'):
 v,_=replay(BASE+'-deck-'+w);coords.update(v)
ladders,_=replay(BASE+'-ladders');coords.update(ladders)
plan=json.loads((R/BASE/'design/plan.json').read_text(encoding='utf-8'));rep=json.loads((R/BASE/'design/verify_decks.json').read_text(encoding='utf-8'))
rays=[{'x':x,'z':z,'blocked_y':[y for y in range(241) if (x,y,z) in hull]} for x in plan['guns']['x'] for z in (77,102)]
stairs=[]
for s in rep['stairs']:
 xs=[p[0] for p in s['points'].values()];lo=s['from_z'];hi=s['to_z']
 gaps=[x for x in range(min(xs),max(xs)+1) if not any((x,120,z) in coords for z in range(lo,hi+1))]
 anchors={k:{'air':tuple(q) not in coords,'support':(q[0],q[1],q[2]-1) in coords,'vertical20_clear':all((q[0],q[1],q[2]+dz) not in coords for dz in range(20))} for k,q in s['points'].items()}
 stairs.append({'name':s['name'],'gap_x':gaps,'anchors':anchors})
out={'scope':'hull + six decks + ladders; later rig excluded','hull_cells':len(hull),'carve_history':hist,'gun_rays':rays,'ladder_cells':len(ladders),'stairs':stairs}
Path(__file__).with_name('corrections_metrics.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print('Hull',len(hull),'ladder',len(ladders),'blocked rays',sum(bool(r['blocked_y']) for r in rays),'gaps',[(s['name'],s['gap_x']) for s in stairs],'anchor failures',sum(not all(a.values()) for s in stairs for a in s['anchors'].values()),'carves',hist)
