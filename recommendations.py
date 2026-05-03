
# ============================================================
# recommendations.py — Actionable Climate Intelligence Engine
# ============================================================

RECOMMENDATIONS = {
    "HEAT_WAVE": {
        "icon": "🔥", "color": "#FF4B4B", "label": "Extreme Heat Event",
        "description": "Temperatures significantly above seasonal norms. High risk of drought, crop damage, and public health emergencies.",
        "Agriculture": {
            "priority": "HIGH",
            "actions": [
                "📌 Increase irrigation frequency by 40% — soil moisture is critical",
                "🌾 Apply mulching to reduce soil evaporation losses",
                "⏰ Shift field operations to early morning (before 7am) or after sunset",
                "🐄 Ensure shade and ample water supply for all livestock",
                "🌱 Monitor crops for heat stress — consider temporary shade nets",
            ]
        },
        "Health": {
            "priority": "CRITICAL",
            "actions": [
                "🚨 Issue public heat advisory — alert elderly, children & outdoor workers",
                "🏢 Open air-conditioned cooling centers in public buildings",
                "🚑 Increase ambulance readiness for heat stroke cases",
                "💧 Distribute ORS packets in slums and low-income areas",
                "📵 Advise against outdoor activity between 11am–4pm",
            ]
        },
        "Infrastructure": {
            "priority": "MODERATE",
            "actions": [
                "⚡ Monitor power grid load — heavy AC demand surge expected",
                "🛣️ Inspect roads for heat buckling — reduce speed limits if needed",
                "🔧 Pre-position repair crews near electrical substations",
                "🚆 Check railway track expansion gaps for thermal stress",
            ]
        },
        "Water": {
            "priority": "HIGH",
            "actions": [
                "💧 Activate water conservation protocols immediately",
                "📊 Monitor reservoir levels daily — alert if below 40% capacity",
                "🚫 Restrict non-essential water use (car washing, park irrigation)",
                "🌊 Accelerate groundwater recharge programs",
            ]
        },
    },
    "COLD_SNAP": {
        "icon": "❄️", "color": "#00B4FF", "label": "Cold Snap / Frost Event",
        "description": "Temperatures significantly below seasonal norms. Risk of crop damage, infrastructure failure, and hypothermia.",
        "Agriculture": {
            "priority": "CRITICAL",
            "actions": [
                "🌾 Apply frost protection covers to sensitive crops immediately",
                "🔥 Use smudge pots or wind machines to prevent frost settling",
                "📦 Accelerate harvest of mature crops before temperatures drop further",
                "🐄 Move livestock to sheltered enclosures with insulated bedding",
            ]
        },
        "Health": {
            "priority": "HIGH",
            "actions": [
                "🏠 Issue cold advisory — ensure homeless shelters are open 24/7",
                "🧥 Organize warm clothing distribution in low-income areas",
                "🚑 Alert hospitals to prepare for hypothermia and respiratory cases",
                "👴 Initiate daily wellness checks on elderly living alone",
            ]
        },
        "Infrastructure": {
            "priority": "HIGH",
            "actions": [
                "🛣️ Pre-treat roads with salt/sand — ice formation risk is high",
                "💧 Insulate exposed water pipelines to prevent burst pipes",
                "⚡ Increase heating grid capacity — energy demand surge expected",
                "✈️ Alert airports to prepare for de-icing operations",
            ]
        },
        "Water": {
            "priority": "MODERATE",
            "actions": [
                "💧 Protect water pipes from freezing — insulation wrap critical",
                "🔄 Keep water flowing at low pressure if overnight freezing is expected",
                "📊 Monitor snowpack levels for spring flood prediction",
            ]
        },
    },
    "EXTREME_RAIN": {
        "icon": "🌧️", "color": "#845EC2", "label": "Extreme Rainfall Event",
        "description": "Precipitation far above normal. Flooding, waterlogging, and infrastructure damage risk is very high.",
        "Agriculture": {
            "priority": "HIGH",
            "actions": [
                "🌾 Harvest mature crops immediately before field flooding",
                "💧 Clear field drainage channels — remove blockages urgently",
                "🐄 Move livestock to higher ground or covered shelters",
                "🌱 Assess soil erosion risk and apply protective measures",
            ]
        },
        "Health": {
            "priority": "CRITICAL",
            "actions": [
                "🚨 Issue flood warning to all low-lying communities",
                "💊 Pre-position medicines for waterborne diseases (cholera, typhoid)",
                "🏥 Establish emergency medical camps in flood-prone areas",
                "🚣 Deploy rescue boats and NDRF teams to high-risk zones",
            ]
        },
        "Infrastructure": {
            "priority": "CRITICAL",
            "actions": [
                "🏗️ Inspect dams, embankments, and drainage systems immediately",
                "🚧 Close flood-prone roads and bridges — deploy traffic diversions",
                "⚡ Protect electrical substations with sandbags",
                "📡 Ensure emergency communication systems are fully operational",
            ]
        },
        "Water": {
            "priority": "HIGH",
            "actions": [
                "💧 Open flood relief channels to protect urban areas",
                "🌊 Monitor river gauge stations every 2 hours",
                "🚰 Protect drinking water treatment plants from contamination",
                "📊 Pre-discharge reservoir water to create flood buffer capacity",
            ]
        },
    },
    "DROUGHT": {
        "icon": "🏜️", "color": "#FF9000", "label": "Drought Conditions",
        "description": "Prolonged dry period with abnormally low precipitation. Long-term water and food security risk.",
        "Agriculture": {
            "priority": "CRITICAL",
            "actions": [
                "🌾 Switch to drought-resistant crop varieties (millets, sorghum, bajra)",
                "💧 Implement drip/micro irrigation — reduce water use by up to 60%",
                "📋 Apply for crop insurance and government drought relief immediately",
                "🌱 Adopt soil moisture conservation techniques (contour farming, mulching)",
            ]
        },
        "Health": {
            "priority": "MODERATE",
            "actions": [
                "💧 Ensure equitable drinking water distribution in all wards",
                "🏥 Monitor malnutrition and dehydration in vulnerable communities",
                "🧴 Promote hygiene even under water rationing constraints",
                "📊 Track food security indicators in drought-affected areas",
            ]
        },
        "Infrastructure": {
            "priority": "HIGH",
            "actions": [
                "🚛 Deploy water tankers to water-scarce communities immediately",
                "🔧 Repair and seal all water distribution pipeline leakages",
                "⚡ Prepare for power cuts — reduced hydro-power output expected",
                "🏗️ Fast-track rainwater harvesting infrastructure projects",
            ]
        },
        "Water": {
            "priority": "CRITICAL",
            "actions": [
                "🚫 Declare water emergency — implement strict rationing protocols",
                "💧 Activate inter-basin water transfer agreements",
                "🌊 Accelerate all rainwater harvesting and storage projects",
                "📊 Monitor groundwater table levels on a daily basis",
            ]
        },
    },
    "COMPOUND": {
        "icon": "⚠️", "color": "#FF6B6B", "label": "Compound Climate Anomaly",
        "description": "Multiple climate variables are simultaneously anomalous. Complex multi-sector response required.",
        "Agriculture": {
            "priority": "HIGH",
            "actions": [
                "📋 Conduct immediate crop damage and field condition assessment",
                "🌾 Consult agricultural extension services for location-specific advice",
                "💧 Review water usage — balance between flood and drought protocols",
                "🐄 Protect livestock based on the dominant climate threat",
            ]
        },
        "Health": {
            "priority": "HIGH",
            "actions": [
                "🚨 Issue a general climate health advisory across all wards",
                "🏥 Increase hospital capacity and readiness for climate-related cases",
                "📡 Activate community health monitoring systems immediately",
            ]
        },
        "Infrastructure": {
            "priority": "MODERATE",
            "actions": [
                "🔧 Conduct infrastructure vulnerability assessment",
                "📡 Ensure emergency response systems are fully operational",
                "🚧 Monitor all critical infrastructure (dams, power grid, roads)",
            ]
        },
        "Water": {
            "priority": "MODERATE",
            "actions": [
                "💧 Monitor all water systems for compound stress effects",
                "📊 Increase monitoring frequency for all water bodies",
            ]
        },
    },
}

PRIORITY_CONFIG = {
    "CRITICAL": {"color": "#FF4B4B", "icon": "🔴", "order": 0},
    "HIGH":     {"color": "#FF9000", "icon": "🟠", "order": 1},
    "MODERATE": {"color": "#FFD700", "icon": "🟡", "order": 2},
    "LOW":      {"color": "#00C851", "icon": "🟢", "order": 3},
}

SECTOR_ICONS = {
    "Agriculture": "🌾",
    "Health": "❤️",
    "Infrastructure": "🏗️",
    "Water": "💧",
}


def get_recommendations(anomaly_type: str) -> dict:
    return RECOMMENDATIONS.get(anomaly_type, RECOMMENDATIONS["COMPOUND"])


def get_dominant_anomaly(df) -> str:
    anomaly_df = df[df["anomaly"] == -1]
    if len(anomaly_df) == 0:
        return "NORMAL"
    if "severity" in anomaly_df.columns:
        type_severity = anomaly_df.groupby("anomaly_type")["severity"].mean()
        return type_severity.idxmax()
    return anomaly_df["anomaly_type"].mode()[0]


def get_summary_stats(df) -> dict:
    total = len(df)
    anomaly_df = df[df["anomaly"] == -1]
    n = len(anomaly_df)
    return {
        "total_records": total,
        "n_anomalies": n,
        "anomaly_rate": round(n / total * 100, 1) if total > 0 else 0,
        "type_counts": anomaly_df["anomaly_type"].value_counts().to_dict() if n > 0 else {},
        "max_severity": int(anomaly_df["severity"].max()) if n > 0 else 0,
        "avg_severity": round(float(anomaly_df["severity"].mean()), 1) if n > 0 else 0,
    }
