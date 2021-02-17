import gmsh
import sys
import math


gmsh.initialize(sys.argv)

gmsh.model.add("lab_1_1")

lc = 0.03


def create_circle(x, y, z, r, lc_input):
    p1 = gmsh.model.geo.addPoint(x, y, z, lc_input)
    p2 = gmsh.model.geo.addPoint(x + r, y, z, lc_input)
    p3 = gmsh.model.geo.addPoint(x, y + r, z, lc_input)
    p4 = gmsh.model.geo.addPoint(x - r, y, z, lc_input)
    p5 = gmsh.model.geo.addPoint(x, y - r, z, lc_input)

    c1 = gmsh.model.geo.addCircleArc(p2, p1, p3)
    c2 = gmsh.model.geo.addCircleArc(p3, p1, p4)
    c3 = gmsh.model.geo.addCircleArc(p4, p1, p5)
    c4 = gmsh.model.geo.addCircleArc(p5, p1, p2)

    return gmsh.model.geo.addCurveLoop([c1, c2, c3, c4])


def create_hollow_torus(x, y, z, r1, r2, R, lc_input):
    l1 = create_circle(x - R, y, z, r1, lc_input)
    l2 = create_circle(x - R, y, z, r2, lc_input)
    s1 = gmsh.model.geo.addPlaneSurface([l1, l2])
    ov1 = gmsh.model.geo.revolve([(2, s1)], x, y, z, 0, 1, 0, -math.pi / 2)

    ov2 = gmsh.model.geo.revolve([(2, s1)], x, y, z, 0, 1, 0, math.pi / 2)

    l3 = create_circle(x + R, y, z, r1, lc_input)
    l4 = create_circle(x + R, y, z, r2, lc_input)
    s2 = gmsh.model.geo.addPlaneSurface([l3, l4])
    ov3 = gmsh.model.geo.revolve([(2, s2)], x, y, z, 0, 1, 0, -math.pi / 2)

    ov4 = gmsh.model.geo.revolve([(2, s2)], x, y, z, 0, 1, 0, math.pi / 2)
    gmsh.model.geo.addPhysicalGroup(3, [ov1[1][1], ov2[1][1], ov3[1][1], ov4[1][1]], 1)


x = 0
y = 0
z = 0
r1 = 0.1
r2 = 0.05
R = 0.3

create_hollow_torus(x, y, z, r1, r2, R, lc)

ent = gmsh.model.getEntities()
gmsh.model.setVisibility(ent, False)
gmsh.model.setVisibility([(3, 5)], True, True)
gmsh.option.setNumber("Mesh.MeshOnlyVisible", 1)

gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(3)

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
