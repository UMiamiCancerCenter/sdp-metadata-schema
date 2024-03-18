from pydantic import BaseModel

class cellLine(BaseModel):
    cellLineName: str
    cellLineLabCanonicalID: str
    cellLineLabName: str
    cellLineLabBatchLabel: str
    cellLineProviderName: str
    cellLineProviderCatalogID: str
    cellLineProviderBatchID: str
    cellLineOrganism: str
    cellLineOrgan: str
    cellLineTissue: str
    cellLineCellType: str
    cellLineDonorSex: str
    cellLineDonorAge: float
    cellLineDonorEthnicity: str
    cellLineHealthStatus: str
    cellLineDisease: str
