import re

from fastapi import Form
from pydantic import BaseModel, field_validator, model_validator
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

    @staticmethod
    def _validate_ace(value: str):
        if len(value) != 12:
            raise ValueError("ACE type must be 12 characters long.")
        if not re.match(r"^[A-Za-z0-9_]+\.[A-Z][A-Z]$", value):
            raise ValueError("ACE type must match pattern '[A-Za-z0-9_]+\\.[A-Z][A-Z]'")
        return value

    @staticmethod
    def _validate_bic(value: str):
        if len(value) != 11:
            raise ValueError("bic type must be 11 characters long.")
        if not re.match(r"^[A-Za-z0-9_]+$", value):
            raise ValueError("bic type must match pattern '[A-Za-z0-9_]+'")
        return value

    @staticmethod
    def _validate_lei(value: str):
        if len(value) != 20:
            raise ValueError("LEI type must be 20 characters long.")
        if not re.match(r"^[A-Za-z0-9_]+$", value):
            raise ValueError("LEI type must match pattern '[A-Za-z0-9_]+'")
        return value

    @staticmethod
    def _validate_eic(value: str):
        if len(value) != 16:
            raise ValueError("EIC type must be 16 characters long.")
        if not re.match(r"^[0-9][0-9][XYZTWV].+$", value):
            raise ValueError("EIC type must match pattern '[0-9][0-9][XYZTWV].+'")
        return value

    @staticmethod
    def _validate_gln(value: str):
        if len(value) != 13:
            raise ValueError("GLN type must be 13 characters long.")
        if not re.match(r"^[A-Za-z0-9_]+$", value):
            raise ValueError("GLN type must match pattern '[A-Za-z0-9_]+'")
        return value

    @model_validator(mode="before")
    def validate_entity_ids(cls, values):
        entity_id_fields = [
            ("idOfMarketParticipant", "idOfMarketParticipantType"),
            ("reportingEntityId", "reportingEntityIdType"),
            ("otherMarketParticipant", "otherMarketParticipantType"),
        ]

        for id_field, type_field in entity_id_fields:
            entity_id = values.get(id_field)
            entity_type = values.get(type_field)

            if entity_id and entity_type:
                if entity_type == EntityIdType.ace:
                    values[id_field] = cls._validate_ace(entity_id)
                elif entity_type == EntityIdType.bic:
                    values[id_field] = cls._validate_bic(entity_id)
                elif entity_type == EntityIdType.lei:
                    values[id_field] = cls._validate_lei(entity_id)
                elif entity_type == EntityIdType.eic:
                    values[id_field] = cls._validate_eic(entity_id)
                elif entity_type == EntityIdType.gln:
                    values[id_field] = cls._validate_gln(entity_id)

        return values

    @field_validator("recordSeqNumber")
    def validate_record_seq_number(cls, value):
        if value < 1:
            raise ValueError("recordSeqNumber must be greater than 0.")
        return value

    @field_validator("contractId")
    def validate_contract_id(cls, value):
        if len(value) > 100:
            raise ValueError("contractId must be at most 100 characters long.")
        if not re.match(r"^[A-Za-z0-9_:-]+$", value):
            raise ValueError("contractId must match pattern '[A-Za-z0-9_:-]+'")
        return value

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
