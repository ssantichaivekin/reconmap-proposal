# ReconGraph Proposal

A proposal to change the old version of reconciliation graph dictionary to a class.
The code for the data structures are in `recon.py`. The code to change the old version dict to the new `ReconGraph` or 
`Reconciliation` is in `examples.py`.

The documentation is in [Read The Docs](https://reconmap-proposal.readthedocs.io/en/latest/).

```python
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

# Convert old format to (single) Reconciliation
recongraph = converter.dict_to_recongraph(old_recon_graph)
print(recongraph)

# Convert old format to ReconGraph
recon = converter.dict_to_reconciliation(old_recon_graph)
print(recon)
```
