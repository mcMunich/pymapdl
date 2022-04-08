# -*- coding: utf-8 -*-


from ansys.mapdl.core import launch_mapdl

# parameters
x = 1 # create a square block
f = 1e6 # force over 1 side of block
ndiv = 4 # element/line division
numElem = (ndiv/x)**3
loadDirection = 'y'

##### modeling
elemSize = (x**3)/numElem**(1/3)

#### Launch pymapdl
mapdl = launch_mapdl()
mapdl.prep7()

#### Materials
mapdl.mp("EX", 1, 200e9)
mapdl.mp("PRXY", 1, 0.3)

#### Geometry
mapdl.csys(0)
mapdl.blc4(0, 0,x, x, x)

#### Elements and meshing
mapdl.et(1, "SOLID186")
mapdl.type(1)
mapdl.keyopt(1, 2, 1)
mapdl.esize(elemSize)
mapdl.vmesh("ALL")
mapdl.eplot()

#### Boundary Conditions: fixed constraint
mapdl.nsel("s", "loc", loadDirection, 0)
mapdl.d("all", "all")

#### Boundary Conditions: load
mapdl.nsel("s", "loc", loadDirection, x)
nnodes = mapdl.get("NumNodes" , "NODE" ,0 , "COUNT" )
mapdl.f("all", "fy",f/nnodes)
mapdl.allsel()

#### Solve
mapdl.run("/solu")
sol_output = mapdl.solve()

#### Plot Results
# plot the normalized global displacement
mapdl.post_processing.plot_nodal_displacement(lighting=False, show_edges=True)
mapdl.post1()
mapdl.set(1,1)
result = mapdl.result

result.plot_principal_nodal_stress(0, 'SEQV', lighting=False, background='w', show_displacement=True, displacement_factor = 10.0, show_edges=True, text_color='k', add_text=False)
nnum, stress = result.principal_nodal_stress(0)

# Generate a list of non mid side node results (filter out nan-s)
tabularResults_VonMises = [[a,b] for a, b in zip(nnum, stress[:, -1]) if str(b) != 'nan' ]

mapdl.exit()


