# Tidegrave updated general arrangement independent review

Stage: general arrangement, not construction completion.

Verdict: PASS WITH MINOR CORRECTIONS. No blocking major finding for this stage. This supersedes the original general-stage beam finding; remaining construction acceptance inputs from the original report remain deferred checks rather than failures of stage0.

Read newest plan.json, draft_general.py and general_arrangement.png without importing/executing the author program. Independently recomputed the geometric law with ordinary Python/math; results saved as independent_metrics_v2.json. No author files or sculpture modified.

## Passed revisions

- Width normalization now gives exactly 13.4 m continuous maximum beam at the midpoint of the section at z55. Sampling the integer x/z grid gives13.399145 m, a negligible coordinate discretization difference.
- Rake endpoints at DWL z52 are x123.75 and584.375, giving46.0625 m waterline span. At z128 they are100/620, giving52.0 m upper hull envelope. At z0 they are140/560; these are extrapolated rake limits, not actual bottom endpoints because the rising floor masks the ends. The updated side image visibly shows the angled stems and rising floor rather than the prior rectangular stem outline.
- Six bow guns now have XYZ/yaw positioning. The two clusters are mirror-symmetric about y120. Closest upper gun centre is1.2 m from the centreline; that supports reserving central space for the bowsprit, but is not a model-bounds collision certificate.
- Weather/gun-deck overlay is now labelled explicitly, resolving the mistaken interpretation of rectangles crossing the narrower weather outline.
- Overall dimensional and provenance limits remain correct for a designed game asset; the sheet still clearly says not construction acceptance.

## Minor corrections

1. Chase notes say 'lower two barrels and one top barrel', while each cluster's base_positions has one gun at z119 and two at z127. The actual layout is lower-one/upper-two and matches the inspected movie bow photograph's triangular arrangement. Correct the note to match coordinates.
2. Flat deck lines in the side image are still drawn all the way from x100 to618, crossing the raked-end void. At z65 the shell domain begins119.6875 and ends590.46875; at z90 it begins111.875 and ends602.1875; at z115 it begins104.0625 and ends613.90625. Trim the drawn deck lines to the actual hull or label deck x limits as outer bounding ranges clipped by hull domain. Construction must apply that clipping.
3. Plan revision and image still say REV01 after material geometry updates. Keep an explicit version/change record so a later verifier can identify which file state was accepted.

## Explicitly deferred beyond this stage

Model-bound muzzle/bowsprit collision, deck hole/ladder/access geometry, magazine y limits, stern gallery/crown detail, true rig spans/sail areas, and game hydrostatics. The author accepted replacing the datum-only calibration with a true geometric perturbation test; current draft code still contains the old datum control, so treat it as withdrawn and do not cite it as an independent perturbation proof.
