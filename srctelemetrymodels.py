from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum

class TelemetryType(str, Enum):
    EMOTIONAL = "emotional"
    VITAL = "vital"
    STRATEGIC = "strategic"
    COGNITIVE = "cognitive"

class ChaosCertification(str, Enum):
    ADVERSARIAL_VALIDATED = "adversarial_validated"
    PARTIALLY_CERTIFIED = "partially_certified"
    UNCERTIFIED = "uncertified"

class FragmentationTelemetry(BaseModel):
    """Core telemetry data model with cryptographic proof"""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    telemetry_id: str = Field(..., description="Unique identifier for this telemetry packet")
    telemetry_type: TelemetryType
    data: Dict[str, Any] = Field(..., description="Actual telemetry payload")
    
    # Cryptographic proof
    signature: str = Field(..., description="ECDSA signature of telemetry hash")
    public_key: str = Field(..., description="Public key for verification")
    origin_hash: str = Field(..., description="SHA-256 hash of original data")
    
    # Chaos certification
    chaos_certification: ChaosCertification = Field(default=ChaosCertification.UNCERTIFIED)
    chaos_score: float = Field(default=0.0, ge=0.0, le=1.0)
    certification_timestamp: Optional[datetime] = None
    
    # Metadata
    version: str = Field(default="1.0.0")
    auction_id: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }