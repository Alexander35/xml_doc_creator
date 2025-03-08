from fastapi import Form
from pydantic import BaseModel
from typing_extensions import Optional
from helpers.db import EntityIdType, TradingCapacityType, BuySellIndicatorType


class DocumentCreateSchema(BaseModel):
    document_id: Optional[int] = None
    reportingEntityId: str
    reportingEntityIdType: EntityIdType
    recordSeqNumber: int
    idOfMarketParticipant: str
    idOfMarketParticipantType: EntityIdType
    otherMarketParticipant: str
    otherMarketParticipantType: EntityIdType
    tradingCapacity: TradingCapacityType
    buySellIndicator: BuySellIndicatorType
    contractId: str

    class Config:
        use_enum_values = True
        str_strip_whitespace = True

    @classmethod
    def as_form(
            cls,
            reportingEntityId: str = Form(...),
            reportingEntityIdType: EntityIdType = Form(...),
            recordSeqNumber: int = Form(...),
            idOfMarketParticipant: str = Form(...),
            idOfMarketParticipantType: EntityIdType = Form(...),
            otherMarketParticipant: str = Form(...),
            otherMarketParticipantType: EntityIdType = Form(...),
            tradingCapacity: TradingCapacityType = Form(...),
            buySellIndicator: BuySellIndicatorType = Form(...),
            contractId: str = Form(...),
            document_id: Optional[int] = Form(None),
    ):
        return cls(
            reportingEntityId=reportingEntityId,
            reportingEntityIdType=reportingEntityIdType,
            recordSeqNumber=recordSeqNumber,
            idOfMarketParticipant=idOfMarketParticipant,
            idOfMarketParticipantType=idOfMarketParticipantType,
            otherMarketParticipant=otherMarketParticipant,
            otherMarketParticipantType=otherMarketParticipantType,
            tradingCapacity=tradingCapacity,
            buySellIndicator=buySellIndicator,
            contractId=contractId,
            document_id=document_id,
        )
