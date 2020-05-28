from recon import MappingNode, ReconGraph, Reconciliation, EventType
from recon import Cospeciation, Duplication, Transfer, Loss, TipTip
from typing import Dict, Tuple, List

def _find_roots(old_recon_graph) -> List[MappingNode]:
    not_roots = set()
    for mapping in old_recon_graph:
        for event in old_recon_graph[mapping]:
            etype, left, right = event
            if etype in 'SDT':
                not_roots.add(left)
                not_roots.add(right)
            elif etype == 'L':
                child = left
                not_roots.add(child)
            elif etype == 'C':
                pass
            else:
                raise ValueError('%s not in "SDTLC' % etype)
    roots = []
    for mapping in old_recon_graph:
        if mapping not in not_roots:
            roots.append(mapping)
    return roots

def dict_to_reconciliation(old_recon_graph: Dict[Tuple, List]):
    """
    Convert the old reconciliation graph format to Reconciliation.

    Example of old format:
    old_recon_graph = {
        ('n0', 'm2'): [('S', ('n2', 'm3'), ('n1', 'm4'))],
        ('n1', 'm4'): [('C', (None, None), (None, None))],
        ('n2', 'm3'): [('T', ('n3', 'm3'), ('n4', 'm1'))],
        ('n3', 'm3'): [('C', (None, None), (None, None))],
        ('n4', 'm1'): [('C', (None, None), (None, None))],
    }
    """
    roots = _find_roots(old_recon_graph)
    if len(roots) > 1:
        raise ValueError("recon_graph has many roots")
    root = roots[0]
    recon = Reconciliation(root)
    for mapping in old_recon_graph:
        host, parasite = mapping
        if len(old_recon_graph[mapping]) != 1:
            raise ValueError('old_recon_graph mapping node has no event or multiple events')
        etype, left, right = old_recon_graph[mapping][0]
        mapping_node = MappingNode(host, parasite)
        if etype in 'SDT':
            left_parasite, left_host = left
            right_parasite, right_host = right
            left_mapping = MappingNode(left_parasite, left_host)
            right_mapping = MappingNode(right_parasite, right_host)
            if etype == 'S':
                recon.set_event(mapping_node, Cospeciation(left_mapping, right_mapping))
            if etype == 'D':
                recon.set_event(mapping_node, Duplication(left_mapping, right_mapping))
            if etype == 'T':
                recon.set_event(mapping_node, Transfer(left_mapping, right_mapping))
        elif etype == 'L':
            child_parasite, child_host = left
            child_mapping = MappingNode(child_parasite, child_host)
            recon.set_event(mapping_node, Loss(child_mapping))
        elif etype == 'C':
            recon.set_event(mapping_node, TipTip())
        else:
            raise ValueError('%s not in "SDTLC' % etype)
    return recon


def dict_to_recongraph(old_recon_graph: Dict[Tuple, List]):
    """
    Convert the old reconciliation graph format to ReconGraph.

    Example of old format:
    old_recon_graph = {
        ('n0', 'm2'): [('S', ('n2', 'm3'), ('n1', 'm4'))],
        ('n1', 'm4'): [('C', (None, None), (None, None))],
        ('n2', 'm3'): [('T', ('n3', 'm3'), ('n4', 'm1'))],
        ('n3', 'm3'): [('C', (None, None), (None, None))],
        ('n4', 'm1'): [('C', (None, None), (None, None))],
    }
    """
    roots = _find_roots(old_recon_graph)
    recon_graph = ReconGraph(roots)
    for mapping in old_recon_graph:
        host, parasite = mapping
        for event in old_recon_graph[mapping]:
            etype, left, right = event
            mapping_node = MappingNode(host, parasite)
            if etype in 'SDT':
                left_parasite, left_host = left
                right_parasite, right_host = right
                left_mapping = MappingNode(left_parasite, left_host)
                right_mapping = MappingNode(right_parasite, right_host)
                if etype == 'S':
                    recon_graph.add_event(mapping_node, Cospeciation(left_mapping, right_mapping))
                if etype == 'D':
                    recon_graph.add_event(mapping_node, Duplication(left_mapping, right_mapping))
                if etype == 'T':
                    recon_graph.add_event(mapping_node, Transfer(left_mapping, right_mapping))
            elif etype == 'L':
                child_parasite, child_host = left
                child_mapping = MappingNode(child_parasite, child_host)
                recon_graph.add_event(mapping_node, Loss(child_mapping))
            elif etype == 'C':
                recon_graph.add_event(mapping_node, TipTip())
            else:
                raise ValueError('%s not in "SDTLC' % etype)
    return recon_graph
