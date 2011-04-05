``asq.selectors``
=================

.. automodule:: asq.selectors

  Selectors are so-called because they are used to select a value from an
  element.  The selected value is often an attribute or sub-element but could
  be any computed value.  The ``selectors`` module provides to standard
  selectors and also some selector factories.

  .. currentmodule asq.selectors

Selectors
---------

  .. autosummary::
     :nosignatures:

     identity

  .. autofunction:: identity(x)

     .. rubric:: Examples

     Use the the identity function with the ``where()`` query operator, which
     has the effect that only elements which evaluate to True are present in
     the result::

       >>> from selectors import identity
       >>> a = [5, 3, 0, 1, 0, 4, 2, 0, 3]
       >>> query(a).where(identity).to_list()
       [5, 3, 1, 4, 2, 3]
       

Selector factories
------------------

  .. autosummary::
     :nosignatures:

     a_
     k_
     m_

  .. autofunction:: a_(name)

     .. rubric:: Longhand equivalent

     The selector factory call::

       a_(name)

     is equivalent to the longhand::

       lambda element: element.name

     .. rubric:: Example

     From a list of spaceship characteristics order the spaceships by length
     and select the spaceship name::

       >>> from asq.selectors import a_
       >>> class SpaceShip(object):
       ...     def __init__(self, name, length, crew):
       ...         self.name = name
       ...         self.length = length
       ...         self.crew = crew
       ...
       >>> spaceships = [SpaceShip("Nebulon-B", 300, 854),
       ...               SpaceShip("V-19 Torrent", 6, 1),
       ...               SpaceShip("Venator", 1137, 7400),
       ...               SpaceShip("Lambda-class T-4a shuttle", 20, 6),
       ...               SpaceShip("GR-45 medium transport", 90, 6)]
       >>> query(spaceships).order_by(a_('length')).select(a_('name')).to_list()
       ['V-19 Torrent', 'Lambda-class T-4a shuttle', 'GR-45 medium transport',
        'Nebulon-B', 'Venator']

     or sort the

  .. autofunction:: k_(key)

     .. rubric:: Longhand equivalent

     The selector factory call::

       k_(key)

     is equivalent to the longhand::

       lambda element: element[name]

     .. rubric:: Example

     From a list of dictionaries containing planetary data, sort the planets by
     increasing mass and select their distance from the sun::

       >>> from asq.selectors import k_
       >>> planets = [dict(name='Mercury', mass=0.055, period=88),
       ...            dict(name='Venus', mass=0.815, period=224.7),
       ...            dict(name='Earth', mass=1.0, period=365.3),
       ...            dict(name='Mars', mass=0.532, period=555.3),
       ...            dict(name='Jupiter', mass=317.8, period=4332),
       ...            dict(name='Saturn', mass=95.2, period=10761),
       ...            dict(name='Uranus', mass=14.6, period=30721),
       ...            dict(name='Neptune', mass=17.2, period=60201)]
       >>> query(planets).order_by(k_('mass')).select(k_('period')).to_list()
       [88, 555.3, 224.7, 365.3, 30721, 60201, 10761, 4332]

  .. autofunction:: m_(name, *args, **kwargs)

     .. rubric:: Longhand equivalent

     The selector factory call::

       m_(name, *args, **kwargs)

     is equivalent to the longhand::

       lambda element: getattr(element, name)(*args, **kwargs)

     .. rubric:: Example

     From a list of SwimmingPool objects compute a list of swimming pool
     areas by selecting the ``area()`` method on each pool::

       >>> class SwimmingPool(object):
       ...     def __init__(self, length, width):
       ...         self.length = length
       ...         self.width = width
       ...     def area(self):
       ...         return self.width * self.length
       ...     def volume(self, depth):
       ...         return self.area() * depth
       ...
       >>> pools = [SwimmingPool(50, 25),
       ...          SwimmingPool(25, 12.5),
       ...          SwimmingPool(100, 25),
       ...          SwimmingPool(10, 10)]
       >>> query(pools).select(m_('area')).to_list()
       [1250, 312.5, 2500, 100]

     Compute volumes of the above pools for a water depth of 2 metres by
     passing the depth as a positional argument to the `m_()` selector
     factory::

       >>> query(pools).select(m_('volume', 2)).to_list()
       [2500, 625.0, 5000, 200]

     Alternatively, we can use a named parameter to make the code clearer::

       >>> query(pools).select(m_('volume', depth=1.5)).to_list()
       [1875.0, 468.75, 3750.0, 150.0]

     



     

     

     

     




