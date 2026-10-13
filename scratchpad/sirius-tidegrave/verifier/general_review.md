# Tidegrave REV01 independent general arrangement review

Result: MINOR for concept/general arrangement; MAJOR if used as construction acceptance without the outstanding layout sheets below.

Read-only review of plan.json, draft_general.py, general_arrangement.png, verify_general.json, and the three provided D23/Walt Disney Archives reference photographs. No author checker was imported. Author files and sculpture were not modified. Independent metrics are in independent_metrics.json.

## PASS

- Hull span is 620-100=520 cells = 52.0 m. At image y1500, stern and bow ink runs are x353..356 and x1731..1734. Their centre separation is 1378 px; 1378/2.65*0.1 = 52.0 m.
- Main mast top ink is y248. Relative to datum y1600, this reads 510.189 cells = 51.019 m, within one raster pixel of the specified 51.0 m.
- Fore, main and mizzen roots lie on their declared deck ranges: fore510/weather100..618, main355/weather100..618, mizzen205/quarter100..240. The bowsprit tip x748 and mast z510 fit inside the 800x241x640 cell work volume.
- Broadside stations are twelve per side per deck, producing 48 broadside guns. Adjacent ports at 32-cell spacing with 16-cell width leave 16 cells of sidewall between ports. Lower port z70..84 sits above DWL52 by 1.8 m at its sill; upper port z95..109 stays below weather115. These are internally consistent coordinates.
- Provenance separates historical references from invented lines, deck heights, supported game gun codes and fixed triple visual clusters. It explicitly withholds hydrostatic/stability acceptance. This boundary is appropriate.
- Three masts, high stepped stern, low forward beak, aged torn ochre canvas and coral/gothic ornament intentions match identifiable reference features. The close-up really shows triangular triple-barrel clusters, and the stern image supports coral branches, tall arched ribs and projecting gallery.

## MINOR corrections before freezing the general sheet

1. Actual maximum beam from the stated hull law is 12.99996 m at x360,z55, not 13.4 m. The 13.4 m figure is twice the nominal station parameter before bilge shrink/tumblehome. At DWL the beam is 12.92608 m; at weather115 it is 10.57489 m. Label physical maximum 13.0 m, and retain 13.4 only if explicitly labelled nominal shaping parameter.
2. The weather outline is drawn at z115 while cannon rectangles use z90. Several rectangles visibly extend outside the weather outline. This can be an overlay, but the legend should explicitly say 'upper gun deck overlay' or render a separate z90 gun-deck outline.
3. The side elevation draws eight sail trapezoids (3 fore + 3 main + 2 mizzen). Historical ten sails are source context and not promised final count, so this is not a count failure. However, those side-view trapezoids are longitudinal depth symbols, not full transverse sail size. No sail area or true yard span can be measured from this sheet. Label rig schematic and defer to a proper rig plan.
4. The museum width ratio should be stated as design context, not direct geometric derivation: this hull law is original, as the provenance correctly says.

## MAJOR outstanding construction inputs

1. Six bow chase guns have counts/codes but no XYZ, orientation, mounting decks, clear muzzle openings, recoil/access envelopes or collision check against bowsprit root. A depicted triple battery must receive a separate bow/frontal layout before installation. A count-only spec is insufficient.
2. Decks occupy long flat planes but the claimed walkable passages/ladders are not coordinate-specified. The two drawn hatch rectangles at x275 and410 have no matching hole/deck/ladder data in plan.json. Powder magazines have x/z limits but no y limits or access separation. A deck-access sheet must resolve these before interior construction acceptance.
3. Stern 'three tier galleries, gothic arch, coral crown' is currently intent and seven thin spikes atop a rectangular stern. The film reference's projected curved gallery and arched rib silhouette are not yet geometrically defined. Detail sheet is needed to prevent a generic stepped box stern during build.

## Verification limitation

The author's verify_general.json is derived from the same width law and renderer. Its 'calibration_shift' is an arithmetic shift of the measuring datum by 3*scale, which necessarily returns3; it is not evidence that an intentionally displaced geometric element was independently detected. Our pixel readings above are separate observations of the rendered image, and our beam calculation exposes the nominal-vs-physical discrepancy. Hydrostatics, supported game metadata, mesh collision and walkability remain build-stage checks.
