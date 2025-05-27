import json
from typing import Any

from utils import (
    GenerateJsonSchemaWithoutDefaultTitles,
    delete_empty_default,
    to_title_case,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)
from pydantic.json_schema import SkipJsonSchema


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator="to_camel", populate_by_name=True, serialize_by_alias=True, field_title_generator=to_title_case)
class UniChem(CustomBaseModel):

    chebi:    str | list[str] | SkipJsonSchema[None] = Field(default=None, title="ChEBI")
    chembl:   str | list[str] | SkipJsonSchema[None] = Field(default=None, title="ChEMBL")
    lincs:    str | list[str] | SkipJsonSchema[None] = Field(default=None, title="LINCS")
    pubchem:  str | list[str] | SkipJsonSchema[None] = Field(default=None, title="PubChem")
    drugbank: str | list[str] | SkipJsonSchema[None] = Field(default=None, title="DrugBank")

    # normalise scalars + lists to str
    @field_validator("*", mode="before")
    @classmethod
    def _to_str(cls, v):
        if v is None:
            return None
        return [str(x) for x in v] if isinstance(v, list) else str(v)



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


class Lincs(CustomBaseModel):

    id: str | SkipJsonSchema[None] = Field(default=None, title="LINCS ID")
    name: str | SkipJsonSchema[None] = None
    alternative_names: list[str] | SkipJsonSchema[None] = Field(alias="alternativeNames", default=None)
    alternative_ids:  list[str] | SkipJsonSchema[None] = Field(alias="alternativeIds",  default=None)
    pubchem_cid: int  | SkipJsonSchema[None] = Field(alias="pubchemCid", default=None, title="PubChem CID")
    chebi_id: int | list[int] | SkipJsonSchema[None] = Field(alias="chebiId", default=None, title="ChEBI ID")
    inchi_parent: str | SkipJsonSchema[None] = Field(alias="inchiParent", default=None, title="InChI Parent")
    inchi_key_parent: str | SkipJsonSchema[None] = Field(alias="inchiKeyParent", default=None, title="InChI Key Parent")
    smiles_parent: str | SkipJsonSchema[None] = Field(alias="smilesParent", default=None, title="SMILES Parent")

    @field_validator("chebi_id", mode="before")
    @classmethod
    def unwrap_chebi(cls, v):
        return v[0] if isinstance(v, list) and len(v) == 1 else v

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
    indication_refs: IndicationRefs | list[IndicationRefs] | SkipJsonSchema[None] = Field(default=None, title="Indication References")
    max_phase_for_ind: float | SkipJsonSchema[None] = Field(default=None, title="Max Phase for Indication")
    mesh_heading: str | SkipJsonSchema[None] = Field(default=None, title="MeSH Heading")

    @field_validator("max_phase_for_ind", mode="before")
    @classmethod
    def _phase_to_float(cls, v):
        return float(v) if v is not None else None

    @field_validator("indication_refs", mode="before")
    @classmethod
    def _collapse_refs(cls, v):
        if not isinstance(v, list):
            return v
        out: dict[str, list[str]] = {}
        for item in v:
            key = item.get("ref_type")
            rid = item.get("ref_id")
            if key and rid:
                out.setdefault(key, []).append(rid)
        return out or None

class TargetComponent(CustomBaseModel):

    uniprot: list[str] | SkipJsonSchema[None] = Field(default=None, title="UniProt")

class DrugMechanism(CustomBaseModel):

    mechanism_of_action: str | SkipJsonSchema[None] = Field(alias="mechanismOfAction", default=None)
    action_type: str | SkipJsonSchema[None] = Field(alias="actionType", default=None)
    target_name: str | SkipJsonSchema[None] = Field(alias="targetName", default=None)
    target_organism: str | SkipJsonSchema[None] = Field(alias="targetOrganism", default=None)
    target_type: str | SkipJsonSchema[None] = Field(alias="targetType", default=None)
    target_components: list[TargetComponent] | SkipJsonSchema[None] = Field(alias="targetComponents", default=None)


class CompoundStructures(CustomBaseModel):

    standard_inchi_key: str | SkipJsonSchema[None] = Field(alias="standardInchiKey", default=None, title="Standard InChI Key")
    canonical_smiles: str | SkipJsonSchema[None] = Field(alias="canonicalSmiles", default=None)


class Biocomponent(CustomBaseModel):

    organism: str | SkipJsonSchema[None] = None


class Biotherapeutic(CustomBaseModel):

    biocomponents: list[Biocomponent] | SkipJsonSchema[None] = None


class MoleculeSynonym(CustomBaseModel):

    molecule_synonym: str | SkipJsonSchema[None] = None
    syn_type: str | SkipJsonSchema[None] = Field(default=None, title="Synonym Type")
    synonyms: str | list[str] | SkipJsonSchema[None] = None


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
    molecule_synonyms: MoleculeSynonym |list[MoleculeSynonym] | SkipJsonSchema[None] = None
    drug_indications: list[DrugIndication] | SkipJsonSchema[None] = None
    drug_mechanisms: list[DrugMechanism] | SkipJsonSchema[None] = None
    compound_structures: CompoundStructures | SkipJsonSchema[None] = None
    biotherapeutic: Biotherapeutic | SkipJsonSchema[None] = None
    # xrefs: dict[str, Any] | SkipJsonSchema[None] = Field(default=None, title="Cross References") - Failed to capture, double check request format and route

    @field_validator("chebi_par_id", mode="before")
    @classmethod
    def chebi_to_str(cls, v):
        return str(v) if v is not None else None

class IdentificationModule(CustomBaseModel):

    nct_id: str | SkipJsonSchema[None] = Field(default=None, title="NCT ID")
    nct_id_aliases: list[str] | SkipJsonSchema[None] = Field(default=None, title="NCT ID Aliases")
    brief_title: str | SkipJsonSchema[None] = Field(default=None, title="Brief Title")
    official_title: str | SkipJsonSchema[None] = Field(default=None, title="Official Title")

class StatusModule(CustomBaseModel):

    overall_status: str | SkipJsonSchema[None] = Field(default=None, title="Overall Status")
    why_stopped: str | SkipJsonSchema[None] = Field(default=None, title="Why Stopped")
    start_date: str | SkipJsonSchema[None] = Field(default=None, title="Start Date")
    primary_completion_date: str | SkipJsonSchema[None] = Field(default=None, title="Primary Completion Date")
    study_first_submit_date: str | SkipJsonSchema[None] = Field(default=None)
    results_first_submit_date: str | SkipJsonSchema[None] = Field(default=None)

class ConditionsModule(CustomBaseModel):
    conditions: list[str] | SkipJsonSchema[None] = None

class DesignModule(CustomBaseModel):

    study_type: str | SkipJsonSchema[None] = None
    phase_list: str | list[str] | SkipJsonSchema[None] = None
    intervention_model: str | SkipJsonSchema[None] = None
    masking: str | SkipJsonSchema[None] = None
    primary_purpose: str | SkipJsonSchema[None] = None

class PrimaryOutcome(CustomBaseModel):

    measure: str | SkipJsonSchema[None] = None
    time_frame: str | SkipJsonSchema[None] = None
    result_type: str | SkipJsonSchema[None] = None

class SecondaryOutcome(CustomBaseModel):

    measure: str | SkipJsonSchema[None] = None
class OutcomesModule(CustomBaseModel):

    primary_outcomes: list[PrimaryOutcome] | SkipJsonSchema[None] = None
    secondary_outcomes: list[SecondaryOutcome] | SkipJsonSchema[None] = None
class ProtocolSection(CustomBaseModel):

    identification_module: IdentificationModule | SkipJsonSchema[None] = Field(default=None, title="Identification Module")
    status_module: StatusModule | SkipJsonSchema[None] = Field(default=None, title="Status Module")
    conditions_module: ConditionsModule | SkipJsonSchema[None] = Field(default=None, title="Conditions Module")
    design_module: DesignModule | SkipJsonSchema[None] = Field(default=None, title="Design Module")
    outcomes_module: OutcomesModule | SkipJsonSchema[None] = Field(default=None, title="Outcomes Module")

class ClinicalTrial(CustomBaseModel):

    protocol_section: ProtocolSection | SkipJsonSchema[None] = Field(default=None, title="Protocol Section")

class DrugbankBlock(CustomBaseModel):

    cas_number: str | SkipJsonSchema[None] = Field(default=None, title="CAS Number")


class PharmgkbBlock(CustomBaseModel):

    generic_names: list[str] | SkipJsonSchema[None]


# ─── SmallMolecule root ───
class SmallMolecule(CustomBaseModel):

    name: str
    scope: str
    structure_image: str | SkipJsonSchema[None] = Field(alias="structureImage", default=None)
    lincs: Lincs | SkipJsonSchema[None] = Field(default=None, title="LINCS")
    unichem: UniChem | SkipJsonSchema[None] = Field(default=None, title="UniChem")
    chembl: Chembl | SkipJsonSchema[None] = Field(default=None, title="ChEMBL")
    pubchem: list[PubChem] | SkipJsonSchema[None] = Field(default=None, title="PubChem")
    clinicaltrials: list[ClinicalTrial] | SkipJsonSchema[None] = Field(default=None, title="Clinical Trials")
    drugbank: DrugbankBlock | SkipJsonSchema[None] = Field(default=None, title="DrugBank")
    pharmgkb: PharmgkbBlock | SkipJsonSchema[None] = Field(default=None, title="PharmGKB")

    @model_validator(mode="before")
    @classmethod
    def rename_id(cls, values: dict[str, Any]) -> dict[str, Any]:
        if "_id" in values:
            values["id"] = values.pop("_id")
        return values

if __name__ == "__main__":
    json_schema=SmallMolecule.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("json_schemas/registry/small_molecule/small_molecule.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)
