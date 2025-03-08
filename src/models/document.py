import logging
import os
import re
import time
from datetime import datetime
import xmlschema
from fastapi import HTTPException
from lxml import etree
from sqlalchemy import Integer, Column, String, DateTime, ForeignKey, Float, Enum, CheckConstraint, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, validates
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from schemas import DocumentCreateSchema
from .base import Base
from .mixin import GeneralMixin
from config import settings, logger
from helpers.db import EntityIdType, TradingCapacityType, BuySellIndicatorType


class DocumentModel(Base, GeneralMixin):
    __tablename__ = "document"

    reportingEntityId = Column(String, nullable=False, doc="reportingEntityID")
    reportingEntityIdType = Column(Enum(EntityIdType), nullable=False, doc="reportingEntityID type")
    recordSeqNumber = Column(Integer, nullable=False, doc="RecordSeqNumber")
    idOfMarketParticipant = Column(String, nullable=False, doc="idOfMarketParticipant")
    idOfMarketParticipantType = Column(Enum(EntityIdType), nullable=False, doc="idOfMarketParticipantType")
    otherMarketParticipant = Column(String, nullable=False, doc="otherMarketParticipant")
    otherMarketParticipantType = Column(Enum(EntityIdType), nullable=False, doc="otherMarketParticipant type")
    tradingCapacity = Column(Enum(TradingCapacityType), nullable=False, doc="tradingCapacity")
    buySellIndicator = Column(Enum(BuySellIndicatorType), nullable=False, doc="buySellIndicator")
    contractId = Column(String, nullable=False, doc="contractId")


    # contractDate = Column(Date, nullable=False, doc="contractDate")
    # contractType = Column(String, nullable=False, doc="contractType")
    # energyCommodity = Column(String, doc="energyCommodity")
    # priceFormula = Column(String, doc="priceFormula")
    # estimatedNotionalAmountValue = Column(Float, doc="estimatedNotionalAmount value")
    # estimatedNotionalAmountUnit = Column(String, doc="estimatedNotionalAmount unit")
    # volumeOptionality = Column(String, doc="volumeOptionality")
    # typeOfIndexPrice = Column(String, doc="typeOfIndexPrice")
    # fixingIndex = Column(String, doc="fixingIndex")
    # fixingIndexType = Column(String, doc="fixingIndexType")
    # fixingIndexSource = Column(String, doc="fixingIndexSource")
    # firstFixingDate = Column(Date, doc="firstFixingDate")
    # lastFixingDate = Column(Date, doc="lastFixingDate")
    # fixingFrequency = Column(String, doc="fixingFrequency")
    # settlementMethod = Column(String, doc="settlementMethod")
    # deliveryPointOrZone = Column(String, doc="deliveryPointOrZone")
    # deliveryStartDate = Column(Date, doc="deliveryStartDate")
    # deliveryEndDate = Column(Date, doc="deliveryEndDate")
    # loadType = Column(String, doc="loadType")
    # actionType = Column(String, doc="actionType")

    active = Column(Boolean, default=True, nullable=False, doc="Active/Deleted")
    xmlFileName = Column(String, nullable=True, doc="xmlFileName")


    xsd_file = "REMITTable2_V1-1.xsd"
    xsd_schema = xmlschema.XMLSchema(xsd_file)

    def generate_xml(self):
        namespaces = {
            'ait2': 'http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd'
        }

        root = etree.Element('{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}REMITTable2', nsmap=namespaces)

        reporting_entity = etree.SubElement(root, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}reportingEntityID")
        etree.SubElement(reporting_entity, f'{{{"http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd"}}}{self.reportingEntityIdType}').text = self.reportingEntityId

        trade_list = etree.SubElement(root, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}TradeList")

        report = etree.SubElement(trade_list, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}nonStandardContractReport")
        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}RecordSeqNumber").text = str(self.recordSeqNumber)

        market_participant = etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}idOfMarketParticipant")
        etree.SubElement(market_participant, f'{{{"http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd"}}}{self.idOfMarketParticipantType}').text = self.idOfMarketParticipant

        other_market_participant = etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}otherMarketParticipant")
        etree.SubElement(other_market_participant,f'{{{"http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd"}}}{self.otherMarketParticipantType}').text = self.otherMarketParticipant

        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}tradingCapacity").text = self.tradingCapacity
        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}buySellIndicator").text = self.buySellIndicator
        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}contractId").text = self.contractId
        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}contractDate").text = datetime.now().strftime("%Y-%m-%d")
        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}contractType").text = "FW"
        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}energyCommodity").text = "EL"

        price_formula = etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}priceOrPriceFormula")
        etree.SubElement(price_formula, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}priceFormula").text = "0,51*DEBY+0,22*DEPY"

        notional_amount = etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}estimatedNotionalAmount")
        etree.SubElement(notional_amount, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}value").text = "0"
        etree.SubElement(notional_amount, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}currency").text = "EUR"

        contract_quantity = etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}totalNotionalContractQuantity")
        etree.SubElement(contract_quantity, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}value").text = "0"
        etree.SubElement(contract_quantity, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}unit").text = "MWh"

        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}volumeOptionality").text = "V"
        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}typeOfIndexPrice").text = "I"

        fixing_index_details = etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}fixingIndexDetails")
        etree.SubElement(fixing_index_details, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}fixingIndex").text = "EEX DE Settlement"
        etree.SubElement(fixing_index_details, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}fixingIndexType").text = "FU"
        etree.SubElement(fixing_index_details, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}fixingIndexSource").text = "EEX"
        etree.SubElement(fixing_index_details, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}firstFixingDate").text = "2021-11-29"
        etree.SubElement(fixing_index_details, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}lastFixingDate").text = "2022-12-15"
        etree.SubElement(fixing_index_details, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}fixingFrequency").text = "O"

        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}settlementMethod").text = "P"
        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}deliveryPointOrZone").text = "10YDE-VE-------2"
        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}deliveryStartDate").text = "2022-01-01"
        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}deliveryEndDate").text = "2023-12-31"
        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}loadType").text = "SH"
        etree.SubElement(report, "{http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd}actionType").text = "N"

        full_path = os.path.join(settings.filestorage, self.xmlFileName)
        tree = etree.ElementTree(root)


        DocumentModel.xsd_schema.validate(tree)

        tree.write(full_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")




    @staticmethod
    async def create(db: AsyncSession, document_data: DocumentCreateSchema):

        def create_update_doc(document):
            for key, value in document_data_dict.items():
                if key == 'document_id':
                    continue

                setattr(document, key, value)

            now = datetime.now()
            document.xmlFileName=f'{now.strftime("%d_%m_%Y_%H_%M")}_REMITTable2_V1_1.xml'
            db.add(document)
            document.generate_xml()

        document_data_dict = document_data.model_dump()

        if "document_id" in document_data_dict and document_data_dict["document_id"]:
            document = await db.get(DocumentModel, int(document_data_dict["document_id"]))
            if document:
                create_update_doc(document)
            else:
                raise HTTPException(status_code=404, detail="Document not found for update")
        else:
            try:
                document = DocumentModel()
                create_update_doc(document)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {e}")
        try:
            await db.commit()
            await db.refresh(document)
            return document
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Duplicate record or integrity constraint failed.")


    @staticmethod
    async def delete(db: AsyncSession, document_id: int):
        document = await db.get(DocumentModel, int(document_id))
        if not document:
            raise HTTPException(status_code=404, detail="Document not found.")
        document.active = False
        await db.commit()
        return {"message": "Document archived successfully"}

    @staticmethod
    def update(db: Session, document_id: int, document_data: DocumentCreateSchema):
        document = db.get(DocumentModel, document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found.")

        for key, value in document_data.dict(exclude_unset=True).items():
            setattr(document, key, value)

        db.commit()
        db.refresh(document)
        return document

    @staticmethod
    async def get_list(db: AsyncSession, page: int = 1, limit: int = 10):
        query = select(DocumentModel).filter(DocumentModel.active == True).offset((page - 1) * limit).limit(limit)
        documents = await db.execute(query)
        documents = documents.scalars().all()
        return documents

    def _validate_ace(self, value):
        if len(value) != 12:
            logger.error(f"value be 12 characters long for 'ace' type,  value: {value}")
            raise ValueError("value be 12 characters long for 'ace' type")
        if not re.match(r"^[A-Za-z0-9_]+\.[A-Z][A-Z]$", value):
            logger.error(f"value pattern'[A-Za-z0-9_]+\\.[A-Z][A-Z]' for 'ace' type value: {value}")
            raise ValueError("value pattern'[A-Za-z0-9_]+\\.[A-Z][A-Z]' for 'ace' type")

    def _validate_bic(self, value):
        if len(value) != 11:
            logger.error(f"value be 11 characters long for 'BIC' type,  value: {value}")
            raise ValueError("value be 11 characters long for 'BIC' type")
        if not re.match(r"^[A-Za-z0-9_]+$", value):
            logger.error(f"value pattern '[A-Za-z0-9_]+' for 'BIC' type,  value: {value}")
            raise ValueError("value pattern '[A-Za-z0-9_]+' for 'BIC' type")

    def _validate_lei(self, value):
        if len(value) != 20:
            logger.error(f"value be 20 characters long for 'LEI' type,  value: {value}")
            raise ValueError("value be 20 characters long for 'LEI' type")
        if not re.match(r"^[A-Za-z0-9_]+$", value):
            logger.error(f"value pattern '[A-Za-z0-9_]+' for 'LEI' type,  value: {value}")
            raise ValueError("value pattern '[A-Za-z0-9_]+' for 'LEI' type")

    def _validate_eic(self, value):
        if len(value) != 16:
            logger.error(f"value be 16 characters long for 'EIC' type,  value: {value}")
            raise ValueError("value be 16 characters long for 'EIC' type")
        if not re.match(r"^[0-9][0-9][XYZTWV].+$", value):
            logger.error(f"value pattern '[0-9][0-9][XYZTWV].+' for 'EIC' type,  value: {value}")
            raise ValueError("value pattern '[0-9][0-9][XYZTWV].+' for 'EIC' type")

    def _validate_gln(self, value):
        if len(value) != 13:
            logger.error(f"value be 13 characters long for 'GLN' type,  value: {value}")
            raise ValueError("value be 13 characters long for 'GLN' type")
        if not re.match(r"^[A-Za-z0-9_]+$", value):
            logger.error(f"value pattern '[A-Za-z0-9_]+' for 'GLN' type,  value: {value}")
            raise ValueError("value pattern '[A-Za-z0-9_]+' for 'GLN' type")

    @validates("idOfMarketParticipant")
    def validate_id_of_market_participant(self, key, value):
        if self.idOfMarketParticipantType == EntityIdType.ace:
            self._validate_ace(value=value)
        elif self.idOfMarketParticipantType == EntityIdType.bic:
            self._validate_bic(value=value)
        elif self.idOfMarketParticipantType == EntityIdType.lei:
            self._validate_lei(value=value)
        elif self.idOfMarketParticipantType == EntityIdType.eic:
            self._validate_eic(value=value)
        elif self.idOfMarketParticipantType == EntityIdType.gln:
            self._validate_gln(value=value)

        return value

    @validates("reportingEntityId")
    def validate_reporting_entity_id(self, key, value):
        if self.reportingEntityIdType == EntityIdType.ace:
            self._validate_ace(value=value)
        elif self.reportingEntityIdType == EntityIdType.bic:
            self._validate_bic(value=value)
        elif self.reportingEntityIdType == EntityIdType.lei:
            self._validate_lei(value=value)
        elif self.reportingEntityIdType == EntityIdType.eic:
            self._validate_eic(value=value)
        elif self.reportingEntityIdType == EntityIdType.gln:
            self._validate_gln(value=value)

        return value

    @validates("otherMarketParticipant")
    def validate_reporting_entity_id(self, key, value):
        if self.otherMarketParticipantType == EntityIdType.ace:
            self._validate_ace(value=value)
        elif self.otherMarketParticipantType == EntityIdType.bic:
            self._validate_bic(value=value)
        elif self.otherMarketParticipantType == EntityIdType.lei:
            self._validate_lei(value=value)
        elif self.otherMarketParticipantType == EntityIdType.eic:
            self._validate_eic(value=value)
        elif self.otherMarketParticipantType == EntityIdType.gln:
            self._validate_gln(value=value)

        return value

    @validates("recordSeqNumber")
    def validate_record_seq_number(self, key, value):
        logger.error(f'VALIDATOR record seq {key, value, type(key), type(value)}')
        if value < 1:
            logger.error(f"recordSeqNumber must be >1,  value: {value}")
            raise ValueError("recordSeqNumber must be >1")

        return value

    @validates("contractId")
    def validate_contract_id(self, key, value):
        if len(value) > 100:
            logger.error(f"contractId must be <= 100 symbols,  value: {value}")
            raise ValueError("contractId must be <= 100 symbols")
        if not re.match(r"^[A-Za-z0-9_:-]+$", value):
            logger.error(f"contractId pattern '[A-Za-z0-9_:-]+',  value: {value}")
            raise ValueError("contractId pattern '[A-Za-z0-9_:-]+'")

        return value
