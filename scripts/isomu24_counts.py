#!/usr/bin/env python3
"""Make additive, unweighted IsoMu24 counts from offline-selected CROWN MC.
Run on shards, hadd counts files, then run --finalize on the merged counts.
Input MC must not be prefiltered by IsoMu24. Never hadd efficiency maps.
"""
import argparse
from array import array


def main():
    import ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', nargs='+')
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('--tree', default='ntuple')
    parser.add_argument('--finalize', action='store_true')
    args = parser.parse_args()
    if args.finalize:
        if len(args.inputs) != 1:
            parser.error('--finalize requires one merged counts file')
        source = ROOT.TFile.Open(args.inputs[0])
        if not source or source.IsZombie():
            raise RuntimeError('Cannot open counts file')
        output = ROOT.TFile.Open(args.output, 'RECREATE')
        for i in (1, 2):
            total = source.Get(f'mu{i}_total')
            passed = source.Get(f'mu{i}_pass')
            if not total or not passed:
                raise RuntimeError('Missing numerator/denominator histograms')
            efficiency = passed.Clone(f'mu{i}_IsoMu24_eff_mc')
            efficiency.Divide(passed, total, 1., 1., 'B')
            efficiency.Write()
            # Zero-denominator bins are undefined, not zero-efficiency measurements.
            total.Write()
            passed.Write()
        source.Get('event_counts').Write()
        output.Close()
        return
    chain = ROOT.TChain(args.tree)
    for path in args.inputs:
        chain.Add(path)
    if chain.GetEntries() == 0:
        raise RuntimeError('No input events')
    ptbins = array('d', [20, 24, 26, 30, 35, 40, 50, 60, 80, 120, 200, 500, 1000])
    etabins = array('d', [0, .9, 1.2, 2.1, 2.4, 2.5])
    output = ROOT.TFile.Open(args.output, 'RECREATE')
    hist = {}
    for i in (1, 2):
        for kind in ('total', 'pass'):
            name = f'mu{i}_{kind}'
            hist[name] = ROOT.TH2D(name, ';corrected pT [GeV];|corrected eta|',
                                  len(ptbins)-1, ptbins, len(etabins)-1, etabins)
    counts = ROOT.TH1D('event_counts', 'Offline and IsoMu24 OR counts', 2, 0, 2)
    counts.GetXaxis().SetBinLabel(1, 'offline_total')
    counts.GetXaxis().SetBinLabel(2, 'IsoMu24_pass')
    for event in chain:
        counts.Fill(.5, event.IsoMu24_event_total)
        counts.Fill(1.5, event.IsoMu24_event_pass)
        for i in (1, 2):
            pt = getattr(event, f'mu{i}_fsr_kit_bsc_pt')
            eta = abs(getattr(event, f'mu{i}_fsr_kit_bsc_eta'))
            for kind in ('total', 'pass'):
                hist[f'mu{i}_{kind}'].Fill(pt, eta, getattr(event, f'mu{i}_IsoMu24_{kind}'))
    output.Write()
    output.Close()


if __name__ == '__main__':
    main()
