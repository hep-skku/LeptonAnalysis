#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Candidate/interface/Candidate.h"

using namespace edm;
using namespace std;

namespace cat {

class CandToWeightProductProducer : public edm::stream::EDProducer<>
{
public:
  CandToWeightProductProducer(const edm::ParameterSet& pset);
  virtual ~CandToWeightProductProducer() { }

  void produce(edm::Event & event, const edm::EventSetup&) override;

private:
  //edm::EDGetTokenT<reco::GenParticleCollection> genParticlesToken_;
  edm::EDGetTokenT<edm::View<reco::Candidate> > candToken_;
  std::vector<edm::EDGetTokenT<float> > fTokens_;
  std::vector<edm::EDGetTokenT<int> > iTokens_;

};

} // namespace

using namespace cat;

typedef std::vector<int> vint;
typedef std::vector<vint> vvint;

CandToWeightProductProducer::CandToWeightProductProducer(const edm::ParameterSet& pset)
{
  candToken_ = consumes<edm::View<reco::Candidate> >(pset.getParameter<edm::InputTag>("src"));
  for ( auto label : pset.getParameter<std::vector<edm::InputTag> >("weights") ) {
    fTokens_.push_back(consumes<float>(label));
    iTokens_.push_back(mayConsume<int>(label));
  }

  produces<edm::ValueMap<float> >("");
}

void CandToWeightProductProducer::produce(edm::Event& event, const edm::EventSetup&)
{
  double weight = 1.0;
  edm::Handle<float> fHandle;
  edm::Handle<int> iHandle;
  for ( int i=0, n=fTokens_.size(); i<n; ++i ) {
    if      ( event.getByToken(fTokens_[i], fHandle) ) weight *= *fHandle;
    else if ( event.getByToken(iTokens_[i], iHandle) ) weight *= *iHandle;
  }

  edm::Handle<edm::View<reco::Candidate> > candHandle;
  event.getByToken(candToken_, candHandle);
  std::vector<float> values;
  for ( int i=0, n=candHandle->size(); i<n; ++i ) values.push_back(weight);

  std::auto_ptr<edm::ValueMap<float> > vMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler filler(*vMap);
  filler.insert(candHandle, values.begin(), values.end());
  filler.fill();
  event.put(vMap);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(CandToWeightProductProducer);
