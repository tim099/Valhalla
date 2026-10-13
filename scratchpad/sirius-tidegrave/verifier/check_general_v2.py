import json, math
from pathlib import Path
R=Path('D:/Unity/Valhalla/Sculpture/works/sirius-tidegrave-01m/design')
p=json.loads((R/'plan.json').read_text(encoding='utf-8'));h=p['hull']
def ends(z):
 f=max(0,1-z/h['rake_height']);return h['stern_x']+h['stern_rake']*f,h['bow_x']-h['bow_rake']*f
def rad(x,z):
 lo,hi=ends(z);t=(x-lo)/(hi-lo)
 if not 0<=t<=1:return 0
 b=h['stations'][-1][1]
 for a,c in zip(h['stations'],h['stations'][1:]):
  if a[0]<=t<=c[0]:b=a[1]+(c[1]-a[1])*(t-a[0])/(c[0]-a[0]);break
 floor=h['floor_base']+h['floor_end_rise']*abs(2*t-1)**3
 if z<=floor:return 0
 return b*math.sqrt((1-math.exp(-(z-floor)/h['bilge_height']))/(1-math.exp(-(h['tumblehome_start']-h['floor_base'])/h['bilge_height'])))*max(.48,1-h['tumblehome_per_z']*max(0,z-h['tumblehome_start']))
out={'stage':'general_only','integer_grid_max_beam_m':max(2*rad(x,z)*.1 for x in range(100,621) for z in range(5,187)),'exact_midsection_max_beam_m':2*rad(sum(ends(55))/2,55)*.1,'rake_endpoints':{str(z):ends(z) for z in (0,22,52,65,90,115,128)},'chase_base_symmetric':all((x,240-y,z) in [tuple(v) for v in p['guns']['chase_layout']['base_positions']] for x,y,z in p['guns']['chase_layout']['base_positions']),'chase_nearest_centerline_y_gap_m':min(abs(y-120)*.1 for x,y,z in p['guns']['chase_layout']['base_positions'])}
Path(__file__).with_name('independent_metrics_v2.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out,indent=2))
