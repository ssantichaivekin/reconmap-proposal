.. reconmap-proposal documentation master file, created by
   sphinx-quickstart on Thu May 28 10:18:21 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Proposal of ReconGraph structure!
=============================================

Examples
--------
Creating the data structure::

   # Old dictionary structure
   old_recon_graph = {
       ('n0', 'm2'): [('S', ('n2', 'm3'), ('n1', 'm4'))],
       ('n1', 'm4'): [('C', (None, None), (None, None))],
       ('n2', 'm3'): [('T', ('n3', 'm3'), ('n4', 'm1'))],
       ('n3', 'm3'): [('C', (None, None), (None, None))],
       ('n4', 'm1'): [('C', (None, None), (None, None))],
   }

   # New ReconGraph structure
   source = MappingNode('n0', 'm2')
   recongraph = ReconGraph(sources=[source])
   recongraph.add_event(MappingNode('n0', 'm2'), Cospeciation(MappingNode('n2', 'm3'), MappingNode('n1', 'm4')))
   recongraph.add_event(MappingNode('n1', 'm4'), TipTip())
   recongraph.add_event(MappingNode('n2', 'm3'), Transfer(MappingNode('n3', 'm3'), MappingNode('n4', 'm1')))
   recongraph.add_event(MappingNode('n3', 'm3'), TipTip())
   recongraph.add_event(MappingNode('n4', 'm1'), TipTip())

   # New (single) Reconciliation structure
   source = MappingNode('n0', 'm2')
   recon = Reconciliation(source)
   recon.set_event(MappingNode('n0', 'm2'), Cospeciation(MappingNode('n2', 'm3'), MappingNode('n1', 'm4')))
   recon.set_event(MappingNode('n1', 'm4'), TipTip())
   recon.set_event(MappingNode('n2', 'm3'), Transfer(MappingNode('n3', 'm3'), MappingNode('n4', 'm1')))
   recon.set_event(MappingNode('n3', 'm3'), TipTip())
   recon.set_event(MappingNode('n4', 'm1'), TipTip())

Checking whether the mapping ``('n1', 'm4')`` has a cospeciation event::

   # Old dictionary structure
   has_cospeciation = False
   mapping = ('n0', 'm2')
   for event in old_recon_graph[mapping]:
       if event[0] == 'S':
           has_cospeciation = True
           break

   # New ReconGraph structure
   has_cospeciation = False
   mapping = MappingNode('n0', 'm2')
   for event in recongraph.events_of(mapping):
       if event.event_type is EventType.COSPECIATION:
           has_cospeciation = True
           break

   # New (single) Reconciliation structure
   is_cospeciation = recon.event_of(MappingNode('n0', 'm2')).event_type is EventType.COSPECIATION

Getting the source mapping node::

   # Old dictionary structure requires passing the source mapping node around

   # New ReconGraph structure
   sources = recongraph.sources

   # New (single) Reconciliation structure
   source = recon.source

Checking whether ``('n4', 'm1')`` is a sink::

   # Old dictionary structure
   mapping_is_sink = old_recon_graph[('n4', 'm1')][0][0] == 'C'

   # New ReconGraph structure
   mapping_is_sink = recongraph.is_sink(MappingNode('n4', 'm1'))

   # New (single) Reconciliation structure
   mapping_is_sink = recon.is_sink(MappingNode('n4', 'm1'))

Documentation
-------------
Note that property ``p`` of a class ``C`` means you can access it with ``C.p`` without parenthesis

.. automodule:: recon
   :members:
   :inherited-members:
   :undoc-members:
