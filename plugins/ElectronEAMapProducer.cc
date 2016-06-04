#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"

using namespace edm;
using namespace std;

namespace cat {

class ElectronEAMapProducer : public edm::stream::EDProducer<>
{
public:
  ElectronEAMapProducer(const edm::ParameterSet& pset);
  virtual ~ElectronEAMapProducer() { }

  void produce(edm::Event & event, const edm::EventSetup&) override;

private:
  edm::EDGetTokenT<edm::View<reco::Candidate> > candToken_;
  EffectiveAreas effectiveAreas_;

};

} // namespace

using namespace cat;

typedef std::vector<int> vint;
typedef std::vector<vint> vvint;

ElectronEAMapProducer::ElectronEAMapProducer(const edm::ParameterSet& pset):
  effectiveAreas_(pset.getParameter<edm::FileInPath>("effAreas").fullPath())
{
  candToken_ = consumes<edm::View<reco::Candidate> >(pset.getParameter<edm::InputTag>("src"));
  produces<edm::ValueMap<float> >("");
}

void ElectronEAMapProducer::produce(edm::Event& event, const edm::EventSetup&)
{
  edm::Handle<edm::View<reco::Candidate> > candHandle;
  event.getByToken(candToken_, candHandle);
  std::vector<float> values;
  for ( auto el = candHandle->begin(); el != candHandle->end(); ++el ) {
    const double aeta = std::abs(el->eta());
    values.push_back(effectiveAreas_.getEffectiveArea(aeta));
  }

  std::auto_ptr<edm::ValueMap<float> > vMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler filler(*vMap);
  filler.insert(candHandle, values.begin(), values.end());
  filler.fill();

  event.put(vMap);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(ElectronEAMapProducer);
