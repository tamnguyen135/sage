r"""
Differentiable maps between differentiable manifolds

The class :class:`DiffMap` implements differentiable maps from an open
subset `U` of a differentiable manifold `M` to some differentiable
manifold `N` over the same topological field `K` as `M` (in most
applications, `K = \RR` or `K = \CC`):

.. MATH::

    \Phi: U\subset M \longrightarrow N


AUTHORS:

- Eric Gourgoulhon, Michal Bejger (2013-2015): initial version

REFERENCES:

.. [1] Chap. 1 of S. Kobayashi & K. Nomizu : *Foundations of Differential Geometry*,
   vol. 1, Interscience Publishers (New York) (1963)
.. [2] Chaps. 2 and 3 of J.M. Lee : *Introduction to Smooth Manifolds*, 2nd ed.,
   Springer (New York) (2013)

"""

#*****************************************************************************
#       Copyright (C) 2015 Eric Gourgoulhon <eric.gourgoulhon@obspm.fr>
#       Copyright (C) 2015 Michal Bejger <bejger@camk.edu.pl>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.manifolds.continuous_map import ContinuousMap

class DiffMap(ContinuousMap):
    r"""
    Differentiable map between two differentiable manifolds.

    This class implements differentiable maps of the type

    .. MATH::

        \Phi: U\subset M \longrightarrow V\subset N

    where `M` and `N` are differentiable manifolds over the same topological
    field `K` (in most applications, `K = \RR` or `K = \CC`), `U` is an open
    subset of `M` and `V` is an open subset of `N`.

    Differentiable maps are the *morphisms* of the *category* of
    differentiable manifolds. The set of all differentiable maps from
    `U` to `V` is therefore the homset between `U` and `V` and is denoted
    by `\mathrm{Hom}(U,V)`.

    The class :class:`DiffMap` is a Sage *element* class, whose *parent*
    class is
    :class:`~sage.manifolds.differentiable.manifold_homset.DiffManifoldHomset`.
    It inherits from the class
    :class:`~sage.manifolds.continuous_map.ContinuousMap` since a
    differentiable map is obviously a continuous one.

    INPUT:

    - ``parent`` -- homset `\mathrm{Hom}(U,V)` to which the differentiable
      map belongs
    - ``coord_functions`` -- (default: ``None``) if not ``None``, must be
      a dictionary of the coordinate expressions (as lists (or tuples) of the
      coordinates of the image expressed in terms of the coordinates of
      the considered point) with the pairs of charts (chart1, chart2)
      as keys (chart1 being a chart on `U` and chart2 a chart on `V`).
      If the dimension of codomain is 1, a single coordinate
      expression can be passed instead of a tuple with a single element
    - ``name`` -- (default: ``None``) name given to the differentiable map
    - ``latex_name`` -- (default: ``None``) LaTeX symbol to denote the
      differentiable map; if none is provided, the LaTeX symbol is set to
      ``name``
    - ``is_isomorphism`` -- (default: ``False``) determines whether the
      constructed object is a isomorphism (i.e. a diffeomorphism); if set to
      ``True``, then the manifolds `M` and `N` must have the same dimension.
    - ``is_identity`` -- (default: ``False``) determines whether the
      constructed object is the identity map; if set to ``True``,
      then `V` must be `U` and the entry ``coord_functions`` is not used.

    .. NOTE::

        If the information passed by means of the argument ``coord_functions``
        is not sufficient to fully specify the differentiable map,
        further coordinate expressions, in other charts, can be subsequently
        added by means of the method
        :meth:`~sage.manifolds.continuous_map.ContinuousMap.add_expr`

    EXAMPLES:

    The standard embedding of the sphere `S^2` into `\RR^3`::

        sage: M = DiffManifold(2, 'S^2') # the 2-dimensional sphere S^2
        sage: U = M.open_subset('U') # complement of the North pole
        sage: c_xy.<x,y> = U.chart() # stereographic coordinates from the North pole
        sage: V = M.open_subset('V') # complement of the South pole
        sage: c_uv.<u,v> = V.chart() # stereographic coordinates from the South pole
        sage: M.declare_union(U,V)   # S^2 is the union of U and V
        sage: xy_to_uv = c_xy.transition_map(c_uv, (x/(x^2+y^2), y/(x^2+y^2)), \
                                             intersection_name='W', restrictions1= x^2+y^2!=0, \
                                             restrictions2= u^2+v^2!=0)
        sage: uv_to_xy = xy_to_uv.inverse()
        sage: N = DiffManifold(3, 'R^3', r'\RR^3')  # R^3
        sage: c_cart.<X,Y,Z> = N.chart()  # Cartesian coordinates on R^3
        sage: Phi = M.diff_map(N, \
        ....: {(c_xy, c_cart): [2*x/(1+x^2+y^2), 2*y/(1+x^2+y^2), (x^2+y^2-1)/(1+x^2+y^2)],  \
        ....:  (c_uv, c_cart): [2*u/(1+u^2+v^2), 2*v/(1+u^2+v^2), (1-u^2-v^2)/(1+u^2+v^2)]}, \
        ....: name='Phi', latex_name=r'\Phi')
        sage: Phi
        Differentiable map Phi from the 2-dimensional differentiable manifold S^2 to
         the 3-dimensional differentiable manifold R^3
        sage: Phi.parent()
        Set of Morphisms from 2-dimensional differentiable manifold S^2 to
         3-dimensional differentiable manifold R^3 in Category of sets
        sage: Phi.parent() is Hom(M, N)
        True
        sage: type(Phi)
        <class 'sage.manifolds.differentiable.diff_map.DiffManifoldHomset_with_category.element_class'>
        sage: Phi.display()
        Phi: S^2 --> R^3
        on U: (x, y) |--> (X, Y, Z) = (2*x/(x^2 + y^2 + 1), 2*y/(x^2 + y^2 + 1), (x^2 + y^2 - 1)/(x^2 + y^2 + 1))
        on V: (u, v) |--> (X, Y, Z) = (2*u/(u^2 + v^2 + 1), 2*v/(u^2 + v^2 + 1), -(u^2 + v^2 - 1)/(u^2 + v^2 + 1))

    It is possible to create the map via the method
    :meth:`~sage.manifolds.differentiable.manifold.DiffManifold.diff_map`
    only in a single pair of charts: the argument ``coord_functions`` is then
    a mere list of coordinate expressions (and not a dictionary) and the
    arguments ``chart1`` and ``chart2`` have to be provided if the charts
    differ from the default ones on the domain and/or the codomain::

        sage: Phi1 = M.diff_map(N, [2*x/(1+x^2+y^2), 2*y/(1+x^2+y^2), (x^2+y^2-1)/(1+x^2+y^2)],
        ....:                   chart1=c_xy, chart2=c_cart, name='Phi', latex_name=r'\Phi')

    Since c_xy and c_cart are the default charts on respectively M and N, they
    can be omitted, so that the above declaration is equivalent to::

        sage: Phi1 = M.diff_map(N, [2*x/(1+x^2+y^2), 2*y/(1+x^2+y^2), (x^2+y^2-1)/(1+x^2+y^2)],
        ....:                   name='Phi', latex_name=r'\Phi')

    With such a declaration, the differentiable map is only partially defined
    on the manifold `S^2`, being known in only one chart::

        sage: Phi1.display()
        Phi: S^2 --> R^3
        on U: (x, y) |--> (X, Y, Z) = (2*x/(x^2 + y^2 + 1), 2*y/(x^2 + y^2 + 1),
         (x^2 + y^2 - 1)/(x^2 + y^2 + 1))

    The definition can be completed by means of the method
    :meth:`~sage.manifolds.continuous_map.ContinuousMap.add_expr`::

        sage: Phi1.add_expr(c_uv, c_cart, [2*u/(1+u^2+v^2), 2*v/(1+u^2+v^2),
        ....:                              (1-u^2-v^2)/(1+u^2+v^2)])
        sage: Phi1.display()
        Phi: S^2 --> R^3
        on U: (x, y) |--> (X, Y, Z) = (2*x/(x^2 + y^2 + 1), 2*y/(x^2 + y^2 + 1),
         (x^2 + y^2 - 1)/(x^2 + y^2 + 1))
        on V: (u, v) |--> (X, Y, Z) = (2*u/(u^2 + v^2 + 1), 2*v/(u^2 + v^2 + 1),
         -(u^2 + v^2 - 1)/(u^2 + v^2 + 1))

    At this stage, Phi1 and Phi are fully equivalent::

        sage: Phi1 == Phi
        True

    The test suite is passed::

        sage: TestSuite(Phi).run()
        sage: TestSuite(Phi1).run()

    The map acts on points::

        sage: np = M.point((0,0), chart=c_uv)  # the North pole
        sage: Phi(np)
        Point on the 3-dimensional differentiable manifold R^3
        sage: Phi(np).coord() # Cartesian coordinates
        (0, 0, 1)
        sage: sp = M.point((0,0), chart=c_xy)  # the South pole
        sage: Phi(sp).coord() # Cartesian coordinates
        (0, 0, -1)

    Differentiable maps can be composed by means of the operator ``*``: let
    us introduce the map `\RR^3\rightarrow \RR^2` corresponding to
    the projection from the point `(X,Y,Z)=(0,0,1)` onto the equatorial plane
    `Z=0`::

        sage: P = DiffManifold(2, 'R^2', r'\RR^2') # R^2 (equatorial plane)
        sage: cP.<xP, yP> = P.chart()
        sage: Psi = N.diff_map(P, (X/(1-Z), Y/(1-Z)), name='Psi',
        ....:                      latex_name=r'\Psi')
        sage: Psi
        Differentiable map Psi from the 3-dimensional differentiable manifold
         R^3 to the 2-dimensional differentiable manifold R^2
        sage: Psi.display()
        Psi: R^3 --> R^2
           (X, Y, Z) |--> (xP, yP) = (-X/(Z - 1), -Y/(Z - 1))

    Then we compose ``Psi`` with ``Phi``, thereby getting a map
    `S^2\rightarrow \RR^2`::

        sage: ster = Psi*Phi ; ster
        Differentiable map from the 2-dimensional differentiable manifold S^2
         to the 2-dimensional differentiable manifold R^2

    Let us test on the South pole (``sp``) that ``ster`` is indeed the
    composite of ``Psi`` and ``Phi``::

        sage: ster(sp) == Psi(Phi(sp))
        True

    Actually ``ster`` is the stereographic projection from the North pole, as
    its coordinate expression reveals::

        sage: ster.display()
        S^2 --> R^2
        on U: (x, y) |--> (xP, yP) = (x, y)
        on V: (u, v) |--> (xP, yP) = (u/(u^2 + v^2), v/(u^2 + v^2))

    If its codomain is 1-dimensional, a differentiable map must be
    defined by a single symbolic expression for each pair of charts, and not
    by a list/tuple with a single element::

        sage: N = DiffManifold(1, 'N')
        sage: c_N = N.chart('X')
        sage: Phi = M.diff_map(N, {(c_xy, c_N): x^2+y^2, \
        ....: (c_uv, c_N): 1/(u^2+v^2)})  # not ...[1/(u^2+v^2)] or (1/(u^2+v^2),)

    An example of differentiable map `\RR \rightarrow \RR^2`::

        sage: R = DiffManifold(1, 'R')  # field R
        sage: T.<t> = R.chart()  # canonical chart on R
        sage: R2 = DiffManifold(2, 'R^2')  # R^2
        sage: c_xy.<x,y> = R2.chart() # Cartesian coordinates on R^2
        sage: Phi = R.diff_map(R2, [cos(t), sin(t)], name='Phi') ; Phi
        Differentiable map Phi from the 1-dimensional differentiable manifold R
         to the 2-dimensional differentiable manifold R^2
        sage: Phi.parent()
        Set of Morphisms from 1-dimensional differentiable manifold R to
         2-dimensional differentiable manifold R^2 in Category of sets
        sage: Phi.parent() is Hom(R, R2)
        True
        sage: Phi.display()
        Phi: R --> R^2
           t |--> (x, y) = (cos(t), sin(t))

    An example of diffeomorphism between the unit open disk and the Euclidean
    plane `\RR^2`::

        sage: D = R2.open_subset('D', coord_def={c_xy: x^2+y^2<1}) # the open unit disk
        sage: Phi = D.diffeomorphism(R2, [x/sqrt(1-x^2-y^2), y/sqrt(1-x^2-y^2)],
        ....:                        name='Phi', latex_name=r'\Phi')
        sage: Phi
        Diffeomorphism Phi from the Open subset D of the 2-dimensional
         differentiable manifold R^2 to the 2-dimensional differentiable
         manifold R^2
        sage: Phi.parent()
        Set of Morphisms from Open subset D of the 2-dimensional differentiable
         manifold R^2 to 2-dimensional differentiable manifold R^2 in Category
         of facade sets
        sage: Phi.parent() is Hom(D, R2)
        True
        sage: Phi.display()
        Phi: D --> R^2
           (x, y) |--> (x, y) = (x/sqrt(-x^2 - y^2 + 1), y/sqrt(-x^2 - y^2 + 1))

    The image of a point::

        sage: p = D.point((1/2,0))
        sage: q = Phi(p) ; q
        Point on the 2-dimensional differentiable manifold R^2
        sage: q.coord()
        (1/3*sqrt(3), 0)

    The inverse diffeomorphism is computed by means of the method
    :meth:`~sage.manifolds.continuous_map.ContinuousMap.inverse`::

        sage: Phi.inverse()
        Diffeomorphism Phi^(-1) from the 2-dimensional differentiable manifold R^2
         to the Open subset D of the 2-dimensional differentiable manifold R^2

    Equivalently, one may use the notations ``^(-1)`` or ``~`` to get the
    inverse::

        sage: Phi^(-1) is Phi.inverse()
        True
        sage: ~Phi is Phi.inverse()
        True

    Check that ``~Phi`` is indeed the inverse of ``Phi``::

        sage: (~Phi)(q) == p
        True
        sage: Phi * ~Phi == R2.identity_map()
        True
        sage: ~Phi * Phi == D.identity_map()
        True

    The coordinate expression of the inverse diffeomorphism::

        sage: (~Phi).display()
        Phi^(-1): R^2 --> D
           (x, y) |--> (x, y) = (x/sqrt(x^2 + y^2 + 1), y/sqrt(x^2 + y^2 + 1))

    A special case of diffeomorphism: the identity map of the open unit disk::

        sage: id = D.identity_map() ; id
        Identity map Id_D of the Open subset D of the 2-dimensional
         differentiable manifold R^2
        sage: latex(id)
        \mathrm{Id}_{D}
        sage: id.parent()
        Set of Morphisms from Open subset D of the 2-dimensional differentiable
         manifold R^2 to Open subset D of the 2-dimensional differentiable
         manifold R^2 in Category of facade sets
        sage: id.parent() is Hom(D, D)
        True
        sage: id is Hom(D,D).one()  # the identity element of the monoid Hom(D,D)
        True

    The identity map acting on a point::

        sage: id(p)
        Point on the 2-dimensional differentiable manifold R^2
        sage: id(p) == p
        True
        sage: id(p) is p
        True

    The coordinate expression of the identity map::

        sage: id.display()
        Id_D: D --> D
           (x, y) |--> (x, y)

    The identity map is its own inverse::

        sage: id^(-1) is id
        True
        sage: ~id is id
        True

    """
    def __init__(self, parent, coord_functions=None, name=None, latex_name=None,
                 is_isomorphism=False, is_identity=False):
        r"""
        Construct a differentiable map.

        TESTS::

            sage: M = DiffManifold(2, 'M')
            sage: X.<x,y> = M.chart()
            sage: N = DiffManifold(3, 'N')
            sage: Y.<u,v,w> = N.chart()
            sage: f = Hom(M,N)({(X,Y): (x+y, x*y, x-y)}, name='f') ; f
            Differentiable map f from the 2-dimensional differentiable manifold
             M to the 3-dimensional differentiable manifold N
            sage: f.display()
            f: M --> N
               (x, y) |--> (u, v, w) = (x + y, x*y, x - y)
            sage: TestSuite(f).run()

        The identity map::

            sage: f = Hom(M,M)({}, is_identity=True) ; f
            Identity map Id_M of the 2-dimensional differentiable manifold M
            sage: f.display()
            Id_M: M --> M
               (x, y) |--> (x, y)
            sage: TestSuite(f).run()

        """
        ContinuousMap.__init__(self, parent, coord_functions=coord_functions,
                               name=name, latex_name=latex_name,
                               is_isomorphism=is_isomorphism,
                               is_identity=is_identity)

    #
    # SageObject methods
    #

    def _repr_(self):
        r"""
        String representation of the object.

        TESTS::

            sage: M = DiffManifold(2, 'M')
            sage: X.<x,y> = M.chart()
            sage: N = DiffManifold(2, 'N')
            sage: Y.<u,v> = N.chart()
            sage: f = Hom(M,N)({(X,Y): (x+y,x*y)})
            sage: f._repr_()
            'Differentiable map from the 2-dimensional differentiable manifold M to
             the 2-dimensional differentiable manifold N'
            sage: f = Hom(M,N)({(X,Y): (x+y,x*y)}, name='f')
            sage: f._repr_()
            'Differentiable map f from the 2-dimensional differentiable manifold M to
             the 2-dimensional differentiable manifold N'
            sage: f = Hom(M,N)({(X,Y): (x+y,x-y)}, name='f', is_isomorphism=True)
            sage: f._repr_()
            'Diffeomorphism f from the 2-dimensional differentiable manifold M to
             the 2-dimensional differentiable manifold N'
            sage: f = Hom(M,M)({(X,X): (x+y,x-y)}, name='f', is_isomorphism=True)
            sage: f._repr_()
            'Diffeomorphism f of the 2-dimensional differentiable manifold M'
            sage: f = Hom(M,M)({}, name='f', is_identity=True)
            sage: f._repr_()
            'Identity map f of the 2-dimensional differentiable manifold M'

        """
        if self._is_identity:
            return "Identity map " + self._name + \
                   " of the {}".format(self._domain)
        if self._is_isomorphism:
            description = "Diffeomorphism"
        else:
            description = "Differentiable map"
        if self._name is not None:
            description += " " + self._name
        if self._domain == self._codomain:
            if self._is_isomorphism:
                description += " of the {}".format(self._domain)
            else:
                description += " from the {} to itself".format(self._domain)
        else:
            description += " from the {} to the {}".format(self._domain,
                                                           self._codomain)
        return description

    def _init_derived(self):
        r"""
        Initialize the derived quantities.

        TEST::

            sage: M = DiffManifold(2, 'M')
            sage: X.<x,y> = M.chart()
            sage: f = M.diffeomorphism(M, [x+y, x-y])
            sage: f._init_derived()
            sage: f._restrictions
            {}
            sage: f._inverse

        """
        ContinuousMap._init_derived(self)  # derived quantities of the mother
                                           # class
        self._diff = {} # dict. of the coord. expressions of the differential
                        # keys: pair of charts

    def _del_derived(self):
        r"""
        Delete the derived quantities.

        TEST::

            sage: M = DiffManifold(2, 'M')
            sage: X.<x,y> = M.chart()
            sage: f = M.diffeomorphism(M, [x+y, x-y])
            sage: f^(-1)
            Diffeomorphism of the 2-dimensional differentiable manifold M
            sage: f._inverse  # was set by f^(-1)
            Diffeomorphism of the 2-dimensional differentiable manifold M
            sage: f._del_derived()
            sage: f._inverse  # has been set to None by _del_derived()

        """
        ContinuousMap._del_derived(self)  # derived quantities of the mother
                                          # class
        self._diff.clear()

    def pullback(self, tensor):
        r"""
        Pullback operator associated with the differentiable map.

        INPUT:

        - ``tensor`` -- instance of class
          :class:`~sage.manifolds.differentiable.tensorfield.TensorField`
          representing a fully covariant tensor field `T` on the mapping's
          codomain, i.e. a tensor field of type (0,p), with p a positive or
          zero integer. The case p=0 corresponds to a scalar field.

        OUTPUT:

        - instance of class
          :class:`~sage.manifolds.differentiable.tensorfield.TensorField`
          representing a fully covariant tensor field on the mapping's domain
          that is the pullback of `T` given by ``self``.

        EXAMPLES:

        Pullback on `S^2` of a scalar field defined on `R^3`::

            sage: M = DiffManifold(2, 'S^2', start_index=1)
            sage: U = M.open_subset('U') # the complement of a meridian (domain of spherical coordinates)
            sage: c_spher.<th,ph> = U.chart(r'th:(0,pi):\theta ph:(0,2*pi):\phi') # spherical coord. on U
            sage: N = DiffManifold(3, 'R^3', r'\RR^3', start_index=1)
            sage: c_cart.<x,y,z> = N.chart() # Cartesian coord. on R^3
            sage: Phi = U.diff_map(N, (sin(th)*cos(ph), sin(th)*sin(ph), cos(th)),
            ....:                  name='Phi', latex_name=r'\Phi')
            sage: f = N.scalar_field(x*y*z, name='f') ; f
            Scalar field f on the 3-dimensional differentiable manifold R^3
            sage: f.display()
            f: R^3 --> R
               (x, y, z) |--> x*y*z
            sage: pf = Phi.pullback(f) ; pf
            Scalar field Phi_*(f) on the Open subset U of the 2-dimensional
             differentiable manifold S^2
            sage: pf.display()
            Phi_*(f): U --> R
               (th, ph) |--> cos(ph)*cos(th)*sin(ph)*sin(th)^2

        Pullback on `S^2` of the standard Euclidean metric on `R^3`::

            sage: g = N.sym_bilin_form_field('g')
            sage: g[1,1], g[2,2], g[3,3] = 1, 1, 1
            sage: g.display()
            g = dx*dx + dy*dy + dz*dz
            sage: pg = Phi.pullback(g) ; pg
            Field of symmetric bilinear forms Phi_*(g) on the Open subset U of
             the 2-dimensional differentiable manifold S^2
            sage: pg.display()
            Phi_*(g) = dth*dth + sin(th)^2 dph*dph

        Pullback on `S^2` of a 3-form on `R^3`::

            sage: a = N.diff_form(3, 'A')
            sage: a[1,2,3] = f
            sage: a.display()
            A = x*y*z dx/\dy/\dz
            sage: pa = Phi.pullback(a) ; pa
            3-form Phi_*(A) on the Open subset U of the 2-dimensional
             differentiable manifold S^2
            sage: pa.display() # should be zero (as any 3-form on a 2-dimensional manifold)
            Phi_*(A) = 0

        """
        from sage.manifolds.differentiable.tensorfield import TensorFieldParal
        from sage.manifolds.differentiable.vectorframe import CoordFrame
        from sage.tensor.modules.comp import Components, CompWithSym, \
                                                 CompFullySym, CompFullyAntiSym

        def _pullback_paral(self, tensor):
            r"""
            Pullback on parallelizable domains.
            """
            dom1 = self._domain
            dom2 = self._codomain
            ncov = tensor._tensor_type[1]
            resu_name = None ; resu_latex_name = None
            if self._name is not None and tensor._name is not None:
                resu_name = self._name + '_*(' + tensor._name + ')'
            if self._latex_name is not None and tensor._latex_name is not None:
                resu_latex_name = self._latex_name + '_*' + tensor._latex_name
            fmodule1 = dom1.vector_field_module()
            ring1 = fmodule1._ring
            si1 = fmodule1._sindex
            of1 = fmodule1._output_formatter
            si2 = dom2._manifold._sindex
            resu = fmodule1.tensor((0,ncov), name=resu_name,
                                   latex_name=resu_latex_name, sym=tensor._sym,
                                   antisym=tensor._antisym)
            for frame2 in tensor._components:
                if isinstance(frame2, CoordFrame):
                    chart2 = frame2._chart
                    for chart1 in dom1._atlas:
                        if (chart1, chart2) in self._coord_expression:
                            # Computation at the component level:
                            frame1 = chart1._frame
                            tcomp = tensor._components[frame2]
                            if isinstance(tcomp, CompFullySym):
                                ptcomp = CompFullySym(ring1, frame1, ncov,
                                                      start_index=si1,
                                                      output_formatter=of1)
                            elif isinstance(tcomp, CompFullyAntiSym):
                                ptcomp = CompFullyAntiSym(ring1, frame1, ncov,
                                                          start_index=si1,
                                                          output_formatter=of1)
                            elif isinstance(tcomp, CompWithSym):
                                ptcomp = CompWithSym(ring1, frame1, ncov,
                                                     start_index=si1,
                                                     output_formatter=of1,
                                                     sym=tcomp.sym,
                                                     antisym=tcomp.antisym)
                            else:
                                ptcomp = Components(ring1, frame1, ncov,
                                                    start_index=si1,
                                                    output_formatter=of1)
                            phi = self._coord_expression[(chart1, chart2)]
                            jacob = phi.jacobian()
                            # X2 coordinates expressed in terms of X1 ones via the
                            # mapping:
                            coord2_1 = phi(*(chart1._xx))
                            for ind_new in ptcomp.non_redundant_index_generator():
                                res = 0
                                for ind_old in dom2._manifold.index_generator(ncov):
                                    ff = tcomp[[ind_old]].coord_function(chart2)
                                    t = chart1.function(ff(*coord2_1))
                                    for i in range(ncov):
                                        t *= jacob[ind_old[i]-si2][ind_new[i]-si1]
                                    res += t
                                ptcomp[ind_new] = res
                            resu._components[frame1] = ptcomp
                return resu
        # End of function _pullback_paral

        # Special case of the identity map:
        if self._is_identity:
            return tensor  # no test for efficiency
        # Generic case:
        dom1 = self._domain
        dom2 = self._codomain
        tdom = tensor._domain
        if not tdom.is_subset(dom2):
            raise ValueError("the tensor field is not defined on the map " +
                             "codomain")
        (ncon, ncov) = tensor._tensor_type
        if ncon != 0:
            raise TypeError("the pullback cannot be taken on a tensor " +
                            "with some contravariant part")
        resu_name = None ; resu_latex_name = None
        if self._name is not None and tensor._name is not None:
            resu_name = self._name + '_*(' + tensor._name + ')'
        if self._latex_name is not None and tensor._latex_name is not None:
            resu_latex_name = self._latex_name + '_*' + tensor._latex_name
        if ncov == 0:
            # Case of a scalar field
            resu_fc = []
            for chart2 in tensor._express:
                for chart1 in dom1._atlas:
                    if (chart1, chart2) in self._coord_expression:
                        phi = self._coord_expression[(chart1, chart2)]
                        coord1 = chart1._xx
                        ff = tensor._express[chart2]
                        resu_fc.append( chart1.function(ff(*(phi(*coord1)))) )
            dom_resu = resu_fc[0]._chart._domain
            for fc in resu_fc[1:]:
                dom_resu = dom_resu.union(fc._chart._domain)
            resu = dom_resu.scalar_field(name=resu_name,
                                         latex_name=resu_latex_name)
            for fc in resu_fc:
                resu._express[fc._chart] = fc
        else:
            # Case of tensor field of rank >= 1
            if tensor._vmodule._dest_map is not tdom._identity_map:
                raise TypeError("the pullback in defined only for tensor " +
                                "fields on {}".format(dom2))
            resu_rst = []
            for chart_pair in self._coord_expression:
                chart1 = chart_pair[0] ; chart2 = chart_pair[1]
                ch2dom = chart2._domain
                if ch2dom.is_subset(tdom):
                    self_r = self.restrict(chart1._domain, subcodomain=ch2dom)
                    tensor_r = tensor.restrict(ch2dom)
                    resu_rst.append(_pullback_paral(self_r, tensor_r))
            dom_resu = resu_rst[0]._domain
            for rst in resu_rst[1:]:
                dom_resu = dom_resu.union(rst._domain)
            resu = dom_resu.tensor_field(0, ncov, name=resu_name,
                                         latex_name=resu_latex_name,
                                         sym=resu_rst[0]._sym,
                                         antisym=resu_rst[0]._antisym)
            for rst in resu_rst:
                if rst._domain is not resu._domain:
                    resu._restrictions[rst._domain] = rst
            if isinstance(resu, TensorFieldParal):
                for rst in resu_rst:
                    for frame, comp in rst._components.iteritems():
                        resu._components[frame] = comp
        return resu
