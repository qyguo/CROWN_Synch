#!/usr/bin/env python3
"""Extract NanoAOD Events while preserving Runs/LuminosityBlocks for CROWN.
Debug use only: copied metadata retains original-file normalization.
"""
import argparse
import os
import ROOT


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('-i', '--input', required=True)
    p.add_argument('-o', '--output', required=True)
    p.add_argument('--run', required=True, type=int)
    p.add_argument('--lumi', required=True, type=int)
    p.add_argument('--event', required=True, type=int)
    args = p.parse_args()
    if os.path.realpath(args.input) == os.path.realpath(args.output):
        p.error('Input and output must differ')
    if os.path.exists(args.output):
        p.error('Output already exists; choose a new filename')
    source = ROOT.TFile.Open(args.input)
    if not source or source.IsZombie():
        raise RuntimeError('Cannot open input')
    for name in ('Events', 'Runs'):
        if not source.Get(name):
            raise RuntimeError(f'Missing input tree {name}')
    df = ROOT.RDataFrame('Events', args.input)
    selection = (f'run=={args.run}u && luminosityBlock=={args.lumi}u '
                 f'&& event=={args.event}ULL')
    selected = df.Filter(selection)
    count = int(selected.Count().GetValue())
    if count == 0:
        raise RuntimeError('Target event not found; no output written')
    # Snapshot writes all Events branches to a conventional TTree.
    options = ROOT.RDF.RSnapshotOptions()
    selected.Snapshot('Events', args.output, '', options)
    output = ROOT.TFile.Open(args.output, 'UPDATE')
    if not output or output.IsZombie():
        raise RuntimeError('Cannot reopen output')
    for name in ('Runs', 'LuminosityBlocks'):
        tree = source.Get(name)
        if tree:
            output.cd()
            clone = tree.CloneTree(-1, 'fast')
            clone.Write(name, ROOT.TObject.kOverwrite)
    output.Close()
    source.Close()
    check = ROOT.TFile.Open(args.output)
    if not check or check.IsZombie() or not check.Get('Runs'):
        raise RuntimeError('Output validation failed')
    if check.Get('Events').GetEntries() != count:
        raise RuntimeError('Output Events count mismatch')
    print(f'Saved {count} event(s): {os.path.abspath(args.output)}')
    print('Runs metadata preserved; use this file for debugging, not MC normalization.')
    check.Close()


if __name__ == '__main__':
    main()
