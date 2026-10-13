# Stage5 weapons independent review

Verdict: PASS for measured weapon placement, structural collision and muzzle clearance. No blocking major found.

Read actual six linked deck model/part files and source voxel caches independently, without importing author checker/builder. Solid collision state includes all enabled assembly voxel links, including three masts, bowsprit, ladder and chase cradle. Exact inspected watermarks are saved in guns_metrics.json: hull ends232425_095_e7d450.json and bowsprit ends232420_234_84207f.json, after the described structure-fit repairs.

## Independent geometry evidence

-54 actual gun models:48 borrowed basecamp-frigate-constitution-01m-gun-24 at scale[1,1,1],6 own chase-tube at[.5,.5,.5]. Read real pivot/at/rotation from deck models.json, not author verify_guns.json.
- Rotations are0,180,-90deg about z, so source voxel cubes remain axis-aligned after transform. For every source voxel, transformed all8 corners, obtained exact world box, enumerated overlapped world solid voxels using strict interior bounds; surface touching excluded. All54 models have0 positive-volume collisions against assembly solid voxels. This checks complete source cubes rather than centres alone.
- Transformed muzzle and breech from source anchors at cell centre(anchor+.5). Each54 muzzle-to-outboard ray, sampled every.5cell for200cells(20m), hits0 solid assembly voxels. This certifies sampled outboard structural clearance, not ballistic range.
- Example broadside S01: muzzle175.5,167,77.5; breech175.5,139,77.5; barrel axis length2.8m. P01 reverses direction consistently.
- Example chase1: muzzle615.75,103.5,125.25; breech587.25,103.5,125.25; axis length2.85m. Other5 share+X direction and paired triangular placement. Source cache bounds7..17,2..60,7..17 and half scale are consistent with the transformed dimensions.

## Earlier rig findings

Current ropes.json now contains kind=sheet,sail=jib and kind=sheet,sail=mizzen-lateen. The prior two-sail missing-sheet metadata finding is closed. Chain relocation was observed as author work but the old ratline wall contact was not re-exported/retested in this limited weapon check, so mark that geometric closure unverified here.

## Limits

Source/current voxel caches were read as engine state rather than independently replaying all historical source events; their current event watermarks are retained in the evidence. Pairwise gun-vs-gun volumetric intersection, ropes/cloth-vs-gun mesh intersection, moving recoil envelope, game firing logic/ballistic range, and rig-specific shifted-asset negative control are not certified by this check. The outward20m clear-ray measurement is geometry extent, not gun range. Known floating-cell/bowsprit overlap repairs are not re-reported as new majors.

Evidence: guns_metrics.json. Independent code: check_guns_independent.py.
