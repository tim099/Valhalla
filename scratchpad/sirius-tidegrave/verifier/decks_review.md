# Tidegrave stage2 shell and stage3 deck/stair independent review

Verdict at the inspected event state: MAJOR, two geometry corrections required. This report precedes any later repair.

Read-only independent event replay of hull work and all enabled, zero-transform assembly child links. No author checker imported. Shell state has668008 cells. Assembly has six deck parts with85212/81346/68684/14932/5228/3164 cells and ladders15567; combined942141 cells, matching CLI stats0165. Independent measurements are in decks_metrics.json.

## MAJOR1: gun-port centres blocked by retained ribs

At all12 gun x stations and both centre heights z77 and102, both broadside wall centre rays contain3 consecutive solid cells even though the new shell port was removed. Thus all48 port centres are obstructed by retained skeleton rib wood. Examples:

- x335,z77: y58..60 and180..182.
- x335,z102: y63..65 and175..177.
- x175,z77: y78..80 and160..162.

This is stage2 geometry, not missing future cannon installation. Cut the intended port domain through the combined old ribs and new shell, then verify complete muzzle clearance against actual model bounds during cannon stage. Record the carve as an intentional skeleton revision rather than preserving a previous_changed=0 claim.

## MAJOR2: four stair entrances retain a0.2m support gap

All28 named foot/lo/hi/head samples are empty air with a solid cell directly below, and all have20cells of vertical centreline headroom. However, point samples hide the gap between low deck and first tread:

- lower-upper-a and upper-weather-a: x308,309 at y120 have no solid support anywhere between their declared from_z/to_z.
- lower-upper-b and upper-weather-b: x443,444 at y120 have the same defect.
- The a hatch ends309; deck begins310. Lowest tread ends307. Hence the two-column break. The b route is shifted+135.

Add a low landing bridge across the uncovered columns to join the first tread to the deck; recheck a continuous supported route, not just four anchors. The three exterior upperdeck stairs have no support gap in the same test.

## Passed readings

- Underwater exterior floodfill using six-neighbour adjacency at z<=52 cannot reach internal air probes(350,120,30),(350,100,30),(400,120,40),(250,120,40). These four probes remain dry. This supports the shell's below-DWL closure; not a hydrostatic balance certificate.
- All28 stair anchors have air/solid-below/2m vertical headroom as stated above.
- Assembly links are enabled, at0,0,0 with no rotation/mirror; CLI reports overlap0,clipped0,one structural component and mirror differences0. Structural connectivity does not prove the walking route across the four inlet gaps.

## Limits

5x5x20 body boxes at lo touch an adjacent rising tread, so that broad box test alone is not classified as an extra defect. The max-height-per-x probe also samples overhead deck surfaces; its large height-jump outputs are not used as stair slope evidence. Actual game collision capsule/step allowance, cannon firing range and shell drawing negative-control result were not independently measured in this turn; do not label these verified. Future masts and guns are outside stage3 scope and not counted as missing stage3 work.
