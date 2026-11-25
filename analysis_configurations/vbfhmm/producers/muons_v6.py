from copy import deepcopy
from ..quantities import output as q
from ..quantities import nanoAOD as n
from code_generation.producer import Producer, ProducerGroup
from . import muons, triggers

NewIso = Producer(name="NewIso", call="basefunctions::FSRNewIso({df}, {output}, {input})",
 input=[n.Muon_pt,n.Muon_pfRelIso04_all,q.Muon_pt_corrected,n.Muon_eta,n.Muon_phi,n.Muon_fsrPhotonIdx,n.FsrPhoton_pt,n.FsrPhoton_eta,n.FsrPhoton_phi,n.FsrPhoton_relIso03,n.FsrPhoton_dROverEt2], output=[q.newIso],scopes=["global"])

def iso_copy(producer):
    result=deepcopy(producer)
    result.name += "V6"
    for scope in result.input:
        result.input[scope]=[q.newIso if x==n.Muon_pfRelIso04_all else x for x in result.input[scope]]
    return result

BaseMuons = ProducerGroup(name="BaseMuonsV6",call="physicsobject::CombineMasks({df}, {output}, {input})",input=[],output=[q.base_muons_mask],scopes=["global"], subproducers=[muons.MuonPtCut,muons.MuonEtaCut,muons.MuonIDCut,iso_copy(muons.MuonIsoCut),iso_copy(muons.LowPtMuonTightCutV4)])
GoodMuons = ProducerGroup(name="GoodMuonsV6",call="physicsobject::CombineMasks({df}, {output}, {input})",input=[q.base_muons_mask],output=[q.good_muons_mask],scopes=["vbfhmm"],subproducers=[muons.GoodMuonPtCut,muons.GoodMuonEtaCut,muons.GoodMuonIDCut,iso_copy(muons.GoodMuonIsoCut)])
VHttHMask=Producer(name="VHttHMask",call="basefunctions::VHttHMuonMask({df}, {output}, {input})",input=[q.Muon_pt_corrected,q.Muon_eta_corrected,n.Muon_isGlobal,n.Muon_isTracker,n.Muon_mediumId,n.Muon_dz,n.Muon_dxy,n.Muon_sip3d,n.Muon_miniPFRelIso_all],output=[q.muon_VHttH_mask],scopes=["global"])
VHttHCount=Producer(name="VHttHCount",call="quantities::NumberOfGoodObjects({df}, {output}, {input})",input=[q.muon_VHttH_mask],output=[q.nmuon_VHttH],scopes=["global"])
VHttHExtra=Producer(name="VHttHExtra",call="basefunctions::ExtraVHttHMuons({df}, {output}, {input})",input=[q.muon_VHttH_mask,q.dimuon_HiggsCand_collection],output=[q.nmuon_VHttH_extra],scopes=["vbfhmm"])
NewIso1=Producer(name="NewIso1",call="basefunctions::getvar<float>({df}, {output}, 0, {input})",input=[q.dimuon_HiggsCand_collection,q.newIso],output=[q.mu1_newIso],scopes=["vbfhmm"])
NewIso2=Producer(name="NewIso2",call="basefunctions::getvar<float>({df}, {output}, 1, {input})",input=[q.dimuon_HiggsCand_collection,q.newIso],output=[q.mu2_newIso],scopes=["vbfhmm"])
Match1=deepcopy(triggers.Muon1IsoMu24Match)
Match1.name="Muon1IsoMu24MatchV6"
Match1.call=Match1.call.replace(", 0.4)",", 0.1)")
Match2=deepcopy(triggers.Muon2IsoMu24Match)
Match2.name="Muon2IsoMu24MatchV6"
Match2.call=Match2.call.replace(", 0.4)",", 0.1)")
Matches=ProducerGroup(name="MatchesV6",call=None,input=None,output=None,scopes=["vbfhmm"],subproducers=[Match1,Match2])
