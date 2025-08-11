# ruff: noqa

import json
from datetime import date
from typing import Union, List
from enum import Enum

from pydantic import BaseModel, Field

from pydantic.config import ConfigDict
from pydantic._internal._core_utils import is_core_schema, CoreSchemaOrField
from pydantic.json_schema import GenerateJsonSchema

def delete_empty_default(schema):
    for key in list(schema):
        if key == "default":
            if schema["default"] == "":
                schema.pop("default")
                continue
        if isinstance(schema[key], dict):
            delete_empty_default(schema[key])

class GenerateJsonSchemaWithoutDefaultTitles(GenerateJsonSchema):
    def field_title_should_be_set(self, schema: CoreSchemaOrField) -> bool:
        return_value = super().field_title_should_be_set(schema)
        if return_value and is_core_schema(schema):
            return False
        return return_value

class smokingStatus(Enum):
    smoker = "Smoker"
    nonSmoker = "Non-smoker"

class specimenOrigin(Enum):
    tissue = "Tissue"
    liquid = "Liquid"

class tumorSampleTypeEnum(Enum):
    primarySite = "Primary Site"
    localRecurrence = "Local Recurrence"
    distantMetastasis = "Distant Metastasis"

class donorInformation(BaseModel):
    model_config = ConfigDict(title="Patient/Donor Information")

    species: str = Field(title="Species", description="Species from which the sample material was extracted, with name chosen from the NCBI Taxonomy. Must be a child term of 'cellular organisms'.")

    gender: str = Field(default="", title="Gender", description="The self-identified gender of the donor in case of a human, the biological sex in case of a non-human donor.")

    primaryRace: str = Field(default="", title="Primary Race", description="The primary race indicated by a human donor.")

    strain: str = Field(default="", title="Strain/Breed", description="The strain or breed of the model organism in case of a non-human donor.")

    ethnicity: str = Field(default="", title="Ethnicity", description="The ethnic group of origin of a human donor.")

    dateOfBirth: date = Field(default="", title="Date of Birth", description="The date of the donor's birth.")

    age: int = Field(default="", title="Age", description="The donor's age at the time of collection of the sample. Age units will be specified in the next field.")

    ageUnits: str = Field(default="", title="Age Units", description="The units of time in which the age is recorded.")

    ageGroup: str = Field(default="", title="Age Group", description="The age group of the donor.")

    intervalDeath: int = Field(default="", title="Interval of Death", description="The number of days between the donor's date of birth and date of death. Report the time units in the Age Units field.")

    tobaccoSmokingHistory: bool = Field(default="", title="Tobacco Smoking History", description="In the case of a human, the donor's self-reported smoking history. True if the patient has ever smoked.")

    tobaccoSmokingStatus: smokingStatus = Field(default="", title="Tobacco Smoking Status", description="In the case of a human, the status of the donor as a smoker or non-smoker at the time the sample was collected.")

    icd10Code: str = Field(default="", title="ICD10 Code", description="In the case of a human donor that is diseased, the ICD-10 code for the diagnosis associated with the sample material coming from pathology reports and chart reviews, if the sample itself is diseased, or the relevant diagnosis code for the patient if the sample material itself is healthy (e.g. normal tissue from a cancer patient).")

    icd10Description: str = Field(default="", title="ICD10 Description", description="In the case of a human donor that is diseased, the ICD-10 code description for the diagnosis associated with the sample material coming from pathology reports and chart reviews, if the sample itself is diseased, or the relevant diagnosis code description for the patient if the sample material itself is healthy (e.g. normal tissue from a cancer patient).")

    pathologicDiagnosis: str = Field(default="", title="Pathologic Diagnosis", description="In the case of a human donor who is diseased, pathologic diagnosis recorded by the provider or researcher relevant to the study or sample material. In the case of a non-human donor that is diseased, name of the disease.")
     
class smallMolecule(BaseModel):
    
    model_config = ConfigDict(title="Small Molecule", 
                              description="Molecules with a low molecular weight (generally < 900 daltons) used to perturb the model system, often binding to specific biological targets.")
    
    role: str = Field(default="Perturbagen", 
                        json_schema_extra={"const": "Perturbagen",
                                           "format": "hidden"})

    entity: str = Field(default="Small Molecule", 
                                         json_schema_extra={"const": "Small Molecule", "format": "hidden"})
    
    smallMoleculeId: str = Field(default="", json_schema_extra={"format": "hidden"})

    smallMoleculeName: str = Field(title="Small Molecule Name", 
                                   description="The common, primary, recognizable name for the small molecule being used.")
    smallMoleculeLabBatchLabel: str = Field(title="Lab Batch Label",
                                             description="Lab-specific ID for the batch of small molecule used in the experiment.", default="")
    smallMoleculeConcentration: float = Field(default="", title="Concentration", 
                                              description="Concentration of small molecule the model system was exposed to.")
    smallMoleculeConcentrationUnits: str = Field(default="", title="Concentration Units", 
                                                 description="Concentration units of exposure (e.g. nanomolar, micromolar, millimolar). Name of unit must be chosen from the Experimental Factor Ontology (EFO) or the Units of Measurement Ontology (UO) and must be a child term of 'concentration unit'.")
    smallMoleculeDuration: float = Field(default="", title="Duration", 
                                         description="Amount of time the model system was exposed to the small molecule.")
    smallMoleculeDurationUnits: str = Field(default="", title="Duration Units",
                                             description="Time units of exposure (e.g. second, minute, hour). Name of unit must be chosen from the Units of Measurement Ontology (UO) and must be a child term of 'time unit'.")

class crisprKnockout(BaseModel):
    
    model_config = ConfigDict(title="CRISPR Knockout", 
                              description="A Cas9/gRNA ribonucleoprotein complex that introduces permanent loss-of-function mutations in a gene.")
    
    role: str = Field(default="Perturbagen", 
                        json_schema_extra={"const": "Perturbagen",
                                           "format": "hidden"})

    entity: str = Field(default="CRISPR Knockout", 
                                         json_schema_extra={"const": "CRISPR Knockout", 
                                                            "format": "hidden"})
    crisprKnockoutName: str = Field(title="Name", 
                            description="The primary name of the CRISPR reagent.")
    crisprKnockoutLabBatchLabel: str = Field(title="Lab Batch Label", 
                                     description="Lab-specific ID for the batch of CRISPR reagent used in the experiment.", default="")
    crisprKnockoutTargetGeneSymbol: str = Field(title="Target Gene Symbol",
                                    description="The HGNC (human), MGI (mouse), RGD (rat), or ZFIN (zebrafish) symbol of the gene knocked out by CRISPR for knockout, or VGNC gene symbols for other vertebrate species.")
    crisprKnockoutTargetGeneId: str = Field(title=
                                            "NCBI Entrez ID for Target Gene",
                                            description="The NCBI Entrez Gene ID for the gene knocked out by CRISPR.", default="")
    crisprKnockoutTargetGeneSpecies: str = Field(title="Target Gene Species", 
                                         description="The species of the target locus, with name chosen from the NCBI Taxonomy. Must be a child term of 'cellular organisms'.")
    crisprKnockoutDuration: float = Field(default="", title="Duration", 
                                         description="Amount of time the model system was exposed to the CRISPR reagent.")
    crisprKnockoutDurationUnits: str = Field(default="", title="Duration Units",
                                             description="Time units of exposure (e.g. second, minute, hour). Name of unit must be chosen from the Units of Measurement Ontology (UO) and must be a child term of 'time unit'.")
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

class protein(BaseModel):
    
    model_config = ConfigDict(title='Protein', description="Natural or engineered perturbagens consisting of large, heavy polypeptide chains structured by primary, secondary, tertiary, and quaternary structures.  Includes, but not limited to, enzymes, cofactors, signaling molecules, adhesion molecules, and structural chains.  Antibodies, while proteins, are defined separately as Antibody perturbagens.")

    role: str = Field(default="Perturbagen", 
                        json_schema_extra={"const": "Perturbagen",
                                           "format": "hidden"})

    entity: str = Field(default="Protein", 
                                         json_schema_extra={"const": "Protein",
                                                            "format": "hidden"})
    proteinName: str = Field(title="Name", description="The primary name of the protein.")
    proteinLabBatchLabel: str = Field(title="Lab Batch Label", description="Lab-specific ID for the batch of protein used in the experiment.", default="")
    proteinUniProtId: str = Field(title="UniProt ID", description="The UniProt ID of the specific protein and, if relevant, isoform.", default="")
    proteinConcentration: float = Field(default="", title="Concentration", 
                                              description="Concentration of protein that the model system was exposed to.")
    proteinConcentrationUnits: str = Field(default="", title="Concentration Units", 
                                                 description="Concentration units of exposure (e.g. nanomolar, micromolar, millimolar). Name of unit must be chosen from the Experimental Factor Ontology (EFO) or the Units of Measurement Ontology (UO) and must be a child term of 'concentration unit'.")
    proteinDuration: float = Field(default="", title="Duration", description="Amount of time the model system was exposed to the protein.")
    proteinDurationUnits: str = Field(default="", title="Duration Units",
                                             description="Time units of exposure (e.g. second, minute, hour). Name of unit must be chosen from the Units of Measurement Ontology (UO) and must be a child term of 'time unit'.")
   

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
#                                                              "formjson_schema_extraat": "hidden"})
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

class primaryCell(BaseModel):

    model_config = ConfigDict(title="Primary Cells", description="Cells obtained from homogeneous tissue, such as a singular organ or organ sub-structure, and maintained in culture temporarily for experimental purposes.  Only viable for a limited time after isolation.")

    role: str = Field(default="Model System", 
                        json_schema_extra={"const": "Model System",
                                           "format": "hidden"})
    entity: str = Field(default="Primary Cells", 
                        json_schema_extra={"const": "Primary Cells",
                                           "format": "hidden"})
    primaryCellName: str = Field(title="Name", description="Name of the type of cells, with the name chosen from the Cell Ontology (CL). Must be a child term of 'cell'.")

    primaryCellLabBatchLabel: str = Field(title='Lab Batch Label', description="Lab-specific ID for the  batch of cells used in the experiment", default="")

    primaryCellTissue: str = Field(title="Tissue of Origin", description="Tissue from which the cells were extracted, with name chosen from NCI Thesaurus, Brenda Tissue Ontology, or UBERON. Must be a child term of 'Tissue (NCIT)', 'tissues, cell types, and enzyme sources (BTO), or tissue (UBERON)'.")

    primaryCellOrgan: str = Field(title="Organ of Origin", description="Organ from which the cells were extracted, with name chosen from NCI Thesaurus, UBERON, or FMA. Must be a child term of 'organ'.", default="")

    primaryCellDisease: str = Field(title="Disease", description="If the cells are diseased, the disease name must be taken from the Disease Ontology. Must be a child term of 'disease'. Leave blank if the cells were not diseased when obtained from the donor.", default="")

    primaryCellDonorInformation: donorInformation = Field(default="", title="Donor Information", description="Information about the human or non-human donor from which the sample material was taken.")




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
    
    cellLineId: str = Field(default="", json_schema_extra={"format": "hidden"})

    cellLineName: str = Field(title="Name", 
                              description="The cell line name as found in the Cell Line Ontology. Must be a child term of 'immortal cell line cell'."
                              )
    cellLineLabBatchLabel: str = Field(title="Lab Batch Label", 
                                       description="Lab-specific ID for the  batch of cells used in the experiment.", default="")
    cellLineLabBatchId: str = Field(default="", description="A MongoDB ObjectId string", json_schema_extra={"format": "hidden"})
    cellLineTissue: str = Field(title="Tissue of Origin", 
                                description="Tissue from which the cell line was derived, with name chosen from NCI Thesaurus, Brenda Tissue Ontology, or UBERON. Must be a child term of 'Tissue (NCIT)', 'tissues, cell types, and enzyme sources (BTO), or tissue (UBERON)'."
                                )
    cellLineOrgan: str = Field(title="Organ of Origin", 
                               description="Organ from which the cell line was derived, with name chosen from NCI Thesaurus, UBERON, or FMA. Must be a child term of 'organ'.",default="")
    cellLineSpecies: str = Field(title="Species of Origin", 
                                  description="Species from which the cell line was derived, with name chosen from the NCBI Taxonomy. Must be a child term of 'cellular organisms'.")
    cellLineDisease: str = Field(title="Disease", 
                                 description="If the cell line came from a diseased tissue, the disease name must be taken from the Disease Ontology. Must be a child term of 'disease'. Leave blank if the origin tissue or cells were not diseased.",
                                 default="")

class cellLinePerturbagen(BaseModel):

    model_config = ConfigDict(title="Cell Line", 
                              description="Immortalized (naturally or engineered), genetically uniform tissue cells able to reproduce indefinitely in standard culture conditions."
                              )
    role: str = Field(default="Perturbagen",
                                            json_schema_extra={"const": "Perturbagen",
                                           "format": "hidden"})
    entity: str = Field(default="Cell Line", 
                                            json_schema_extra={"const": "Cell Line",
                                                                "format": "hidden",
                                                                })
    
    cellLineId: str = Field(default="", json_schema_extra={"format": "hidden"})

    cellLineName: str = Field(title="Name", 
                              description="The cell line name as found in the Cell Line Ontology. Must be a child term of 'immortal cell line cell'."
                              )
    cellLineLabBatchLabel: str = Field(title="Lab Batch Label", 
                                       description="Lab-specific ID for the  batch of cells used in the experiment.", default="")
    cellLineLabBatchId: str = Field(default="", description="A MongoDB ObjectId string", json_schema_extra={"format": "hidden"})
    cellLineTissue: str = Field(title="Tissue of Origin", 
                                description="Tissue from which the cell line was derived, with name chosen from NCI Thesaurus, Brenda Tissue Ontology, or UBERON. Must be a child term of 'Tissue (NCIT)', 'tissues, cell types, and enzyme sources (BTO), or tissue (UBERON)'."
                                )
    cellLineOrgan: str = Field(title="Organ of Origin", 
                               description="Organ from which the cell line was derived, with name chosen from NCI Thesaurus, UBERON, or FMA. Must be a child term of 'organ'.",default="")
    cellLineSpecies: str = Field(title="Species of Origin", 
                                  description="Species from which the cell line was derived, with name chosen from the NCBI Taxonomy. Must be a child term of 'cellular organisms'.")
    cellLineDisease: str = Field(title="Disease", 
                                 description="If the cell line came from a diseased tissue, the disease name must be taken from the Disease Ontology. Must be a child term of 'disease'. Leave blank if the origin tissue or cells were not diseased.",
                                 default="")


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

# class patientSample(BaseModel):
    
#     model_config = ConfigDict(title="Patient Sample")
#     role: str = Field(default="Biospecimen", 
#                         json_schema_extra={"const": "Biospecimen",
#                                            "format": "hidden"})
#     entity: str = Field(default="Patient Sample", 
#                         json_schema_extra={"const": "Patient Sample",
#                                            "format": "hidden"})
#     patientSampleId: str = Field(title="Patient Sample ID")
#     patientSampleDisease: str = Field(title="Disease", 
#                                       description="If the sample came from diseased tissue, the disease name must be taken from the Disease Ontology. Must be a child term of 'disease'. Leave blank if the tissue was not diseased.",
#                                       default="",
#                                       json_schema_extra=pop_default)
class tetOnOff(Enum):
    tetOn = "Tet-ON"
    tetOff = "Tet-OFF"   

class tetExpressionSystem(BaseModel):
    model_config = ConfigDict(title="Tet Expression System") 

    role: str = Field(default="Perturbagen",
                                            json_schema_extra={"const": "Perturbagen",
                                           "format": "hidden"})
    entity: str = Field(default="Tet Expression System", 
                                            json_schema_extra={"const": "Tet Expression System",
                                                                "format": "hidden",
                                                                })

    transactivatorVectorName: str = Field(default="", title="Transactivator Vector Name", description="The name of the vector/plasmid containing the gene for the tetracycline transactivator protein.")

    transactivatorType: tetOnOff = Field(title="Transactivator Type", description="Tet-On or Tet-Off.")

    transactivatorProteinName: str = Field(title="Transactivator Protein Name", description="The name of the specific transactivator protein encoded by the vector, e.g. tTA, rtTA, rtTA2, etc.")

    transactivatorVectorLabBatchLabel: str = Field(default="", title="Transactivator Vector Lab Batch Label", description="Lab-specific ID for the batch of transactivator vector.")

    responseVectorName: str = Field(default="", title="Response Vector Name", description="The name of the vector/plasmid containing the gene(s) under control of the tetracycline response element (TRE).")

    responseVectorGeneOfInterest: str = Field(default="", title="Response Vector Gene of Interest", description="The gene being regulated under the Tet system.")

    responseVectorReporterGene: str = Field(default="", title="Response Vector Reporter Gene", description="If present, the reporter gene used to monitor expression.")

    responseVectorPromoter: str = Field(default="", title="Response Vector Promoter", description="The type of promoter making up the TRE in the response vector.")

    responseVectorLabBatchLabel: str = Field(default="", title="Response Vector Lab Batch Label", description="Lab-specific ID for the batch of response vector.")

    tetLabName: str = Field(default="", title="Lab Name", description="Name of the lab running the experiment.")

    doxLabBatchLabel: str = Field(default="", title="Doxycycline Lab Batch Label", description="Lab-specific ID for the batch of doxycycine used in the experiment.")

    doxConcentration: float = Field(default="", title="Doxycycline Concentration", description="Concentration of doxycycline the model system was incubated with.")

    doxConcentrationUnits: str = Field(default="", title="Doxycycline Concentration Units", description="Concentration units of incubation with doxycycline.")

    doxDuration: float = Field(default="", title="Doxycycline Incubation Time", description="Time of incubation with doxycycline.")

    doxDurationUnits: str = Field(default="", title="Doxycycline Incubation Time Units", description="Time units of incubation with doxycycline.")

    doxVehicle: str = Field(default="", title="Doxycycline Vehicle", description="Solvent used to dissolve doxycycline.")

    transfectionTransductionMethod: str = Field(default="", title="Transfection/Transduction Method", description="Method used for introducing the Tet expression system (e.g. lipofection, electroporation, viral transduction.")

    transfectionTransductionReagent: str = Field(default="", title="Transfection/Transduction Reagent", description="Specific transfection reagent or virus used (e.g. lipofectamine, lentivirus, adenovirus.")

class tumorSample(BaseModel):
    model_config = ConfigDict(title="Tumor Sample")

    role: str = Field(default="Model System",
                                            json_schema_extra={"const": "Model System",
                                           "format": "hidden"})
    entity: str = Field(default="Tumor Sample", 
                                            json_schema_extra={"const": "Tumor Sample",
                                                                "format": "hidden",
                                                                })

    tumorType: str = Field(title="Tumor Type", description="The type of cancer or benign tumor, preferably using OncoTree terminology.")

    resectionSite: str = Field(default="", title="Resection Site", description="The anatomical, organ, and/or tissue location where the resection for the tumor sample was performed.")

    tumorSpecimenOrigin: specimenOrigin = Field(default="", title="Specimen Origin", description="The type of biopsy performed for specimen collection: tissue or liquid.") 

    tumorSampleType: tumorSampleTypeEnum = Field(default="", title="Sample Type", description="The tumor sample's type based on its location: primary site, site of local recurrence, or distant metastasis.")

    tumorOrgan: str = Field(default="", title="Organ of Origin", description="The organ in which the tumor originated.")

    tumorTissue: str = Field(default="", title="Tissue of Origin", description="The tissue type in which the tumor originated.")

    tumorCellType: str = Field(default="", title="Cell Type of Origin", description="The type of cell from which the tumor originated.")

    tumorPrimaryDiseaseSite: str = Field(default="", title="Primary Disease Site", description="Diagnosis site granular grouper for standarization.")

    tumorSampleDonorInformation: donorInformation = Field(default="", title="Donor Information", description="Information about the human or non-human donor from which the sample material was taken.")

class tissue(BaseModel):
    model_config = ConfigDict(title="Tissue")

    role: str = Field(default="Model System",
                                            json_schema_extra={"const": "Model System",
                                           "format": "hidden"})
    entity: str = Field(default="Tissue", 
                                            json_schema_extra={"const": "Tissue",
                                                                "format": "hidden",
                                                                })
    
    tissueType: str = Field(title="Tissue Type", description="The type of tissue sampled.")

    tissueOrgan: str = Field(default="", title="Organ of Origin", description="The organ in which the tissue was located.")

    tissueDisease: str = Field(default="", title="Disease", description="If the tissue was diseased, the disease name must be taken from the Disease Ontology. Must be a child term of 'disease'. Leave blank if the tissue was not diseased when obtained from the donor.")

    tissueDonorInformation: donorInformation = Field(default="", title="Donor Information", description="Information about the human or non-human donor from which the sample material was taken.")

class sample(BaseModel):

    model_config = ConfigDict(title="Sample", json_schema_extra={
                        "version": "0.1.9"
            })
    
    name: str = Field(title='Sample Name', 
                      description="Please provide a unique name for the sample.")
    description: str = Field(default="", title="Sample Description", 
                             description="Please include a description or any other helpful comments or annotations for the sample.")
    experimentalSystem: Union[
            cellLine,
            primaryCell,
            tumorSample,
            # differentiatedCells,
            # ipsc,
            tissue
            # patientSample
            ] = Field(title="Model System", json_schema_extra={
                                  "type": "object"
                            })
    perturbation: List[Union[
        smallMolecule,
        crisprKnockout,
        # rnai,
        # antibody,
        protein,
        tetExpressionSystem,
        cellLinePerturbagen
        # infectiousAgent
            ] 
        ] = Field(default="", title="Perturbations")
                 

if __name__ == "__main__":
    json_schema=sample.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("json_schemas/sample/sample.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)