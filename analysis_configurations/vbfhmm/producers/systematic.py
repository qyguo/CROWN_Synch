from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup
# write by jiahua

####################
# Set of producers used for syst uncertainties    
####################

CalPDFUncertainty_up = Producer(
    name="CalPDFUncertainty",
    call="reweighting::LHEpdf({df}, {output}, {input}, \"up\")",
    input=[
        nanoAOD.LHEPdfWeight,
    ],
    output=[q.PDF_uncertainty_up],
    scopes=["global", "vbfhmm"],
)

CalPDFUncertainty_down = Producer(
    name="CalPDFUncertainty",
    call="reweighting::LHEpdf({df}, {output}, {input}, \"down\")",
    input=[
        nanoAOD.LHEPdfWeight,
    ],
    output=[q.PDF_uncertainty_down],
    scopes=["global", "vbfhmm"],
)

CalQCDScaleUncertainty_up = Producer(
    name="CalQCDScaleUncertainty_up",
    call="reweighting::LHEscale({df}, {output}, {input}, \"up\")",
    input=[
        nanoAOD.LHEScaleWeight,
    ],
    output=[q.qcd_unc_up],
    scopes=["global", "vbfhmm"],
)

CalQCDScaleUncertainty_down = Producer(
    name="CalQCDScaleUncertainty_down",
    call="reweighting::LHEscale({df}, {output}, {input}, \"down\")",
    input=[
        nanoAOD.LHEScaleWeight,
    ],
    output=[q.qcd_unc_down],
    scopes=["global", "vbfhmm"],
)

StoreLHE_pdf = Producer(
    name="StoreLHE_pdf",
    call='basefunctions::StoreTheoryWeights({df}, {output}, "LHEPdfWeight")',
    input=[], output=[q.LHE_pdf_weights], scopes=["vbfhmm"],
)
StoreLHE_scale = Producer(
    name="StoreLHE_scale",
    call='basefunctions::StoreTheoryWeights({df}, {output}, "LHEScaleWeight")',
    input=[], output=[q.LHE_scale_weights], scopes=["vbfhmm"],
)
QCDScaleUpStored = Producer(name="QCDScaleUpStored", call='reweighting::LHEscale({df}, {output}, {input}, "up")', input=[q.LHE_scale_weights], output=[q.qcd_unc_up], scopes=["vbfhmm"])
QCDScaleDownStored = Producer(name="QCDScaleDownStored", call='reweighting::LHEscale({df}, {output}, {input}, "down")', input=[q.LHE_scale_weights], output=[q.qcd_unc_down], scopes=["vbfhmm"])
