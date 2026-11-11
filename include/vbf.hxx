#ifndef CROWN_VBF_HXX
#define CROWN_VBF_HXX

#include <ROOT/RVec.hxx>
#include <Math/Vector4D.h>
#include <algorithm>
#include <cmath>

namespace jet {
// Input contains original NanoAOD indices after all jet selections.
// Sort again using corrected pT; stable ties preserve collection order.
inline ROOT::RVec<int> SelectDijet(ROOT::RVec<int> indices,
    const ROOT::RVec<float> &pt, const ROOT::RVec<float> &eta,
    const ROOT::RVec<float> &phi, const ROOT::RVec<float> &mass,
    bool maximum_mass) {
    std::stable_sort(indices.begin(), indices.end(),
                     [&](int a, int b) { return pt.at(a) > pt.at(b); });
    ROOT::RVec<int> pair{-1, -1};
    if (indices.size() < 2) return pair;
    if (!maximum_mass) return {indices[0], indices[1]};
    double best = -1.;
    for (size_t i = 0; i < indices.size(); ++i) {
        const int a = indices[i];
        const ROOT::Math::PtEtaPhiMVector p1(pt.at(a), eta.at(a), phi.at(a), mass.at(a));
        for (size_t j = i + 1; j < indices.size(); ++j) {
            const int b = indices[j];
            const ROOT::Math::PtEtaPhiMVector p2(pt.at(b), eta.at(b), phi.at(b), mass.at(b));
            const double mjj = (p1 + p2).M();
            // Strict comparison makes ties deterministic: first pair in pT order.
            if (std::isfinite(mjj) && mjj > best) {
                best = mjj;
                pair = {a, b};
            }
        }
    }
    return pair;
}
} // namespace jet
#endif
