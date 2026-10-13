# Stage6 equipment and stage7 ornament independent review

Verdict at fresh inspected snapshot: MAJOR findings remain. This report precedes subsequent corrections.

Used fresh read-only CLI parts/OBJ exports rather than older tidegrave_preview.vxk. Snapshot exports1037401 solid voxel cells,116 models,299 ropes. Independently transformed equipment source voxel cubes from actual models.json plus linked offsets, tested strict positive-volume overlap with linked solid voxels. Author checkers/builders were read only, never imported. Raw samples: equipment_metrics.json; source: check_equipment_independent.py.

## MAJOR1 equipment intersects poop stair

- Quarterdeck steering wheel has123 collided structural cells. Examples(188,115,143),(172,115,158),(184,121,148).
- Quarterdeck binnacle has10 collided cells. Example(194,119,141).
- Independently identified all listed examples as occupied by the ladder child, not ornament. These are the quarter-to-poop stair steps/supports. Relocate equipment or route the stair around it, then recheck both model geometry and human passage.

## MAJOR2 current whole structure has two floating strips

Fresh CLI stats measured3 six-connected components, not1: largest1037391 cells; two5-cell strips at x609..613,y114,z133 and x609..613,y126,z133. Mirror differences0 and cavities0. These strips must be connected or precisely removed before structural completion. They may originate from a later bow-gun clearance cut; their presence is a fresh actual reading, not an older ornament-image inference.

## Minor / measured door limit

Magazine doorway spans y17..23 (7cells=.7m) and z2..17 (16cells=1.6m). Both x43/44 wall layers remain solid at z18..22. This does not provide the2m standing clearance used in stair verification. Increase if human access is intended or document its crawl/service role; actual game capsule doorway allowance is unverified.

## Passed equipment and ornament readings

-48 powder-barrel models,24 in each local45x41x24 room, have0 positive-volume collisions with room/ship/other linked solid voxels. Models retain the basecamp source, use.2scale and100lb game inventory metadata, giving2400lb per room. Rooms sit at240/440,100,30 and their floor support probe at all8 pillar tops(x243/281/443/481,y103/137,z29) is solid, immediately below room floorz30. Thus these rooms are not unsupported floating boxes.
- Own rudder and borrowed capstan have0 model-vs-solid collisions in this static check. Wheel/binnacle findings are above.
- Actual OBJ steering-rope vertex samples of all6 named steer-wheel/lead/tiller objects have0 deck voxel hits in the fresh snapshot. This does not certify tube interiors or continuous segment sweep, but no deck-intersection sample can be reported from these actual readings.
- Ornament31745 cells, mirror difference0;2743 ornament cells are face-adjacent to earlier structure. This establishes extensive root contacts, while whole-structure3component result above still prevents completion.
- Personally inspected ornament_bow/stern images against the previously inspected Disney Archives reference photographs. Triple-tier projecting stern galleries, pale gothic arch/coral branches, prow teeth and paired triangular forward barrels are recognisable design borrowings. The broken astrolabe and regularly spaced pale railing finials are original stylisation. It is a new game design inspired by the movie, not an exact miniature reproduction.

## Limits

Did not repeat the previous54-cannon review after crew changes. Powder pairwise barrel-vs-barrel intersection, moving steering-wheel/rudder swept volumes, continuous rope tube/triangle collision and live crew/navigation are unverified. Export snapshot and newer cache reads can diverge during author work; reported stats/components and equipment findings are tied to the stated1037401-cell state and should be rechecked after repair.
