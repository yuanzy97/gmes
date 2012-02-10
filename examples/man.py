#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, datetime
new_path = os.path.abspath('../')
sys.path.append(new_path)

from datetime import datetime
print os.uname()
print 'python version:', sys.version
start_time = datetime.now()

from numpy import cross
from gmes import material, geometry, fdtd, source, constant, pw_material

space = geometry.Cartesian(size=(6,6,6), resolution=10)
body = geometry.Block(material.Dielectric(1), size=(1,1,2))
head = geometry.Sphere(material.Dielectric(2), radius=0.5, center=(0,0,-1.5))
hat = geometry.Cone(material.Dielectric(3), axis=(0,0.2,-1), radius=0.7,
                    height=0.5, center=(0,0.2,-2.15))
leg1 = geometry.Cylinder(material.Dielectric(4), axis=(0,-0.2,-1),
                         radius=0.2, height=2, center=(0,0.5,+2))
leg2 = geometry.Cylinder(material.Dielectric(5), axis=(0,0.2,-1),
                         radius=0.2, height=2, center=(0,-0.5,2))
arm1 = geometry.Ellipsoid(material.Dielectric(6),
                          e1=(1, 0, 0), e2=(0, 1, -1), e3=cross((1, 0, 0), (0, 1, -1)),
                          size=(0.5, 0.5, 1.5), center=(0, 1.3, -0.2))
arm2 = geometry.Ellipsoid(material.Dielectric(7),
                          e1=(1, 0, 0), e2=(0, 1, 1), e3=cross((1, 0, 0), (0, 1, 1)),
                          size=(0.5, 0.5, 1.5), center=(0, -1.3, -0.2))
geom_list = (geometry.DefaultMedium(material.Dielectric(10)),
             body, head, hat, leg1, leg2, arm1, arm2)

my_fdtd = fdtd.FDTD(space, geom_list, ())

import cProfile, pstats
cProfile.runctx('my_fdtd.init()', globals(), locals(), 'man.prof')
s = pstats.Stats('man.prof')
s.strip_dirs().sort_stats('time').print_stats()

my_fdtd.show_permittivity_ex(axis=constant.X, cut=0)
my_fdtd.show_permittivity_ex(axis=constant.Y, cut=0)
my_fdtd.show_permittivity_ex(axis=constant.Z, cut=0)