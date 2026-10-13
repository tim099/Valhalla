# Tidegrave skeleton v2 independent review

Verdict: PASS for skeleton stage. No actionable major/minor discrepancy found in the checked stage state.

Scope is the event watermark230136_710_bc4cb9.json. Only the first four events were replayed, ending with the11310-cell correction. Later shell events/current cache were deliberately excluded. No author checker was imported, no author module executed, and no sculpture or author file was modified. Independent code and raw metrics are check_skeleton_independent.py and skeleton_metrics.json beside this report.

## Event witness and correction safety

- Original stamps:744 +275969 =276713 cells.
- Carve:169618 coordinates. This set is exactly original-state coordinates minus final expected skeleton coordinates. No desired coordinate was carved.
- Addition:11310 coordinates. This set is exactly expected skeleton coordinates minus original-state coordinates.
- Final replay:118405 cells. Against skeleton.vox.txt: missing-or-wrong-color0, extra0. Every retained original expected cell still has its original color.
- These are independently reproduced from event contents, not inferred from verify_skeleton.json.

## Geometry

- Independent six-neighbour traversal yields exactly one component of118405 cells.
- Mirror y120 gives0 absent-or-different-color cells.
- Occupied bounds: x105..617, y54..186, z0..129; all fit the800x241x640 workspace.
- CLI log0013_stats_.txt independently reports118405 cells, one component, no mirror difference and zero cavities. The component/mirror values were independently reproduced here; zero cavities was corroborated from the CLI witness only, not independently flood-filled.

## Drawing and actual image measurements

- skeleton_cell_plan.png is800x200. Reading every non-background pixel and mapping image-row to z gives exact agreement with the actual event state's x/z projection: missing0, extra0.
- skeleton_side.png is2400x1968. Its olive body pixels bound x315..1853 and image-row1530..1919. This gives1539x390 pixels, exactly513x130 occupied coordinate cells at3pixels/cell, matching event x105..617 and z0..129. Thus actual side envelope is51.3m in occupied-cell extent and13.0m high; this is a skeleton-state extent, not a contradiction of the planned52m completed upper hull.
- Personally inspected yaw45 rendering: frames are open, connected through keel structure, and show coherent bilge curves; no visually detached frame was observed. This visual observation is backed by the independent component check.

## True negative control

Constructed a separately shifted set from actual stage voxel coordinates with x+3, keeping the original drawing image and its origin fixed. Measured left boundary changes from105 to108, hence3cells(0.3m). Pixel symmetric difference is9640. This is a geometric perturbation rather than a measuring-datum change and would reject the shifted asset.

## Unverified/not applicable at this stage

Hydrostatics, cannon firing range, cannon collision/access, deck walkability, rig and stern ornament are not present in skeleton stage and were not certified. Source originality and movie similarity beyond the skeleton silhouette remain covered by the general-stage review and later detail stages.
