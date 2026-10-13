# Tidegrave rig independent review

Verdict: MINOR geometry/control metadata findings; no new blocking major certified by this limited sample. Known bowsprit stump and flag-pole work are excluded from new findings.

Obtained actual OBJ through read-only senate export into verifier/rig_actual.obj and parsed its vertices/object groups independently. Did not import author checker or builder. Export witness:988805 voxel cells,195 ropes,10 sail objects,10 models; all broken/hidden/disabled counters0. OBJ has12 sail meshes because the ensign contributes3 meshes. The sail JSON contains9 working sails plus1 flag, not10 working propulsion sails.

## Minor findings

1. Sheet metadata exists for14 ropes covering7 square sails, but none for mizzen-lateen or jib. Thus those two working sails have no tagged controlling sheet in current ropes.json. Add correctly named sheet ropes and meta before sail-handling acceptance; exact game response is unverified here.
2. Lowest ratlines intersect solid sidewall/bulwark voxels, beyond intentional single-point chain attachments. Actual OBJ vertex samples map into hull cells at mizzen port ratline1:(186,84,135),(224,78,135); ratline2 reaches z140/141; ratline3 reaches145/146. Main ratline1 hits z122, fore ratline1/2 hit121/128. These are lower than the respective wall tops. Move the lowest cross-ratlines above the local wall or explicitly terminate a lower ladder/chainplate outside the hull. Several brace ends also cross multiple hull cells near chain anchor, suggesting wall-routing checks before declaring rig collision-free.

## Passed actual readings

- Sail exported vertex samples have0 hits against hull voxel occupancy. Mast intersections are limited to the sail's top/attachment vicinity: e.g.fore-course at(510,120,235),(513,119,230),main-course at(355,120,250),(358,119,246). These are not treated as a new major because the mast/yard attachment lives there.
- All10 model parts export without broken refs. Three course/topgallant pairs and mizzen crossjack/topsail are at scale[1,1,1], rotation z=-18, pivot4.5/120.5/4.5. Gaff/boom have separate120.5/120.5/180.5 pivots and rotate0. Rig plan only lists8 horizontal yards; the2 mizzen gaff/boom models are nevertheless present in actual models.json/export.
- Yard metadata lengths use correct0.1m/cell to feet conversion, e.g210cells=21m=68.90ft. Diameter metadata11.81in refers0.3m; generated course yard radius1.6cells allows about0.32m continuous diameter before voxel discretization. This is an approximation, not a severe scale mismatch.

## Explicit limits

This is vertex-in-voxel sampling of actual OBJ after mapping exporter x,z,y back to sculpt x,y,z; continuous triangle intersections, entire swept cloth animation, rope tube interiors, ladder clearance against every triangle and hydrodynamics were not certified. No shifted rig export was available, so a rig-specific negative asset-offset control is unverified. Earlier skeleton's true3cell test does not automatically validate rig meshes. Bow stump repair and flag pole are known author work and intentionally not re-reported as new major.

Raw collision samples and bounds are in rig_metrics.json; code is check_rig_independent.py.
