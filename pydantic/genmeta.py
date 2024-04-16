import json
from typing import Union, List

# import streamlit as st
from pydantic import BaseModel, Field
# import streamlit_pydantic as sp

from pydantic.config import ConfigDict

def pop_default(s):
    s.pop('default')

class smallMolecule(BaseModel):
    
    model_config = ConfigDict(title="Small Molecule", 
                              description="Molecules with a low molecular weight (generally < 900 daltons) used to perturb the experimental system, often binding to specific biological targets.")

    entity: str = Field(default="Small Molecule", 
                                         json_schema_extra={"const": "Small Molecule", "format": "hidden"})
    smallMoleculeName: str = Field(title="Small Molecule Name", 
                                   description="The common, primary, recognizable name for the small molecule being used.")
    smallMoleculeLabBatchLabel: str = Field(title="Lab Batch Label",
                                             description="Lab-specific ID for the batch of small molecule used in the experiment.", default="", json_schema_extra=pop_default)
    smallMoleculeDuration: float = Field(title="Duration", 
                                         description="Amount of time the experimental system was exposed to the small molecule.")
    smallMoleculeDurationUnits: str = Field(title="Duration Units",
                                             description="Time units of exposure (e.g. second, minute, hour). Name of unit must be chosen from the Units of Measurement Ontology and must be a child term of 'time unit'.")
    smallMoleculeConcentration: float = Field(title="Concentration", 
                                              description="Concentration of small molecule the experimental system was exposed to.")
    smallMoleculeConcentrationUnits: str = Field(title="Concentration Units", 
                                                 description="Concentration units of exposure (e.g. nanomolar, micromolar, millimolar). Name of unit must be chosen from the Units of Measurement Ontology and must be a child term of 'concentration unit'.")

class crisprKnockout(BaseModel):
    
    model_config = ConfigDict(title="CRISPR Knockout", 
                              description="A Cas9/gRNA ribonucleoprotein complex that introduces permanent loss-of-function mutations in a gene.")

    entity: str = Field(default="CRISPR Knockout", 
                                         json_schema_extra={"const": "CRISPR Knockout", 
                                                            "format": "hidden"})
    crisprKnockoutName: str = Field(title="Name", 
                            description="The primary name of the CRISPR reagent.")
    crisprKnockoutLabBatchLabel: str = Field(title="Lab Batch Label", 
                                     description="Lab-specific ID for the batch of CRISPR reagent used in the experiment.", default="", json_schema_extra=pop_default)
    crisprKnockoutTargetGeneSymbol: str = Field(title="Target Gene Symbol",
                                         description="The HGNC (human), MGI (mouse), RGD (rat), or ZFIN (zebrafish) symbol of the gene knocked out by CRISPR for knockout, or VGNC gene symbols for other vertebrate species.")
    crisprKnockoutTargetGeneId: str = Field(title="NCBI Entrez ID for Target Gene", 
                                    description="The NCBI Entrez Gene ID for the gene knocked out by CRISPR.", default="", json_schema_extra=pop_default)
    crisprKnockoutTargetGeneSpecies: str = Field(title="Target Gene Species", 
                                         description="The species of the target locus, with name chosen from the NCBI Taxonomy. Must be a child term of 'cellular organisms'.")
    crisprKnockoutDuration: float = Field(title="Duration", 
                                         description="Amount of time the experimental system was exposed to the small molecule.")
    crisprKnockoutDurationUnits: str = Field(title="Duration Units",
                                             description="Time units of exposure (e.g. second, minute, hour). Name of unit must be chosen from the Units of Measurement Ontology and must be a child term of 'time unit'.")
    # crisprKnockoutConcentration: str = Field(title="Concentration")

# class rnai(BaseModel):

#     model_config = ConfigDict(title="RNAi")
    
#     entity: str = Field(default="RNAi", 
#                                          json_schema_extra={"const": "RNAi",
#                                                             "format": "hidden"})
#     rnaiName: str = Field(title="Target Sequence")
#     rnaiDuration: str = Field(title="Duration")
#     rnaiConcentration: str = Field(title="Concentration")

# class antibody(BaseModel):

#     model_config = ConfigDict(title="Antibody")
    
#     entity: str = Field(default="Antibody", 
#                                          json_schema_extra={"const": "Antibody",
#                                                             "format": "hidden"})
#     antibodyName: str = Field(title="Antibody Name")
#     antibodyDuration: str = Field(title="Duration")
#     antibodyConcentration: str = Field(title="Concentration")

# class proteinP(BaseModel):
    
#     model_config = ConfigDict(title='Protein')

#     entity: str = Field(default="Protein", 
#                                          json_schema_extra={"const": "Protein",
#                                                             "format": "hidden"})
#     proteinPName: str = Field(title="Protein Name")
#     proteinPDuration: str = Field(title="Duration")
#     proteinPConcentration: str = Field(title="Concentration")

# class infectiousAgent(BaseModel):
    
#     model_config = ConfigDict(title="Infectious Agent")

#     entity: str = Field(default="Infectious Agent", 
#                                          json_schema_extra={"const": "Infectious Agent",
#                                                             "format": "hidden"})
#     infectiousAgentName: str = Field(title="Agent Name")
#     infectiousAgentDuration: str = Field(title="Duration")
#     infectiousAgentConcentration: str = Field(title="Concentration")

# class epigeneticModification(BaseModel):

    # model_config = ConfigDict(title="Epigenetic Modification")
    
    # entity: str = Field(default="Epigenetic Modification", 
    #                     json_schema_extra={"const": "Epigenetic Modification",
    #                                        "format": "hidden"})
    # epigeneticModificationName: str = Field(title="Modification Type")
    
# class protein(BaseModel):
    
    # model_config = ConfigDict(title="Protein", json_schema_extra={"ui": {
    #                                 "preview": {
    #                                  "visible": True
    #                                 }
    #                                 }
    #                             })

    # entity: str = Field(default="Protein", json_schema_extra={"const": "Protein",
    #                                                           "format": "hidden"})
    # proteinName: str = Field(title="Protein Name")
# class transcript(BaseModel):
    
    # model_config = ConfigDict(title="Transcript", json_schema_extra={"ui": {
    #                                 "preview": {
    #                                  "visible": True
    #                                 }
    #                                 }
    #                             })

    # entity: str = Field(default="Transcript", json_schema_extra={"const": "Transcript",
    #                                                              "format": "hidden"})
    # transcriptName: str = Field(title="NCBI Accession Number", json_schema_extra={"ui": {
    #                                                                 "preview": {
    #                                                                 "visible": True
    #                                                              }
    #                                                         }})
# class gene(BaseModel):
    
    # model_config = ConfigDict(title="Gene", json_schema_extra={"ui": {
    #                                 "preview": {
    #                                  "visible": True
    #                                 }
    #                                 }
    #                             })

    # entity: str = Field(default="Gene", json_schema_extra={"const": "Gene",
    #                                                        "format": "hidden"})
    # geneName: str = Field(title="Gene Name", json_schema_extra={"ui": {
    #                                                                 "preview": {
    #                                                                 "visible": True
    #                                                              }
    #                                                         }})
# class tissue(BaseModel):
    
#     model_config = ConfigDict(title="Tissue", json_schema_extra={"ui": {
#                                     "preview": {
#                                      "visible": True
#                                     }
#                                     }
#                                 })
#     role: str = Field(default="Model System", json_schema_extra={"const": "Model System",
#                                                              "format": "hidden"})
#     entity: str = Field(default="Tissue", json_schema_extra={"const": "Tissue",
#                                                              "format": "hidden"})
#     tissueType: str = Field(title="Tissue Type", json_schema_extra={"ui": {
#                                                                     "preview": {
#                                                                     "visible": True
#                                                                  }
#                                                             }})
#     tissueLabBatchLabel: str = Field(default="", title="Lab Batch Label", json_schema_extra={"ui": {
#                                                                     "preview": {
#                                                                     "visible": True
#                                                                  }
#                                                             }})
#     tissueOrganism: str = Field(title="Organism of Origin", json_schema_extra={"ui": {
#                                                                     "preview": {
#                                                                     "visible": True
#                                                                  }
#                                                             }})

# class primaryCells(BaseModel):

#     model_config = ConfigDict(title="Primary Cells", json_schema_extra={"ui": {
#                                     "preview": {
#                                      "visible": True
#                                     }
#                                     }
#                                 })
#     role: str = Field(default="Model System", 
#                         json_schema_extra={"const": "Model System",
#                                            "format": "hidden"})
#     entity: str = Field(default="Primary Cells", 
#                         json_schema_extra={"const": "Primary Cells",
#                                            "format": "hidden"})
#     primaryCellsType: str = Field(title="Cell Type", json_schema_extra={"ui": {
#                                                                     "preview": {
#                                                                     "visible": True
#                                                                  }
#                                                             }})

# class differentiatedCells(BaseModel):
    
#     model_config = ConfigDict(title="Differentiated Cells", json_schema_extra={"ui": {
#                                     "preview": {
#                                      "visible": True
#                                     }
#                                     }
#                                 })
#     role: str = Field(default="Model System", 
#                         json_schema_extra={"const": "Model System",
#                                            "format": "hidden"})
#     entity: str = Field(default="Differentiated Cells", 
#                         json_schema_extra={"const": "Differentiated Cells",
#                                            "format": "hidden"})
#     differentiatedCellsType: str = Field(title="Cell Type", json_schema_extra={"ui": {
#                                                                     "preview": {
#                                                                     "visible": True
#                                                                  }
#                                                             }})
#     precursorCellName: str = Field(title="Precursor Cell Name")
# class ipsc(BaseModel):
    
#     model_config = ConfigDict(title="iPSC", json_schema_extra={"ui": {
#                                     "preview": {
#                                      "visible": True
#                                     }
#                                     }
#                                 })

#     role: str = Field(default="Model System", 
#                         json_schema_extra={"const": "Model System",
#                                            "format": "hidden"})
#     entity: str = Field(default="iPSC", json_schema_extra={"const": "iPSC",
#                                                            "format": "hidden"})
#     ipscId: str = Field(title="iPSC ID", json_schema_extra={"ui": {
#                                                                     "preview": {
#                                                                     "visible": True
#                                                                  }
#                                                             }})

class cellLine(BaseModel):

    model_config = ConfigDict(title="Cell Line", 
                              description="Immortalized (naturally or engineered), genetically uniform tissue cells able to reproduce indefinitely in standard culture conditions."
                              )
    role: str = Field(default="Model System",
                                            json_schema_extra={"const": "Model System",
                                           "format": "hidden"})
    entity: str = Field(default="Cell Line", 
                                            json_schema_extra={"const": "Cell Line",
                                                                "format": "hidden",
                                                                })
    cellLineName: str = Field(title="Name", 
                              description="The cell line name as found in the Cell Line Ontology. Must be a child term of 'immortal cell line cell'." 
                              )
    cellLineLabBatchLabel: str = Field(title="Lab Batch Label", 
                                       description="Lab-specific ID for the  batch of cells used in the experiment.", default="", json_schema_extra=pop_default)
    cellLineTissue: str = Field(title="Tissue of Origin", 
                                description="Tissue from which the cell line was derived, with name chosen from NCI Thesaurus, Brenda Tissue Ontology, or UBERON. Must be a child term of 'Tissue (NCIT)', 'tissues, cell types, and enzyme sources (BTO), or tissue (UBERON)'."
                                )
    cellLineOrgan: str = Field(title="Organ of Origin", 
                               description="Organ from which the cell line was derived, with name chosen from NCI Thesaurus, UBERON, or FMA. Must be a child term of 'organ'.",
                               default="",
                               json_schema_extra=pop_default)
    cellLineSpecies: str = Field(title="Species of Origin", 
                                  description="Species from which the cell line was derived, with name chosen from the NCBI Taxonomy. Must be a child term of 'cellular organisms'."
                                  )
    cellLineDisease: str = Field(title="Disease", 
                                 description="If the cell line came from a diseased tissue, the disease name must be taken from the Disease Ontology. Must be a child term of 'disease'. Leave blank if the origin tissue or cells were not diseased.",
                                 default="",
                                 json_schema_extra=pop_default)



# class wastewater(BaseModel):
    
    # model_config = ConfigDict(title="Wastewater", json_schema_extra={"ui": {
    #                                 "preview": {
    #                                  "visible": True
    #                                 }
    #                                 }
    #                             })

    # entity: str = Field(default="Wastewater", json_schema_extra={"const": "Wastewater",
    #                                                              "format": "hidden"})
    # wastewaterName: str = Field(title="Sample ID", json_schema_extra={"ui": {
    #                                                                 "preview": {
    #                                                                 "visible": True
    #                                                              }
    #                                                         }})

class patientSample(BaseModel):
    
    model_config = ConfigDict(title="Patient Sample")
    role: str = Field(default="Biospecimen", 
                        json_schema_extra={"const": "Biospecimen",
                                           "format": "hidden"})
    entity: str = Field(default="Patient Sample", 
                        json_schema_extra={"const": "Patient Sample",
                                           "format": "hidden"})
    patientSampleId: str = Field(title="Patient Sample ID")
    patientSampleDisease: str = Field(title="Disease", 
                                      description="If the sample came from diseased tissue, the disease name must be taken from the Disease Ontology. Must be a child term of 'disease'. Leave blank if the tissue was not diseased.",
                                      default="",
                                      json_schema_extra=pop_default)
   
# class target(BaseModel):
    
    # model_config = ConfigDict(title="Molecular Target", json_schema_extra={"ui": {
    #                                 "preview": {
    #                                  "visible": True
    #                                 }
    #                                 }
    #                             })

    # entity: str = Field(default="Molecular Target", 
    #                                      json_schema_extra={"const": "Molecular Target",
    #                                                         "format": "hidden"})
    # content: Union[
    #         gene,
    #         transcript,
    #         protein,
    #         epigeneticModification
    #         ] = Field(json_schema_extra={
    #                               "ui": {
    #                                 "preview": {
    #                                 "visible": True
    #                                 }}})


# class biospecimen(BaseModel):
    
    # model_config = ConfigDict(title="Biospecimen", json_schema_extra={"ui": {
    #                                 "preview": {
    #                                  "visible": True
    #                                 }
    #                                 }
    #                             })

    # entity: str = Field(default="Biospecimen", json_schema_extra={"const": "Biospecimen",
    #                                                               "format": "hidden"})
    # content: Union[
    #         patientSample,
    #         wastewater
    #         ] = Field(json_schema_extra={
    #                               "ui": {
    #                                 "preview": {
    #                                 "visible": True
    #                                 }}})
    

# class modelSystem(BaseModel):

    # model_config = ConfigDict(title="Model System", json_schema_extra={"ui": {
    #                                 "preview": {
    #                                  "visible": True
    #                                 }
    #                                 }
    #                             })
    
    # entity: str = Field(default="Model System", 
    #                                      json_schema_extra={"const": "Model System",
    #                                                         "format": "hidden"})
    # content: Union[
    #         cellLine,
    #         ipsc,
    #         primaryCells,
    #         differentiatedCells,
    #         tissue
    #         ] = Field(json_schema_extra={"ui": {
    #                                 "preview": {
    #                                 "visible": True
    #                                 }
    #                             }})

class sample(BaseModel):

    model_config = ConfigDict(title="Sample", json_schema_extra={
                        "version": "0.0.1"
            })
    
    name: str = Field(title='Sample Name', 
                      description="Please provide a unique name for the sample.")
    description: str = Field(title="Sample Description", 
                             description="Please include a description or any other helpful comments or annotations for the sample.")
    experimentalSystem: Union[
            cellLine,
            # primaryCells
            # differentiatedCells,
            # ipsc,
            # tissue
            patientSample
            ] = Field(title="Experimental System", json_schema_extra={
                                  "type": "object"
                            })
    perturbation: List[Union[
        smallMolecule,
        crisprKnockout
        # rnai,
        # antibody,
        # proteinP,
        # infectiousAgent
            ] 
        ]
                 

def example():
    """ run this to see the schema dumped """
    with open ("genmeta_schema.json", "w") as ft:
        print(json.dumps(sample.model_json_schema(), indent=2), 
              file = ft)

example()

# data = sp.pydantic_form(key="my_form", model=ExperimentalSubject)
# if data:
#     st.json(data.json())