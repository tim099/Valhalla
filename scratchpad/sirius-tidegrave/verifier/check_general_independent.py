import json, math
from pathlib import Path
from PIL import Image
R=Path('D:/Unity/Valhalla/Sculpture/works/sirius-tidegrave-01m/design')
p=json.loads((R/'plan.json').read_text(encoding='utf-8')); h=p['hull']
def radius(x,z):
    t=(x-h['stern_x'])/(h['bow_x']-h['stern_x'])
    ss=h['stations']; b=ss[-1][1]
    for a,c in zip(ss,ss[1:]):
        if a[0]<=t<=c[0]: b=a[1]+(c[1]-a[1])*(t-a[0])/(c[0]-a[0]);break
    f=h['floor_base']+h['floor_end_rise']*abs(2*t-1)**3
    if z<=f:return 0
    return b*math.sqrt(1-math.exp(-(z-f)/h['bilge_height']))*max(.48,1-h['tumblehome_per_z']*max(0,z-h['tumblehome_start']))
beam=max((2*radius(x,z)*.1,x,z) for x in range(100,621) for z in range(5,187))
im=Image.open(R/'general_arrangement.png'); ink=(217,226,208)
# Pixel segments: mast at x=355, keel line at x=360, stem vertical lines, no author helpers imported.
mx=round(90+355*2.65)
mast_top=min(y for y in range(200,1350) if im.getpixel((mx,y))==ink)
stem_px=[]
for x in range(2300):
    if im.getpixel((x,1500))==ink:stem_px.append(x)
out={'independent_checker':True,'author_module_imported':False,
 'actual_max_beam_m':beam[0],'beam_peak_xz':[beam[1],beam[2]],
 'weather_beam_at_x360_m':2*radius(360,115)*.1,
 'dwl_beam_at_x360_m':2*radius(360,52)*.1,
 'mast_top_y_pixel':mast_top,'mast_top_z_from_pixels':(1600-mast_top)/2.65,
 'stem_pixels_at_y1500':stem_px,'stem_span_m_from_pixels':(max(stem_px)-min(stem_px))/2.65*.1,
 'lower_gun_port_z':[70,84],'upper_gun_port_z':[95,109],
 'lower_port_sill_freeboard_m':(70-52)*.1,
 'between_decks_m':2.5,'clear_height_with_4cell_deck_m':2.1,
 'broadside_gun_count':len(p['guns']['x'])*len(p['guns']['decks'])*2,
 'chase_coordinates_provided':False,'ladder_coordinates_provided':False,
 'rig_sails_drawn_count':8}
Path(__file__).with_name('independent_metrics.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
