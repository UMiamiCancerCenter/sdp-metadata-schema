import json
import re

from utils import (
    GenerateJsonSchemaWithoutDefaultTitles,
    Scope,
    delete_empty_default,
    to_title_case,
)

from pydantic import (
    BaseModel,
    Field,
)
from pydantic.json_schema import SkipJsonSchema


def to_camel(s: str) -> str:
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), s)

class CustomBaseModel(BaseModel):
    model_config = {"alias_generator": to_camel, "populate_by_name": True, "serialize_by_alias": True, "field_title_generator": to_title_case}
class UniChem(CustomBaseModel):

    chebi:    list[str] | SkipJsonSchema[None] = Field(default=None, title="ChEBI")
    chembl:   list[str] | SkipJsonSchema[None] = Field(default=None, title="ChEMBL")
    lincs:    list[str] | SkipJsonSchema[None] = Field(default=None, title="LINCS")
    pubchem:  list[str] | SkipJsonSchema[None] = Field(default=None, title="PubChem")
    drugbank: list[str] | SkipJsonSchema[None] = Field(default=None, title="DrugBank")

class PubChemSmiles(CustomBaseModel):

    canonical: str | SkipJsonSchema[None] = None


class Iupac(CustomBaseModel):

    systematic: str | SkipJsonSchema[None] = None


class PubChem(CustomBaseModel):

    cid: int | SkipJsonSchema[None] = Field(default=None, title="CID")
    inchi: str | SkipJsonSchema[None] = Field(default=None, title="InChI")
    inchikey: str | SkipJsonSchema[None] = Field(default=None, title="InChI Key")
    iupac: Iupac | SkipJsonSchema[None] = Field(default=None, title="IUPAC Name")
    smiles: PubChemSmiles | SkipJsonSchema[None] = Field(default=None, title="SMILES")
    molecular_formula: str | SkipJsonSchema[None] = Field(alias="molecularFormula", default=None)
    cas_number: str | SkipJsonSchema[None] = Field(default=None, title="CAS Number")

class Bioactivity(CustomBaseModel):
    activity_comment: str | SkipJsonSchema[None] = None
    standard_relation: str | SkipJsonSchema[None] = None
    standard_type: str | SkipJsonSchema[None] = None
    standard_units: str | SkipJsonSchema[None] = None
    standard_value: float | SkipJsonSchema[None] = None
    target_pref_name: str | SkipJsonSchema[None] = Field(default=None, title="Target Preferred Name")
    target_organism: str | SkipJsonSchema[None] = None

class Lincs(CustomBaseModel):

    id: str | SkipJsonSchema[None] = Field(default=None, title="LINCS ID")
    name: str | SkipJsonSchema[None] = None
    alternative_names: list[str] | SkipJsonSchema[None] = Field(alias="alternativeNames", default=None)
    alternative_ids:  list[str] | SkipJsonSchema[None] = Field(alias="alternativeIds",  default=None)
    pubchem_cid: int  | SkipJsonSchema[None] = Field(alias="pubchemCid", default=None, title="PubChem CID")
    chebi_id: list[int] | SkipJsonSchema[None] = Field(alias="chebiId", default=None, title="ChEBI ID")
    inchi_parent: str | SkipJsonSchema[None] = Field(alias="inchiParent", default=None, title="InChI Parent")
    inchi_key_parent: str | SkipJsonSchema[None] = Field(alias="inchiKeyParent", default=None, title="InChI Key Parent")
    smiles_parent: str | SkipJsonSchema[None] = Field(alias="smilesParent", default=None, title="SMILES Parent")

class MoleculeProperties(CustomBaseModel):

    full_mwt: float | SkipJsonSchema[None] = Field(default=None, title="Full Molecule Weight")
    hba: int | SkipJsonSchema[None] = Field(default=None, title="Hydrogen Bond Acceptors")
    hbd: int | SkipJsonSchema[None] = Field(default=None, title="Hydrogen Bond Donors")
    acd_logp: float | SkipJsonSchema[None] = Field(default=None, title="ACD LogP")
    qed_weighted: float | SkipJsonSchema[None] = Field(alias="qedWeighted", default=None, title="Quantitative Estimate of Drug-likeness")


class IndicationRefs(CustomBaseModel):

    clinical_trials: list[str] | SkipJsonSchema[None] = Field(alias="clinicalTrials", validation_alias="ClinicalTrials", default=None)
    fda: list[str] | SkipJsonSchema[None] = Field(default=None, alias="fda", validation_alias="FDA", title="FDA")

class DrugIndication(CustomBaseModel):

    efo_id: str | SkipJsonSchema[None] = Field(default=None, title="EFO ID")
    efo_term: str | SkipJsonSchema[None] = Field(default=None, title="EFO Term")
    first_approval: int | SkipJsonSchema[None] = None
    indication_refs: list[IndicationRefs] | SkipJsonSchema[None] = Field(default=None, title="Indication References")
    max_phase_for_ind: float | SkipJsonSchema[None] = Field(default=None, title="Max Phase for Indication")
    mesh_heading: str | SkipJsonSchema[None] = Field(default=None, title="MeSH Heading")

class TargetComponent(CustomBaseModel):

    accession: str | SkipJsonSchema[None] = None

class DrugMechanism(CustomBaseModel):

    mechanism_of_action: str | SkipJsonSchema[None] = Field(alias="mechanismOfAction", default=None)
    action_type: str | SkipJsonSchema[None] = Field(alias="actionType", default=None)
    target_name: str | SkipJsonSchema[None] = Field(alias="targetName", default=None)
    target_organism: str | SkipJsonSchema[None] = Field(alias="targetOrganism", default=None)
    target_type: str | SkipJsonSchema[None] = Field(alias="targetType", default=None)
    target_components: list[TargetComponent] | SkipJsonSchema[None] = Field(alias="targetComponents", default=None)


class MoleculeStructures(CustomBaseModel):

    standard_inchi_key: str | SkipJsonSchema[None] = Field(alias="standardInchiKey", default=None, title="Standard InChI Key")
    canonical_smiles: str | SkipJsonSchema[None] = Field(alias="canonicalSmiles", default=None)


class Biocomponent(CustomBaseModel):

    organism: str | SkipJsonSchema[None] = None


class Biotherapeutic(CustomBaseModel):

    biocomponents: list[Biocomponent] | SkipJsonSchema[None] = None


class MoleculeSynonym(CustomBaseModel):

    molecule_synonym: str | SkipJsonSchema[None] = None
    syn_type: str | SkipJsonSchema[None] = Field(default=None, title="Synonym Type")
    synonyms: list[str] | SkipJsonSchema[None] = None

class Xref(CustomBaseModel):
    xref_id: str | SkipJsonSchema[None] = Field(default=None, title="Cross-reference ID")
    xref_name: str | SkipJsonSchema[None] = Field(default=None, title="Cross-reference Name")
    xref_src_db: str | SkipJsonSchema[None] = Field(default=None, title="Cross-reference Source Database")

class Chembl(CustomBaseModel):

    molecule_chembl_id: str | SkipJsonSchema[None] = Field(default=None, title="ChEMBL ID")
    pref_name: str | SkipJsonSchema[None] = Field(default=None, title="Preferred Name")
    max_phase: float | SkipJsonSchema[None] = None
    max_phase_curated: str | SkipJsonSchema[None] = Field(alias="maxPhaseCurated", default=None, title="Max Phase Description")
    first_approval: int | SkipJsonSchema[None] = None
    chebi_par_id: str | SkipJsonSchema[None] = Field(alias="chebiParId", default=None, title="ChEBI Parent ID")
    oral: bool | SkipJsonSchema[None] = None
    parenteral: bool | SkipJsonSchema[None] = None
    withdrawn_flag: bool | SkipJsonSchema[None] = Field(alias="withdrawnFlag", default=None)
    withdrawn_reason: str | SkipJsonSchema[None] = Field(alias="withdrawnReason", default=None)
    black_box_warning: bool | SkipJsonSchema[None] = None
    smiles: str | SkipJsonSchema[None] = Field(default=None, title="SMILES")
    inchi: str | SkipJsonSchema[None] = Field(default=None, title="InChI")
    inchi_key: str | SkipJsonSchema[None] = Field(default=None, title="InChI Key")
    molecule_properties: MoleculeProperties | SkipJsonSchema[None] = None
    molecule_synonyms: list[MoleculeSynonym] | SkipJsonSchema[None] = None
    drug_indications: list[DrugIndication] | SkipJsonSchema[None] = None
    drug_mechanisms: list[DrugMechanism] | SkipJsonSchema[None] = None
    molecule_structures: MoleculeStructures | SkipJsonSchema[None] = None
    biotherapeutic: Biotherapeutic | SkipJsonSchema[None] = None
    xrefs: list[Xref] | SkipJsonSchema[None] = Field(default=None, title="Cross-references")
    bioactivities: list[Bioactivity] | SkipJsonSchema[None] = None

class EnrollmentInfo(CustomBaseModel):
    count: int | SkipJsonSchema[None] = Field(alias="enrollmentCount", default=None)
    type: str | SkipJsonSchema[None] = Field(alias="enrollmentType", default=None)

class IdentificationModule(CustomBaseModel):

    nct_id: str | SkipJsonSchema[None] = Field(default=None, title="NCT ID")
    nct_id_aliases: list[str] | SkipJsonSchema[None] = Field(default=None, title="NCT ID Aliases")
    brief_title: str | SkipJsonSchema[None] = Field(default=None, title="Brief Title")
    official_title: str | SkipJsonSchema[None] = Field(default=None, title="Official Title")

class ApiDate(CustomBaseModel):
    date: str | SkipJsonSchema[None] = None
    type: str | SkipJsonSchema[None] = None

class StatusModule(CustomBaseModel):

    overall_status: str | SkipJsonSchema[None] = Field(default=None, title="Overall Status")
    why_stopped: str | SkipJsonSchema[None] = Field(default=None, title="Why Stopped")
    start_date: ApiDate | SkipJsonSchema[None] = Field(default=None, title="Start Date")
    primary_completion_date: ApiDate | SkipJsonSchema[None] = Field(default=None, title="Primary Completion Date")
    study_first_submit_date: str | SkipJsonSchema[None] = Field(default=None)
    results_first_submit_date: str | SkipJsonSchema[None] = Field(default=None)

class ConditionsModule(CustomBaseModel):
    conditions: list[str] | SkipJsonSchema[None] = None

class DesignModule(CustomBaseModel):

    study_type: str | SkipJsonSchema[None] = None
    phase_list: list[str] | SkipJsonSchema[None] = None
    intervention_model: str | SkipJsonSchema[None] = None
    masking: str | SkipJsonSchema[None] = None
    primary_purpose: str | SkipJsonSchema[None] = None
    enrollment_info: EnrollmentInfo | SkipJsonSchema[None] = Field(alias="enrollmentInfo", default=None)

class Intervention(CustomBaseModel):
    intervention_name: str | SkipJsonSchema[None] = Field(alias="interventionName", default=None)
    intervention_type: str | SkipJsonSchema[None] = Field(alias="interventionType", default=None)

class ArmsInterventionsModule(CustomBaseModel):
    interventions: list[Intervention] | SkipJsonSchema[None] = None

class Outcome(CustomBaseModel):

    measure: str | SkipJsonSchema[None] = None
    time_frame: str | SkipJsonSchema[None] = None
    result_type: str | SkipJsonSchema[None] = None

class OutcomesModule(CustomBaseModel):

    primary_outcomes: list[Outcome] | SkipJsonSchema[None] = None
    secondary_outcomes: list[Outcome] | SkipJsonSchema[None] = None

class Location(CustomBaseModel):
    country: str | SkipJsonSchema[None] = None
    facility: str | SkipJsonSchema[None] = None

class OfficialContact(CustomBaseModel):
    contact_name: str | SkipJsonSchema[None] = None

class ContactsLocationsModule(CustomBaseModel):
    locations: list[Location] | SkipJsonSchema[None] = None
    official_contacts: list[OfficialContact] | SkipJsonSchema[None] = None

class LeadSponsor(CustomBaseModel):
    name: str | SkipJsonSchema[None] = None

class Collaborator(CustomBaseModel):
    name: str | SkipJsonSchema[None] = None

class SponsorsCollaboratorsModule(CustomBaseModel):
    lead_sponsor: LeadSponsor | SkipJsonSchema[None] = None
    collaborators: list[Collaborator] | SkipJsonSchema[None] = None

class OversightModule(CustomBaseModel):
    fda_regulated_drug: str | SkipJsonSchema[None] = None
    has_expanded_access: bool | SkipJsonSchema[None] = None
class ProtocolSection(CustomBaseModel):

    identification_module: IdentificationModule | SkipJsonSchema[None] = None
    status_module: StatusModule | SkipJsonSchema[None] = None
    design_module: DesignModule | SkipJsonSchema[None] = None
    conditions_module: ConditionsModule | SkipJsonSchema[None] = None
    arms_interventions_module: ArmsInterventionsModule | SkipJsonSchema[None] = None
    outcomes_module: OutcomesModule | SkipJsonSchema[None] = None
    contacts_locations_module: ContactsLocationsModule | SkipJsonSchema[None] = None
    sponsors_collaborators_module: SponsorsCollaboratorsModule | SkipJsonSchema[None] = None
    oversight_module: OversightModule | SkipJsonSchema[None] = None

class EventStat(CustomBaseModel):
    group_id: str | SkipJsonSchema[None] = Field(alias="groupId", default=None)
    num_affected: str | SkipJsonSchema[None] = Field(alias="numAffected", default=None)
    num_at_risk: str | SkipJsonSchema[None] = Field(alias="numAtRisk", default=None)

class AdverseEvent(CustomBaseModel):
    term: str | SkipJsonSchema[None] = None
    organ_system: str | SkipJsonSchema[None] = Field(alias="organSystem", default=None)
    source_vocabulary: str | SkipJsonSchema[None] = Field(alias="sourceVocabulary", default=None)
    assessment_type: str | SkipJsonSchema[None] = None
    stats: list[EventStat] | SkipJsonSchema[None] = None

class AdverseEventsModule(BaseModel):
    serious_events: list[AdverseEvent] | SkipJsonSchema[None] = Field(alias="seriousEvents", default=None)
    other_events: list[AdverseEvent] | SkipJsonSchema[None] = Field(alias="otherEvents", default=None)

class ResultsSection(CustomBaseModel):
    adverse_events_module: AdverseEventsModule | SkipJsonSchema[None] = Field(alias="adverseEventsModule", default=None)

class CtStudy(CustomBaseModel):
    protocol_section: ProtocolSection | SkipJsonSchema[None] = Field(alias="protocolSection", default=None)
    results_section: ResultsSection | SkipJsonSchema[None] = Field(alias="resultsSection", default=None)

class PharmgkbBlock(CustomBaseModel):

    generic_names: list[str] | SkipJsonSchema[None] = None


# ─── SmallMolecule root ───
class SmallMolecule(CustomBaseModel):

    name: str
    scope: Scope
    structure_image: str | SkipJsonSchema[None] = Field(alias="structureImage", default=None)
    lincs: Lincs | SkipJsonSchema[None] = Field(default=None, title="LINCS")
    unichem: UniChem | SkipJsonSchema[None] = Field(default=None, title="UniChem")
    chembl: Chembl | SkipJsonSchema[None] = Field(default=None, title="ChEMBL")
    pubchem: list[PubChem] | SkipJsonSchema[None] = Field(default=None, title="PubChem")
    clinicaltrials: list[CtStudy] | SkipJsonSchema[None] = Field(default=None, title="Clinical Trials")
    pharmgkb: PharmgkbBlock | SkipJsonSchema[None] = Field(default=None, title="PharmGKB")

    model_config = {"title": "Small Molecule Registry", "description": "Molecules with a low molecular weight (generally < 900 daltons) used to perturb the experimental system, often binding to specific biological targets.","json_schema_extra": {"version": "0.0.35"}}

if __name__ == "__main__":
    json_schema=SmallMolecule.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("json_schemas/registry/small_molecule/small_molecule.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)
