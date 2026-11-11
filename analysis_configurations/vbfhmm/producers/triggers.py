from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import ExtendedVectorProducer

####################
# Set of producers used for trigger flags
####################

GenerateSingleMuonTriggerFlags = ExtendedVectorProducer(
    name="GenerateSingleMuonTriggerFlags",
    call='trigger::GenerateTripleTriggerORFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {ptcut}, {ptcut}, {etacut}, {etacut}, {etacut}, {trigger_particle_id}, {trigger_particle_id}, {trigger_particle_id}, {filterbit}, {filterbit}, {filterbit}, {max_deltaR_triggermatch} )',
    input=[
        q.muon_p4_1,
        q.muon_p4_2,
        q.muon_p4_3,
        nanoAOD.TriggerObject_bit,
        nanoAOD.TriggerObject_id,
        nanoAOD.TriggerObject_pt,
        nanoAOD.TriggerObject_eta,
        nanoAOD.TriggerObject_phi,
    ],
    output="flagname",
    scope=["m2m"],
    vec_config="singlemuon_trigger",
)
GenerateSingleMuonTriggerFlagsForDiMuChannel = ExtendedVectorProducer(
    name="GenerateSingleMuonTriggerFlagsForDiMuChannel",
    call='trigger::GenerateDoubleTriggerORFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {ptcut}, {etacut}, {etacut}, {trigger_particle_id}, {trigger_particle_id}, {filterbit}, {filterbit}, {max_deltaR_triggermatch} )',
    input=[
        q.muon_p4_1,
        q.muon_p4_2,
        nanoAOD.TriggerObject_bit,
        nanoAOD.TriggerObject_id,
        nanoAOD.TriggerObject_pt,
        nanoAOD.TriggerObject_eta,
        nanoAOD.TriggerObject_phi,
    ],
    output="flagname",
    scope=["gghmm","vbfhmm","e2m","eemm","nnmm","fjmm"],
    vec_config="singlemuon_trigger",
)
###
GenerateSingleMuonTriggerFlagsForDiMuChannel_2022 = ExtendedVectorProducer(
    name="GenerateSingleMuonTriggerFlagsForDiMuChannel_2022",
    call='trigger::GenerateDoubleTriggerORFlag_2022({df}, {output}, {input}, "{hlt_path}", {ptcut}, {ptcut}, {etacut}, {etacut}, {trigger_particle_id}, {trigger_particle_id}, {filterbit}, {filterbit}, {max_deltaR_triggermatch} )',
    input=[
        q.muon_p4_1,
        q.muon_p4_2,
        nanoAOD.TriggerObject_bit,
        nanoAOD.TriggerObject_id,
        nanoAOD.TriggerObject_pt,
        nanoAOD.TriggerObject_eta,
        nanoAOD.TriggerObject_phi,
    ],
    output="flagname",
    scope=["gghmm","vbfhmm","e2m","eemm","nnmm","fjmm"],
    vec_config="singlemuon_trigger",
)
GenerateSingleMuonTriggerFlagsForQuadMuChannel = ExtendedVectorProducer(
    name="GenerateSingleMuonTriggerFlagsForQuadMuChannel",
    call='trigger::GenerateQuadTriggerORFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {ptcut}, {ptcut}, {ptcut}, {etacut}, {etacut}, {etacut}, {etacut}, {trigger_particle_id}, {trigger_particle_id}, {trigger_particle_id}, {trigger_particle_id}, {filterbit}, {filterbit}, {filterbit}, {filterbit}, {max_deltaR_triggermatch} )',
    input=[
        q.muon_p4_1,
        q.muon_p4_2,
        q.muon_p4_3,
        q.muon_p4_4,
        nanoAOD.TriggerObject_bit,
        nanoAOD.TriggerObject_id,
        nanoAOD.TriggerObject_pt,
        nanoAOD.TriggerObject_eta,
        nanoAOD.TriggerObject_phi,
    ],
    output="flagname",
    scope=["mmmm"],
    vec_config="singlemuon_trigger",
)

from code_generation.producer import Producer, ProducerGroup

Muon1IsoMu24Match = Producer(
    name="Muon1IsoMu24Match",
    call='trigger::GenerateDoubleTriggerORFlag_2022({df}, {output}, {input}, "HLT_IsoMu24", 26., 26., 2.5, 2.5, 13, 13, 3, 3, 0.4)',
    input=[q.muon_leadingp4_H, q.muon_leadingp4_H,
           nanoAOD.TriggerObject_bit, nanoAOD.TriggerObject_id,
           nanoAOD.TriggerObject_pt, nanoAOD.TriggerObject_eta, nanoAOD.TriggerObject_phi],
    output=[q.mu1_IsoMu24_matched], scopes=["vbfhmm"],
)

Muon2IsoMu24Match = Producer(
    name="Muon2IsoMu24Match",
    call='trigger::GenerateDoubleTriggerORFlag_2022({df}, {output}, {input}, "HLT_IsoMu24", 26., 26., 2.5, 2.5, 13, 13, 3, 3, 0.4)',
    input=[q.muon_subleadingp4_H, q.muon_subleadingp4_H,
           nanoAOD.TriggerObject_bit, nanoAOD.TriggerObject_id,
           nanoAOD.TriggerObject_pt, nanoAOD.TriggerObject_eta, nanoAOD.TriggerObject_phi],
    output=[q.mu2_IsoMu24_matched], scopes=["vbfhmm"],
)

HiggsMuonIsoMu24Matches = ProducerGroup(name="HiggsMuonIsoMu24Matches", call=None, input=None, output=None, scopes=["vbfhmm"], subproducers=[Muon1IsoMu24Match, Muon2IsoMu24Match])

_count_producers = []
_count_producers.append(Producer(name="IsoMu24_event_total", call='basefunctions::DefineQuantity({df}, {output}, 1)', input=[], output=[q.IsoMu24_event_total], scopes=["vbfhmm"]))
_count_producers.append(Producer(name="IsoMu24_event_pass", call='basefunctions::TriggerPassCount({df}, {output}, {input})', input=[q.mu1_IsoMu24_matched, q.mu2_IsoMu24_matched], output=[q.IsoMu24_event_pass], scopes=["vbfhmm"]))
_count_producers.append(Producer(name="mu1_IsoMu24_total", call='basefunctions::DefineQuantity({df}, {output}, 1)', input=[], output=[q.mu1_IsoMu24_total], scopes=["vbfhmm"]))
_count_producers.append(Producer(name="mu1_IsoMu24_pass", call='basefunctions::TriggerPassCount({df}, {output}, {input})', input=[q.mu1_IsoMu24_matched, q.mu1_IsoMu24_matched], output=[q.mu1_IsoMu24_pass], scopes=["vbfhmm"]))
_count_producers.append(Producer(name="mu2_IsoMu24_total", call='basefunctions::DefineQuantity({df}, {output}, 1)', input=[], output=[q.mu2_IsoMu24_total], scopes=["vbfhmm"]))
_count_producers.append(Producer(name="mu2_IsoMu24_pass", call='basefunctions::TriggerPassCount({df}, {output}, {input})', input=[q.mu2_IsoMu24_matched, q.mu2_IsoMu24_matched], output=[q.mu2_IsoMu24_pass], scopes=["vbfhmm"]))

IsoMu24Counts = ProducerGroup(name="IsoMu24Counts", call=None, input=None, output=None, scopes=["vbfhmm"], subproducers=_count_producers)
