"""Mock data elements for DQ Rule Refinement Studio."""

MOCK_DATA_ELEMENTS = {
    "FRS Affiliate Code": {
        "cde_name": "FRS Affiliate Code",
        "cde_definition": (
            "The affiliate code provides a reference number using the FRS Business "
            "registry to identify Citigroup fully owned subsidiaries."
        ),
        "rule_title": "Rule_FRS_Affiliate_Code_Accuracy",
        "rule_dimension": "Accuracy",
        "business_text": (
            "Produce error if present and= '00000' when the Counterparty GFCID is not "
            "a Citigroup fully owned subsidiary."
        ),
    },
    "Standardized BCM Code": {
        "cde_name": "Standardized BCM Code (STD_BCM_CD)",
        "cde_definition": "Standardized BCM Code - 8 digit numerical value",
        "rule_title": "Rule_Standardized_BCM_Code_STD_BCM_CD_Accuracy",
        "rule_dimension": "Accuracy",
        "business_text": (
            "Produce error if the Standardized BCM Code does not match an 8-digit "
            "numerical format."
        ),
    },
    "Customer Address": {
        "cde_name": "Customer Address",
        "cde_definition": (
            "The current mailing address of the customer including street, city, "
            "state, and zip code."
        ),
        "rule_title": "Rule_Customer_Address_Completeness",
        "rule_dimension": "Completeness",
        "business_text": "Customer address must not be blank for all active customer records.",
    },
    "Trade Settlement Date": {
        "cde_name": "Trade Settlement Date",
        "cde_definition": (
            "The date on which a trade is expected to settle and ownership is transferred."
        ),
        "rule_title": "Rule_Trade_Settlement_Date_Timeliness",
        "rule_dimension": "Timeliness",
        "business_text": (
            "Produce error if Settlement Date is more than 3 business days after Trade Date "
            "for equity transactions."
        ),
    },
    "Counterparty GFCID": {
        "cde_name": "Counterparty GFCID",
        "cde_definition": "Global Financial Crime Identifier assigned to each counterparty entity.",
        "rule_title": "Rule_Counterparty_GFCID_Accuracy",
        "rule_dimension": "Accuracy",
        "business_text": (
            "Produce error if Counterparty GFCID is null or does not conform to the "
            "10-character alphanumeric GFCID format."
        ),
    },
}
