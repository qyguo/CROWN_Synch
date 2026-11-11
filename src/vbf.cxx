#include "ROOT/RDataFrame.hxx"
#include "../include/jets.hxx"
#include "../include/vbf.hxx"

namespace jet {
ROOT::RDF::RNode DijetSelection(ROOT::RDF::RNode df,
    const std::string &index1, const std::string &index2,
    const std::string &mjj, const std::string &deta, const std::string &flag,
    const std::string &collection, const std::string &pt,
    const std::string &eta, const std::string &phi, const std::string &mass,
    bool maximum_mass, float min_mass, float min_deta,
    float min_leading_pt, float min_subleading_pt) {
    const auto pair_col = index1 + "_pair";
    auto result = df.Define(pair_col,
        [maximum_mass](const ROOT::RVec<int> &indices,
                       const ROOT::RVec<float> &pts, const ROOT::RVec<float> &etas,
                       const ROOT::RVec<float> &phis, const ROOT::RVec<float> &masses) {
            return SelectDijet(indices, pts, etas, phis, masses, maximum_mass);
        }, {collection, pt, eta, phi, mass})
        .Define(index1, [](const ROOT::RVec<int> &pair) { return pair[0]; }, {pair_col})
        .Define(index2, [](const ROOT::RVec<int> &pair) { return pair[1]; }, {pair_col})
        .Define(mjj, [](int a, int b, const ROOT::RVec<float> &pts,
                       const ROOT::RVec<float> &etas, const ROOT::RVec<float> &phis,
                       const ROOT::RVec<float> &masses) {
            if (a < 0 || b < 0) return -1.;
            const ROOT::Math::PtEtaPhiMVector p1(pts.at(a), etas.at(a), phis.at(a), masses.at(a));
            const ROOT::Math::PtEtaPhiMVector p2(pts.at(b), etas.at(b), phis.at(b), masses.at(b));
            return (p1 + p2).M();
        }, {index1, index2, pt, eta, phi, mass})
        .Define(deta, [](int a, int b, const ROOT::RVec<float> &etas) {
            return a < 0 || b < 0 ? -1.f : std::abs(etas.at(a) - etas.at(b));
        }, {index1, index2, eta});
    return result.Define(flag,
        [=](int a, int b, double mass_value, float delta_eta, const ROOT::RVec<float> &pts) {
            return a >= 0 && b >= 0 && mass_value > min_mass &&
                   delta_eta > min_deta && pts.at(a) > min_leading_pt &&
                   pts.at(b) > min_subleading_pt;
        }, {index1, index2, mjj, deta, pt});
}
} // namespace jet
