from recon import MappingNode, ReconGraph, Reconciliation, EventType
from recon import Cospeciation, Duplication, Transfer, Loss, TipTip
import converter

## Examples

# Creating a reconciliation graph
old_recon_graph = {
    ('n0', 'm2'): [('S', ('n2', 'm3'), ('n1', 'm4'))],
    ('n1', 'm4'): [('C', (None, None), (None, None))],
    ('n2', 'm3'): [('T', ('n3', 'm3'), ('n4', 'm1'))],
    ('n3', 'm3'): [('C', (None, None), (None, None))],
    ('n4', 'm1'): [('C', (None, None), (None, None))],
}
 
source = MappingNode('n0', 'm2')
recongraph = ReconGraph(sources=[source])
recongraph.add_event(MappingNode('n0', 'm2'), Cospeciation(MappingNode('n2', 'm3'), MappingNode('n1', 'm4')))
recongraph.add_event(MappingNode('n1', 'm4'), TipTip())
recongraph.add_event(MappingNode('n2', 'm3'), Transfer(MappingNode('n3', 'm3'), MappingNode('n4', 'm1')))
recongraph.add_event(MappingNode('n3', 'm3'), TipTip())
recongraph.add_event(MappingNode('n4', 'm1'), TipTip())

source = MappingNode('n0', 'm2')
recon = Reconciliation(source)
recon.set_event(MappingNode('n0', 'm2'), Cospeciation(MappingNode('n2', 'm3'), MappingNode('n1', 'm4')))
recon.set_event(MappingNode('n1', 'm4'), TipTip())
recon.set_event(MappingNode('n2', 'm3'), Transfer(MappingNode('n3', 'm3'), MappingNode('n4', 'm1')))
recon.set_event(MappingNode('n3', 'm3'), TipTip())
recon.set_event(MappingNode('n4', 'm1'), TipTip())

# Checking whether the mapping ('n1', 'm4') has a cospeciation event
# old
has_cospeciation = False
mapping = ('n0', 'm2')
for event in old_recon_graph[mapping]:
    if event[0] == 'S':
        has_cospeciation = True
        break
assert has_cospeciation

# new for ReconGraph
has_cospeciation = False
mapping = MappingNode('n0', 'm2')
for event in recongraph.events_of(mapping):
    if event.event_type() is EventType.COSPECIATION:
        has_cospeciation = True
        break
assert has_cospeciation

# new for single Reconciliation
is_cospeciation = recon.event_of(MappingNode('n0', 'm2')).event_type() is EventType.COSPECIATION
assert is_cospeciation

# Getting the source (for the old one, we have to pass the sources around)
sources = recongraph.sources
assert len(sources) == 1 and sources[0] == MappingNode('n0', 'm2')

source = recon.source
assert source == MappingNode('n0', 'm2')

# Checking whether ('n4', 'm1') is leaf
mapping_is_sink = old_recon_graph[('n4', 'm1')][0][0] == 'C'
assert mapping_is_sink

mapping_is_sink = recongraph.is_sink(MappingNode('n4', 'm1'))
assert mapping_is_sink

mapping_is_sink = recon.is_sink(MappingNode('n4', 'm1'))
assert mapping_is_sink

recongraph = converter.dict_to_recongraph(old_recon_graph)
print(recongraph)

recon = converter.dict_to_reconciliation(old_recon_graph)
print(recon)
