import json

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

class UniChem(BaseModel):
    chebi: str = Field(default="", title="ChEBI", description="ChEBI is a freely available ontology of molecular entities focused on 'small' chemical compounds")  
    chembl: str = Field(default="", title="ChEMBL", description="A database of bioactive drug-like small molecules and bioactivities abstracted from the scientific literature.") 
    lincs: str = Field(default="", title="LINCS", description="The LINCS DCIC facilitates and standardizes the information relevant to LINCS assays as described in http://www.lincsproject.org/data/data-standards/")
    # mcule: str = Field(default="", title="Mcule", description="An online drug discovery platform with virtual screening and molecular modelling services.")
    # molport: str = Field(default="", title="MolPort", description="MolPort. A database designed to assist users find commercial sources of compounds. Access requires (free) registration. Only stock compounds included from Nov 2017.")
    pubchem: str = Field(default="", title="PubChem", description="A database of normalized PubChem compounds (CIDs) from the PubChem Database.")
    drugbank: str = Field(default="", title="DrugBank", description="A database that combines drug (i.e. chemical, pharmacological and pharmaceutical) data with drug target (i.e. sequence, structure, and pathway) information.")
    # pdb: str = Field(default="", title="PDBe", description="The European resource for the collection, organisation and dissemination of data on biological macromolecular structures, including structures of small molecule ligands for proteins.")
    # gtopdb: str = Field(default="", title="Guide to Pharmacology", description="The IUPHAR (International Union of Basic and Clinical Pharmacology)/BPS (British Pharmacological Society) Guide to PHARMACOLOGY database contains structures of small molecule ligands, peptides and antibodies, with their affinities at protein targets.")
    # pubchem_dotf: str = Field(default="", title="PubChem: Drugs of the Future", description="A subset of the PubChem DB: from the original depositor 'drugs of the future' (Prous).")
    # kegg_ligand: str = Field(default="", title="KEGG Ligand", description="KEGG LIGAND is a composite DB consisting of COMPOUND, GLYCAN, REACTION, RPAIR, RCLASS, and ENZYME DBs, whose entries are identified by C, G, R, RP, RC, and EC numbers, respectively.")
    # nih_ncc: str = Field(default="", title="NIH Clinical Collection", description="Collections of plated arrays of small molecules that have a history of use in human clinical trials. Assembled by the National Institutes of Health (NIH) through the Molecular Libraries Roadmap Initiative")
    # zinc: str = Field(default="", title="ZINC", description="A free database of commercially-available compounds for virtual screening, provided by the Shoichet Laboratory in the Department of Pharmaceutical Chemistry at the University of California, San Francisco (UCSF).  [Irwin and Shoichet, J. Chem. Inf. Model. 2005;45(1):177-82]")
    # emolecules: str = Field(default="", title="eMolecules", description="A free chemical structure search engine containing millions of public domain structures. Pricing, availabilities, and vendor information requires an eMolecules Plus subscription.")
    # atlas: str = Field(default="", title="Atlas", description="The Gene Expression Atlas is a semantically enriched database of meta-analysis based summary statistics over a curated subset of ArrayExpress Archive, servicing queries for condition-specific gene expression patterns as well as broader exploratory searches for biologically interesting genes/samples.")
    # fdasrs: str = Field(default="", title="FDA SRS", description="The primary goal of the FDA/USP Substance Registration System (SRS) is to unambiguously define all substances present in regulated products. Once a substance has been defined, the SRS assigns a strong identifier that is permanently associated with the substance: a UNII (Unique Ingredient Identifier). This is a a non-proprietary, free, unique, unambiguous, nonsemantic, alphanumeric identifier based on a substances molecular structure and/or descriptive information.")
    # surechembl: str = Field(default="", title="SureChEMBL", description="SureChEMBL automatically extracts chemistry from the full text of all major patent authorities. Compounds are derived from either chemical names found in text or in chemical depictions. All SureChEMBL compounds are included, except those failing UniChem loading rules.")
    # pharmgkb: str = Field(default="", title="PharmGKB", description="PharmGKB (Pharmacogenomics Knowledgebase) is a comprehensive resource that curates knowledge about the impact of genetic variation on drug response for clinicians and researchers.")
    # hmdb: str = Field(default="", title="Human Metabolome Database", description="The Human Metabolome Database (HMDB) is a freely available electronic database containing detailed information about small molecule metabolites found in the human body. It is intended to be used for applications in metabolomics, clinical chemistry, biomarker discovery and general education. The database is designed to contain or link three kinds of data: 1) chemical data, 2) clinical data, and 3) molecular biology/biochemistry data")
    # selleck: str = Field(default="", title="Selleck", description="Selleck Chemicals is a supplier of biochemical products, including over 1,000 inhibitor products")
    # pubchem_tpharma: str = Field(default="", title="PubChem: Thomson Pharma", description="A subset of the PubChem DB: from the original depositor 'Thomson Pharma'.")
    # nmrshiftdb2: str = Field(default="", title="NMRShiftDB", description="An NMR database (web database) for organic structures and their nuclear magnetic resonance (nmr) spectra. It allows for spectrum prediction (13C, 1H and other nuclei) as well as for searching spectra, structures and other properties. Last not least, it features peer-reviewed submission of datasets by its users.")
    # actor: str = Field(default="", title="ACToR", description="ACToR (Aggregated Computational Toxicology Resource)")
    # recon: str = Field(default="", title="Recon", description="A biochemical knowledge-base on human metabolism")
    # nikkaji: str = Field(default="", title="Nikkaji", description="Nakkaji (The Japan Chemical Substance Dictionary) is an organic compound dictionary database prepared by the Japan Science and Technology Agency (JST).")
    # bindingdb: str = Field(default="", title="BindingDB", description="A public, web-accessible database of measured binding affinities, focusing chiefly on the interactions of proteins considered to be drug-targets with small, drug-like molecules")
    # comptox: str = Field(default="", title="EPA CompTox Dashboard", description="The foundation of chemical safety testing relies on chemistry information such as high-quality chemical structures and physicochemical properties. This information is used by scientists to predict the potential health risks of chemicals.The CompTox Dashboard is part of a suite of dashboards developed by EPA to help evaluate the safety of chemicals. It provides access to a variety of data and information on over 700,000 chemicals currently in use and of interest to environmental researchers. Within the CompTox Dashboard, users can access chemical structures, experimental and predicted physicochemical and toxicity data, and additional links to relevant websites and applications. It maps curated physicochemical property data associated with chemical substances to their corresponding chemical structures")
    # lipidmaps: str = Field(default="", title="LipidMaps", description="LIPID Metabolites And Pathways Strategy (LIPID MAPS) is a multi-institutional effort created to identify and quantitate, using a systems biology approach and sophisticated mass spectrometers, all of the major, and many minor, lipid species in mammalian cells, as well as to quantitate the changes in these species in response to perturbation")
    # drugcentral: str = Field(default="", title="DrugCentral", description="DrugCentral is an online drug information resource created and maintained by Division of Translational Informatics at University of New Mexico, providing information on active ingredients chemical entities, pharmaceutical products, drug mode of action, indications, pharmacologic action")
    # carotenoiddb: str = Field(default="", title="CarotenoidDB", description="A Database of information on naturally occurring carotenoids from many organisms, extracted  from the literature.")
    # metabolights: str = Field (default="", title="Metabolights", description="A database for Metabolomics experiments and derived information. The database is cross-species, cross-technique and covers metabolite structures and their reference spectra as well as their biological roles, locations and concentrations, and experimental data from metabolic experiments.")
    # brenda: str = Field(default="", title="Brenda", description="A comprehensive Enzyme Information system containing enzyme functional data extracted directly from the primary literature.")
    # rhea: str = Field(default="", title="Rhea", description="An expert curated resource of biochemical reactions designed for the annotation of enzymes and genome-scale metabolic networks and models")
    # chemicalbook: str = Field(default="", title="ChemicalBook", description="An online knowledge-base of chemicals and a platform of the Chinese domestic vendors in chemical industry")
    # swisslipids: str = Field(default="", title="SwissLipids", description="SwissLipids is an expert curated resource that provides a framework for the integration of lipid and lipidomic data with biological knowledge and models")
    # dailymed: str = Field(default="", title="DailyMed", description="A database of marketed drugs in the USA, containing label and package insert information")
    # clinicaltrials: str = Field(default="", title="ClinicalTrials", description="Intervention names from ClinicalTrials.gov. A database of privately and publicly funded clinical studies conducted around the world")

class Content(BaseModel):
    name: str = Field(default="", title="Name")
    alternativeNames: list[str] = Field(default="", title="Alternative Names")
    alternativeIds: list[str] = Field(default="", title="Alternative IDs")
    pubchemCid: str = Field(default="", title="PubChem CID")
    chebiId: str = Field(default="", title="ChEBI ID")
    inchiCanonical: str = Field(default="", title="Canonical InChI", description="InChi representation of standardized chemical structure")
    smilesCanonical: str = Field(default="", title="Canonical SMILES", description="Canonical SMILES representation of standardized chemical structure")
class Lincs(BaseModel):
    id: str = Field(default="", title="LINCS ID")
    name: str = Field(default="", title="Name")
    alternativeNames: list[str] = Field(default="", title="Alternative Names")
    alternativeIds: list[str] = Field(default="", title="Alternative IDs")
    pubchemCid: str = Field(default="", title="PubChem CID")
    chebiId: str = Field(default="", title="ChEBI ID")
    inchiParent: str = Field(default="", title="Parent InChI")
    smilesParent: str = Field(default="", title="Parent SMILES")

# class AeolusIndication(BaseModel):
#     count: int = Field(default="", title="Count")
#     id: str = Field(default="", title="ID")
#     meddra_code: str = Field(default="", title="medDRA Code")
#     name: str = Field(default="", title="Name")

# class AeolusOutcome(BaseModel):
#     case_count: int = Field(default="", title="Case Count")
#     id: str = Field(default="", title="ID")
#     meddra_code: str = Field(default="", title="medDRA Code")
#     name: str = Field(default="", title="Name")
#     prr: float = Field(default="", title="Proportional Reporting Ratio")
#     prr_95_ci: list[float] = Field(default="", title="PRR 95% Confidence Interval")
#     ror: float = Field(default="", title="Reporting Odds Ratio")
#     ror_95_ci: list[float] = Field(default="", title="ROR 95% Confidence Interval")

# class Aeolus(BaseModel):
#     drug_id: str = Field(default="", title="Drug ID")
#     drug_name: str = Field(default="", title="Drug Name")
#     inchikey: str = Field(default="", title="InChI Key")
#     indicatons: list[AeolusIndication] = Field(default="", title="Indications")
#     no_of_outcomes: int = Field(default="", title="Number of Outcomes")
#     outcomes: list[AeolusOutcome] = Field(default="", title="Outcomes")
#     pt: str = Field(default="", title="Preferred Term")
#     rxcui: str = Field(default="", title="RxCUI", description="RxNorm Concept Unique Identifier")
#     unii: str = Field(default="", title="UNII", description="Unique Ingredient Identifier")

# class Chebi(BaseModel):
#     id: str = Field(default="", title="ID")
#     secondary_chebi_id: list[str] = Field(default="", title="Secondary ChEBI IDs")
#     name: str = Field(default="", title="Name")
#     formulae: str = Field(default="", title="Chemical Formula")
#     definition: str = Field(default="", title="Definition")
#     brand_names: list[str] = Field(default="", title="Brand Names")
#     inchi: str = Field(default="", title="InChI")
#     inchikey: str = Field(default="", title="InChI Key")
#     inn: str = Field(default="", title="INN", description="International Nonproprietary Name")
#     iupac: str = Field(default="", title="IUPAC Name")
#     smiles: str = Field(default="", title="SMILES")
#     synonyms: list[str] = Field(default="", title="Synonyms")  

class Efo(BaseModel):
    # id: str = Field(default="", title="ID")
    term: str = Field(default="", title="Term")

# class IndicationRefs(BaseModel):
#     ATC: str = Field(default="")
#     ClinicalTrials: str = Field(default="")
#     DailyMed: str = Field(default="")
#     FDA: str = Field(default="")
#     id: str = Field(default="", title="ID")
#     type: str = Field(default="", title="Type")
#     url: str = Field(default="", title="URL")

class ChemblDrugIndication(BaseModel):
    efo: list[Efo] = Field(default="", title="EFO", description="Experimental Factor Ontology")
    # first_approval: int = Field(default="", title="First Approval")
    # indicaton_refs: list[IndicationRefs] = Field(default="", title="Indication References")
    # max_phase_for_ind: str = Field(default="", title="Maximum Phase for Indication")
    # mesh_heading: str = Field(default="", title="MeSH Heading")
    # mesh_id: str = Field(default="", title="MeSH ID")

# class ChemblMechanismRefs(BaseModel):
#     ClinicalTrials: str = Field(default="")
#     DOI: str = Field(default="")
#     DailyMed: str = Field(default="")
#     Expert: str = Field(default="")
#     FDA: str = Field(default="")
#     ISBN: str = Field(default="")
#     IUPHAR: str = Field(default="")
#     InterPro: str = Field(default="")
#     KEGG: str = Field(default="")
#     Other: str = Field(default="")
#     PMC: str = Field(default="")
#     Patent: str = Field(default="")
#     PubChem: str = Field(default="")
#     PubMed: str = Field(default="")
#     UniProt: str = Field(default="")
#     Wikipedia: str = Field(default="")
#     id: str = Field(default="", title="ID")
#     type: str = Field(default="", title="Type")
#     url: str = Field(default="", title="URL")

class ChemblTargetComponent(BaseModel):
    # ensembl_gene: list[str] = Field(default="", title="Ensembl Genes")
    uniprot: list[str] = Field(default="", title="UniProt")

class ChemblDrugMechanism(BaseModel):
    actionType: str = Field(default="", title="Action Type")
    # mechanism_refs: list[ChemblMechanismRefs] = Field(default="", title="Mechanism References")
    # target_chembl_id: str = Field(default="", title="Target ChEMBL ID")
    targetComponents: list[ChemblTargetComponent] = Field(default="", title="Target Components")
    targetName: str = Field(default="", title="Target Name")
    # target_organism: str = Field(default="", title="Target Organism")
    # target_type: str = Field(default="", title="Target Type")

class ChemblMoleculeSynonym(BaseModel):
    moleculeSynonym: str = Field(default="", title="Molecule Synonym")
    synType: str = Field(default="", title="Synonym Type")
    # synonyms: str = Field(default="", title="Synonyms")

class Chembl(BaseModel):
    drugIndications: list[ChemblDrugIndication] = Field(default="", title="Drug Indications")
    # binding_site_name: str = Field(default="", title="Binding Site Name")
    drugMechanisms: list[ChemblDrugMechanism] = Field(default="", title="Drug Mechanisms")
    # first_approval: int = Field(default="", title="First Approval")
    # first_in_class: int = Field(default="", title="First in Class")
    # helm_notation: str = Field(default="", title="Helm Notation")
    # inchi: str = Field(default="", title="InChI")
    # inchi_key: str = Field(default="", title="InChI Key")
    # indication_class: list[str] = Field(default="", title="Indication Class(es)")
    # inorganic_flag: int = Field(default="", title="Inorganic Flag")
    maxPhase: float = Field(default="", title="Maximum Phase", description="Maximum phase of development reached for the compound (4 = approved). Null where max phase has not yet been assigned.")
    # molecule_chembl_id: str = Field(default="", title="Molecule ChEMBL ID")
    moleculeSynonyms: list[ChemblMoleculeSynonym] = Field(default="", title="Molecule Synonyms")
    moleculeType: str = Field(default="", title="Molecule Type")
    # natural_product: int = Field(default="", title="Natural Product", description="Indicates whether the compound is natural product-derived (currently curated only for drugs)")
    # oral: bool = Field(default="", title="Oral", description="Indicates whether the drug is known to be administered orally.")
    # orphan: int = Field(default="", title="Orphan", description="Indicates orphan designation, i.e. intended for use against a rare condition (1 = yes, 0 = no, -1 = preclinical compound ie not a drug)")
    # parenteral: bool = Field(default="", title="Parenteral", description="Indicates whether the drug is known to be administered parenterally")
    # polymer_flag: bool = Field(default="", title="Polymer Flag", description="Indicates whether a molecule is a small molecule polymer (e.g., polistyrex)")
    # pref_name: str = Field(default="", title="Preferred Name")
    # prodrug: str = Field(default="", title="Prodrug", description="Indicates that the molecule is a pro-drug (see molecule hierarchy for active component, where known)")
    # smiles: str = Field(default="", title="SMILES")
    # structure_type: str = Field(default="", title="Structure Type", description="Indications whether the molecule has a small molecule structure or a protein sequence (MOL indicates an entry in the compound_structures table, SEQ indications an entry in the protein_therapeutics table, NONE indicates an entry in neither table, e.g., structure unknown)")
    # therapeutic_flag: bool = Field(default="", title="Therapeutic Flag", description="Indicates that a drug has a therapeutic application (as opposed to e.g., an imaging agent, additive etc).")
    # topical: bool = Field(default="", title="Topical", description="Indicates whether the drug is known to be administered topically.")
    # usan_stem: str = Field(default="", title="USAN Stem", description="Where the compound has been assigned a USAN name, this indicates the stem, as described in the USAN_STEM table.")
    # usan_stem_definition: str = Field(default="", title="USAN Stem Definition", description="Definition of the USAN stem")
    # usan_substem: str = Field(default="", title="USAN Substem", description="Where the compound has been assigned a USAN name, this indicates the substem")
    # usan_year: int = Field(default="", title="USAN Year", description="The year in which the application for a USAN/INN name was made")

# class DrugBank(BaseModel):
#     accession_number: list[str] = Field(default="", title="Accession Number")
#     cas: str = Field(default="", title="CAS", description="Chemical Abstracts Service (CAS) registry number") 
#     id: str = Field(default="", title="ID")
#     inchi_key: str = Field(default="", title="InChI Key")
#     name: str = Field(default="", title="name")
#     synonyms: list[str] = Field(default="", title="Synonyms")
#     unii: str = Field(default="", title="UNII", description="Unique Ingredient Identifier")

# class DrugCentralApproval(BaseModel):
#     agency: str = Field(default="", title="Agency")
#     company: str = Field(default="", title="Company")
#     date: str = Field(default="", title="Date")
#     orphan: str = Field(default="", title="Orphan")

# class DrugCentralUniProt(BaseModel):
#     gene_symbol: str = Field(default="", title="Gene Symbol")
#     swissprot_entry: str = Field(default="", title="Swiss-Prot Entry")
#     uniprot_id: str = Field(default="", title="UniProt ID")

# class DrugCentralBioactivity(BaseModel):
#     act_source: str = Field(default="", title="Bioactivity Source")
#     act_type: str = Field(default="", title="Bioactivity Type")
#     act_value: float = Field(default="", title="Bioactivity Value")
#     action_type: str = Field(default="", title="Action Type")
#     moa: float = Field(default="", title="Mechanism of Action")
#     moa_source: str = Field(default="", title="Mechanism of Action Source")
#     organism: str = Field(default="", title="Organism")
#     target_class: str = Field(default="", title="Target Class")
#     target_name: str = Field(default="", title="Target Name")
#     uniprot: list[DrugCentralUniProt] = Field(default="", title="UniProt")

# class DrugCentralDrugDosage(BaseModel):
#     dosage: float = Field(default="", title="Dosage")
#     route: str = Field(default="", title="Route")
#     unit: str = Field(default="", title="Unit")

# class DrugCentralIndication(BaseModel):
#     concept_name: str = Field(default="", title="Concept Name")
#     cui_semantic_type: str = Field(default="", title="CUI Semantic Type")
#     snomed_concept_id: int = Field(default="", title="SNOMED Concept ID")
#     snomed_full_name: str = Field(default="", title="SNOMED Full Name")
#     umls_cui: str = Field(default="", title="UMLS CUI")

# class DrugCentralDrugUse(BaseModel):
#     contraindication: list[DrugCentralIndication] = Field(default="", title="Contraindications")
#     diagnosis: list[DrugCentralIndication] = Field(default="", title="Diagnoses")
#     indication: list[DrugCentralIndication] = Field(default="", title="Indications")
#     off_label_use: list[DrugCentralIndication] = Field(default="", title="Off Label Uses")
#     reduce_risk: list[DrugCentralIndication] = Field(default="", title="Reduced Risks")
#     symptomatic_treatment: list[DrugCentralIndication] = Field(default="", title="Symptomatic Treatments")

# class DrugCentralFdaAdverseEvent(BaseModel):
#     drug_ae: int = Field(default="", title="Patients Taking Drug Having Adverse Event")
#     drug_no_ae: int = Field(default="", title="Patients Taking Drug Not Having Adverse Event")
#     level: str = Field(default="", title="Level")
#     llr: float = Field(default="", title="Likelihood Ratio")
#     llr_threshold: float = Field(default="", title="Likelihood Ratio Threshold")
#     meddra_code: int = Field(default="", title="medDRA Code")
#     meddra_term: str = Field(default="", title="medDRA Term")
#     no_drug_ae: int = Field(default="", title="Patients Not Taking Drug Having Adverse Event")
#     no_drug_no_ar: int = Field(default="", title="Patients Not Taking Drug Not Having Adverse Event")

# class DrugCentralPharmClassSpecs(BaseModel):
#     code: str = Field(default="", title="Code")
#     description: str = Field(default="", title="Description")

# class DrugCentralPharmClass(BaseModel):
#     chebi: list[DrugCentralPharmClassSpecs] = Field(default="", title="ChEBI")
#     # fda_chemical/ingredient: list[DrugCentralPharmClassSpecs] = Field(default="", title="FDA Chemical/Ingredient")  # noqa: E999
#     fda_cs: list[DrugCentralPharmClassSpecs] = Field(default="", title="FDA CS")
#     fda_epc: list[DrugCentralPharmClassSpecs] = Field(default="", title="FDA EPC")
#     fda_ext: list[DrugCentralPharmClassSpecs] = Field(default="", title="FDA EXT")
#     fda_moa: list[DrugCentralPharmClassSpecs] = Field(default="", title="FDA MoA")
#     fda_pe: list[DrugCentralPharmClassSpecs] = Field(default="", title="FDA PE")
#     mesh_pa: list[DrugCentralPharmClassSpecs] = Field(default="", title="MeSH PA")

# class DrugCentralStructure(BaseModel):
#     cas_rn: str = Field(default="", title="CAS RN", description="Chemical Abstracts Service (CAS) registry number")
#     inchi: str = Field(default="", title="InChI")
#     inchikey: str = Field(default="", title="InChI Key")
#     inn: str = Field(default="", title="INN", description="International Nonproprietary Name")
#     smiles: str = Field(default="", title="SMILES")

# class DrugCentral(BaseModel):
#     approval: list[DrugCentralApproval] = Field(default="", title="Approvals")
#     bioactivity: list[DrugCentralBioactivity] = Field(default="", title="Bioactivities")
#     drug_dosage: list[DrugCentralDrugDosage] = Field(default="", title="Drug Dosages")
#     drug_use: DrugCentralDrugUse = Field(default="", title="Drug Use")
#     fda_adverse_event: list[DrugCentralFdaAdverseEvent] = Field(default="", title="FDA Adverse Events")
#     pharmacology_class: DrugCentralPharmClass = Field(default="", title="Pharmacology Class")
#     structures: DrugCentralStructure = Field(default="", title="Structures")
#     synonyms: list[str] = Field(default="", title="Synonyms")

# class PharmGKB(BaseModel):
#     id: str = Field(default="", title="ID")
#     name: str = Field(default="", title="Name")
#     inchi: str = Field(default="", title="InChI")
#     smiles: str = Field(default="", title="SMILES")
#     generic_names: list[str] = Field(default="", title="Generic Names")
#     trade_names: list[str] = Field(default="", title="Trade Names")
#     type: str = Field(default="", title="Type")

class PubChemIupac(BaseModel):
    # allowed: str = Field(default="", title="Allowed")
    # cas_like_style: str = Field(default="", title="CAS-like Style")
    # markup: str = Field(default="", title="Markup")
    # preferred: str = Field(default="", title="Preferred")
    systematic: str = Field(default="", title="Systematic")
    # traditional: str = Field(default="", title="Traditional")

class PubChemSmiles(BaseModel):
    canonical: str = Field(default="", title="Canonical")
    # isomeric: str = Field(default="", title="Isomeric")

class PubChem(BaseModel):
    cid: str = Field(default="", title="CID")
    inchi: str = Field(default="", title="InChI")
    # inchikey: str = Field(default="", title="InChI Key")  
    iupac: PubChemIupac = Field(default="", title="IUPAC", json_schema_extra={"type": "object"})
    molecularFormula: str = Field(default="", title="Molecular Formula")
    smiles: PubChemSmiles = Field(default="", title="SMILES", json_schema_extra={"type": "object"})
 
class SmallMolecule(BaseModel):
    model_config = ConfigDict(title="Small Molecule")

    name: str = Field(title="Name")
    content: Content = Field(default="", title="User-submitted Content", json_schema_extra={"type": "object"})
    unichem: UniChem = Field(default="", title="UniChem Cross References", json_schema_extra={"type": "object"})
    lincs: Lincs = Field(default="", title="LINCS Metadata", json_schema_extra={"type": "object"})
    # aeolus: Aeolus = Field(default="", title="AEOLUS", description="Adverse Event Open Learning through Universal Standardization", json_schema_extra={"type": "object"})
    # chebi: Chebi = Field(default="", title="ChEBI", description="Chemical Entities of Biological Interest", json_schema_extra={"type": "object"})
    chembl: Chembl = Field(default="", title="ChEMBL", json_schema_extra={"type": "object"})
    # drugbank: DrugBank = Field(default="", Title="DrugBank", json_schema_extra={"type": "object"})
    # drugcentral: DrugCentral = Field(default="", title="DrugCentral", json_schema_extra={"type": "object"})
    # pharmgkb: PharmGKB = Field(default="", title="PharmGKB", json_schema_extra={"type": "object"})
    pubchem: PubChem = Field(default="", title="PubChem", json_schema_extra={"type": "object"})

if __name__ == "__main__":
    json_schema=SmallMolecule.model_json_schema(schema_generator=GenerateJsonSchemaWithoutDefaultTitles)
    delete_empty_default(json_schema)
    with open ("small_molecule_registry.json", "w") as ft:
        print(json.dumps(json_schema, indent=2), file = ft)