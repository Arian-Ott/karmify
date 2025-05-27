from pydantic import BaseModel, Field
import enum


class CCPReport(BaseModel):
    reportee: str = Field(..., description="The username of the user being reported")
    reporter: str = Field(..., description="The username of the user making the report")
    category_id: int = Field(..., description="The ID of the category being reported")
    comment: str = Field(..., description="The comment or reason for the report")


class CCPReportHTTP(BaseModel):
    reportee: str = Field(..., description="The username of the user being reported")
    category_id: int = Field(..., description="The ID of the category being reported")
    comment: str = Field(..., description="The comment or reason for the report")
