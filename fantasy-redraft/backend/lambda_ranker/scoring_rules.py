# scoring_rules.py

# Each profile is a complete ruleset.
# You can add: "half_ppr_2026", "ppr_2025", "dynasty_2024", etc.

RULESETS: dict[str, dict] = {
    "default_2026": {
        # Passing (points per stat-unit)
        "pass_td": 4.0,
        "interception": -2.0,
        "pick_six": -4.0,
        "pass_yd": 1 / 25,     # points per passing yard
        "pass_1d": 0.2,        # points per passing first down

        # Rushing
        "rush_td": 6.0,
        "rush_yd": 0.1,        # points per rushing yard (1/10)
        "rush_1d": 0.3,
        "rush_bonuses": [      # data-driven thresholds
            {"yd": 100, "pts": 2},
            {"yd": 200, "pts": 4},
        ],

        # Receiving
        "reception": 0.5,
        "rec_td": 6.0,
        "rec_yd": 0.1,         # points per receiving yard (1/10)
        "rec_1d": 0.5,
        "rec_bonuses": [
            {"yd": 200, "pts": 4},
        ],

        # Other
        "return_td": 6.0,
        "two_pt": 2.0,
        "fumble_lost": -2.0,
    },

    # Example alternate profile (optional)
    "ppr_2026": {
        "reception": 1.0,
        "rush_bonuses": [{"yd": 100, "pts": 2}, {"yd": 200, "pts": 4}],
        "rec_bonuses": [{"yd": 200, "pts": 4}],
    },
}

# What your scoring.py imports
DEFAULT_RULES = RULESETS["default_2026"]
