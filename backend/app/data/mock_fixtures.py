"""
Realistic mock datasets for Deals and Work Orders boards.
Contains realistic messy data (inconsistent sector names, dirty dates, missing values,
varied capitalization, etc.) to power Demo Mode when Monday credentials are not supplied.
"""

MOCK_DEALS_RAW = [
    {
        "id": "D101",
        "name": "NTPC Solar Thermal Survey - Phase 2",
        "sector": "Energy",
        "deal_size": "₹2,50,00,000",
        "stage": "Closed Won",
        "expected_close_date": "2026-01-15"
    },
    {
        "id": "D102",
        "name": "Adani Green Wind Farm Mapping",
        "sector": " ENERGY ",
        "deal_size": "₹1.8 Cr",
        "stage": "Proposal Sent",
        "expected_close_date": "10/03/2026"
    },
    {
        "id": "D103",
        "name": "NHAI Delhi-Mumbai Expressway Corridor Flight",
        "sector": "infra",
        "deal_size": "₹3,20,00,000",
        "stage": "Negotiation",
        "expected_close_date": "20-Mar-2026"
    },
    {
        "id": "D104",
        "name": "Tata Steel Iron Ore Pit Volumetric Survey",
        "sector": "Mining",
        "deal_size": "₹95,00,000",
        "stage": "Closed Won",
        "expected_close_date": "2026-02-01"
    },
    {
        "id": "D105",
        "name": "Reliance Jamnagar Refinery Inspection",
        "sector": "energy sector",
        "deal_size": "₹4,10,00,000",
        "stage": "Qualified Lead",
        "expected_close_date": "Jan 28, 2026"
    },
    {
        "id": "D106",
        "name": "L&T Smart City Topographical Survey",
        "sector": "construction sector",
        "deal_size": "₹1,50,00,000",
        "stage": "Proposal Sent",
        "expected_close_date": "2026-04-10"
    },
    {
        "id": "D107",
        "name": "Karnataka Crop Health Analytics Initiative",
        "sector": "Agri-Tech",
        "deal_size": "₹75,00,000",
        "stage": "Closed Won",
        "expected_close_date": "15/01/2026"
    },
    {
        "id": "D108",
        "name": "GMR Hyderabad Airport Runway Thermal Scan",
        "sector": "Infrastructure",
        "deal_size": "₹1.2 Cr",
        "stage": "Negotiation",
        "expected_close_date": "TBD"  # Intentional missing/invalid date
    },
    {
        "id": "D109",
        "name": "Coal India Singrauli Overburden Assessment",
        "sector": "MINING",
        "deal_size": None,  # Intentional missing value
        "stage": "Proposal Sent",
        "expected_close_date": "2026-03-30"
    },
    {
        "id": "D110",
        "name": "PowerGrid High Tension Transmission Monitoring",
        "sector": "Power & Energy",
        "deal_size": "₹2,10,00,000",
        "stage": "Closed Lost",
        "expected_close_date": "2026-02-14"
    },
    {
        "id": "D111",
        "name": "Irrigation Canal LiDAR Mapping - MP Govt",
        "sector": "Utilities",
        "deal_size": "₹1,85,00,000",
        "stage": "Closed Won",
        "expected_close_date": "2026-01-25"
    },
    {
        "id": "D112",
        "name": "Jindal Steel Stockpile Measurement",
        "sector": "Mining",
        "deal_size": "₹60,00,000",
        "stage": "Closed Won",
        "expected_close_date": "2026-02-28"
    },
    {
        "id": "D113",
        "name": "BHEL Haridwar Facility 3D Modeling",
        "sector": "Civil Construction",
        "deal_size": "₹1,10,00,000",
        "stage": "Proposal Sent",
        "expected_close_date": "12/04/2026"
    },
    {
        "id": "D114",
        "name": "Vedanta Aluminium Smelter Thermal Audit",
        "sector": "Mining",
        "deal_size": "₹1.4 Cr",
        "stage": "Negotiation",
        "expected_close_date": "2026-03-15"
    },
    {
        "id": "D115",
        "name": "Border Defense Surveillance Pilot",
        "sector": "Defense & Aerospace",
        "deal_size": "₹5,00,00,000",
        "stage": "Qualified Lead",
        "expected_close_date": "2026-05-01"
    }
]


MOCK_WORK_ORDERS_RAW = [
    {
        "id": "WO201",
        "name": "WO - NTPC Solar Thermal Survey Flight Execution",
        "deal_name": "NTPC Solar Thermal Survey - Phase 2",
        "sector": "Energy",
        "status": "Completed",
        "contract_value": "₹2,50,00,000",
        "start_date": "2026-01-16",
        "target_completion_date": "2026-02-10"
    },
    {
        "id": "WO202",
        "name": "WO - Tata Steel Iron Ore Pit Flight Operations",
        "deal_name": "Tata Steel Iron Ore Pit Volumetric Survey",
        "sector": "MINING",
        "status": "In Progress",
        "contract_value": "₹95,00,000",
        "start_date": "2026-02-02",
        "target_completion_date": "2026-03-15"
    },
    {
        "id": "WO203",
        "name": "WO - Karnataka Crop Health Flight & Processing",
        "deal_name": "Karnataka Crop Health Analytics Initiative",
        "sector": "Agri-Tech",
        "status": "Delayed Flight Ops",
        "contract_value": "₹75,00,000",
        "start_date": "2026-01-18",
        "target_completion_date": "2026-02-20"
    },
    {
        "id": "WO204",
        "name": "WO - Irrigation Canal LiDAR Field Survey",
        "deal_name": "Irrigation Canal LiDAR Mapping - MP Govt",
        "sector": "utilities",
        "status": "In Progress",
        "contract_value": "₹1,85,00,000",
        "start_date": "2026-01-28",
        "target_completion_date": "2026-03-30"
    },
    {
        "id": "WO205",
        "name": "WO - Jindal Steel Volumetric Processing",
        "deal_name": "Jindal Steel Stockpile Measurement",
        "sector": "Mining",
        "status": "Completed",
        "contract_value": "₹60,00,000",
        "start_date": "2026-03-01",
        "target_completion_date": "2026-03-12"
    },
    {
        "id": "WO206",
        "name": "WO - NHAI Highway Preliminary Reconnaissance",
        "deal_name": "NHAI Delhi-Mumbai Expressway Corridor Flight",
        "sector": "infra",
        "status": "Overdue",
        "contract_value": "₹3,20,00,000",
        "start_date": "2026-02-10",
        "target_completion_date": "2026-02-25"
    },
    {
        "id": "WO207",
        "name": "WO - Solar Power Plant Thermal Baseline Scan",
        "deal_name": "Adani Green Wind Farm Mapping",
        "sector": "Energy Sector",
        "status": "Awaiting Clearance",  # Maps to On Hold
        "contract_value": "₹1,80,00,000",
        "start_date": "2026-02-15",
        "target_completion_date": "N/A"  # Intentional missing date
    },
    {
        "id": "WO208",
        "name": "WO - Refinery Flare Stack Inspection",
        "deal_name": "Reliance Jamnagar Refinery Inspection",
        "sector": "ENERGY",
        "status": "Scheduled",
        "contract_value": None,  # Intentional missing value
        "start_date": "2026-03-01",
        "target_completion_date": "2026-04-15"
    }
]
