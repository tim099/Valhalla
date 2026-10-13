import json, collections
from pathlib import Path
from PIL import Image
R=Path('D:/Unity/Valhalla/Sculpture/works/sirius-tidegrave-01m')
files=sorted((R/'events').rglob('*.json'))[:4]
actual={};old=None;deleted=set();added=set()
for i,f in enumerate(files):
 e=json.loads(f.read_text(encoding='utf-8'))
 if e['op']=='stampvox':
  for x,y,z,c in e['placed_colored']:actual[x,y,z]=c
 elif e['op']=='carve':
  for xyz in e['carved_voxels']:deleted.add(tuple(xyz));actual.pop(tuple(xyz),None)
 if i==1:old=dict(actual)
 if i==3:added={tuple(v[:3]) for v in e['placed_colored']}
expected={tuple(v[:3]):v[3] for line in (R/'design/skeleton.vox.txt').read_text().splitlines() if (v:=list(map(int,line.split(','))))}
coords=set(actual);remaining=set(coords);components=[]
while remaining:
 s=remaining.pop();q=[s];n=0
 while q:
  x,y,z=q.pop();n+=1
  for k in ((x-1,y,z),(x+1,y,z),(x,y-1,z),(x,y+1,z),(x,y,z-1),(x,y,z+1)):
   if k in remaining:remaining.remove(k);q.append(k)
 components.append(n)
projection={(x,z) for x,y,z in coords}
im=Image.open(R/'design/skeleton_cell_plan.png').convert('RGB'); bg=im.getpixel((0,0))
pixels={(x,im.height-1-y) for y in range(im.height) for x in range(im.width) if im.getpixel((x,y))!=bg}
shifted={(x+3,z) for x,z in projection}
out={'events_replayed':[f.name for f in files],'actual_voxels':len(actual),'missing_or_color':sum(actual.get(k)!=v for k,v in expected.items()),'extra':len(coords-set(expected)), 'old_voxels':len(old),'carved_count':len(deleted),'carve_only_old_extras':deleted==set(old)-set(expected),'retained_old_expected_unchanged':all(actual.get(k)==v for k,v in old.items() if k in expected),'added_exact_missing':added==set(expected)-set(old),'components_6':sorted(components,reverse=True),'mirror_missing_or_color':sum(actual.get((x,240-y,z))!=c for (x,y,z),c in actual.items()),'bbox':[[min(k[j] for k in coords),max(k[j] for k in coords)] for j in range(3)],'cell_png_size':im.size,'png_projection_missing':len(projection-pixels),'png_projection_extra':len(pixels-projection),'negative_geometry_shift_x':3,'negative_measured_left_bound_shift':min(x for x,z in shifted)-min(x for x,z in pixels),'negative_symmetric_pixel_difference':len(shifted^pixels)}
Path(__file__).with_name('skeleton_metrics.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out,indent=2))
