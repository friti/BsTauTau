import ROOT
from DataFormats.FWLite import Events, Handle

# Load the file
events = Events("file:GEN-RunIII2024Summer24wmLHEGS-00004.root")

# Prepare to access genParticles
handle_gen = Handle("std::vector<reco::GenParticle>")
label_gen = ("genParticles", "", "GEN")

for i, event in enumerate(events):
    event.getByLabel(label_gen, handle_gen)
    gen_particles = handle_gen.product()

    for p in gen_particles:
        if abs(p.pdgId()) == 531:  # Bs meson
            print("Event",str(i),": Found Bs (PDG ID: ",str(p.pdgId()), "mass ",str(p.mass()))

            if p.numberOfMothers() > 0:
                mom = p.mother(0)
                print("Mother PDG ID:",str(mom.pdgId())," status:", str(mom.status()), "mass:", mom.mass())
            else:
                print("No mother")
    #if i >= 10:
    #    break
 
