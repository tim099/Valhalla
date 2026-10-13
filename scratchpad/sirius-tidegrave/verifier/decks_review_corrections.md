# Stage2/3 two-finding correction verification

Verdict: PASS for the two previously reported major findings. Both are closed at the replayed state. This is a limited recheck, not a new whole-ship acceptance.

Independent event replay, with author checker/module excluded. Collision scope is hull, six deck children and ladders; later rig links are excluded as requested.

1. Hull carve event231407_639_50eb5b.json removes exactly6480 cells, leaves661528 hull cells, and changes0 retained colors. At12 gun x positions and both centre heights77/102, scanning all241 y positions now finds0 occupied cells on every full transverse ray. This establishes48 clear side-centre rays and resolves the rib blockage. Actual cannon model envelope remains its own stage check.
2. Latest ladders contain16023 cells, up from15567, hence456 added landing cells. The supported centreline probe between foot and head finds0 unsupported x columns for all seven stairs. Previously empty308/309 and443/444 are now supported. All28 foot/lo/hi/head points remain air, have immediate support below, and have20cells of vertical centreline headroom.

Raw evidence: corrections_metrics.json; independent code: check_corrections_independent.py.
