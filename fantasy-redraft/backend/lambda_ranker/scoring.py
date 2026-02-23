from typing import Any
from scoring_rules import DEFAULT_RULES




def _safe_float(x: Any, default: float = 0.0) -> float:              #api input from json could be anything. turns anything into number
    try:
        return float(x)
    except (TypeError, ValueError):
        return float(default)

def _apply_bonus_list(yards: float, bonuses: Any) -> float:
    """
    bonuses can be:
      - list of {"yd": 100, "pts": 2} (your current style)
      - list of {"yards": 100, "points": 2} (alternate style)
    We support both.
    """
    if not isinstance(bonuses, list):                                   #isinstance checks value at run time
        return 0.0

    pts = 0.0
    for b in bonuses:
        if not isinstance(b, dict):
            continue
        thr = _safe_float(b.get("yd", b.get("yards", 0.0)))
        add = _safe_float(b.get("pts", b.get("points", 0.0)))
        if yards >= thr:
            pts += add
    return pts

def compute_fantasy_points(p: dict, s: dict | None = None) -> tuple[float, dict]:     #if caller doesnt pass "s" set it to "none" automatically
    """
    Compute fantasy points for a single player projection dict `p`
    using league settings dict `s`.

    Returns:
        (total_points, breakdown_dict)
    """
    # Build data-driven rules: defaults + request overrides
    rules = DEFAULT_RULES.copy()
    if s:
        rules.update(s)

    breakdown: dict[str, float] = {}

    # Backward compatibility: if user already supplies projected_points, use it
    if p.get("projected_points") is not None:
        pts = _safe_float(p["projected_points"])
        breakdown["projected_points"] = pts
        return pts, breakdown

    # --- Passing ---
    pass_yd = _safe_float(p.get("pass_yd", 0))
    pass_td = _safe_float(p.get("pass_td", 0))
    interceptions = _safe_float(p.get("interceptions", 0))
    pick_six = _safe_float(p.get("pick_six", 0))
    pass_1d = _safe_float(p.get("pass_1d", 0))

    breakdown["pass_td"] = pass_td * _safe_float(rules.get("pass_td", 4.0))
    breakdown["interceptions"] = interceptions * _safe_float(rules.get("interception", -2.0))
    breakdown["pick_six"] = pick_six * _safe_float(rules.get("pick_six", -4.0))

    # You currently store pass yard scoring as "points per yard" in settings:
    # default is 1/25 points per yard.
    breakdown["pass_yd"] = pass_yd * _safe_float(rules.get("pass_yd", 1 / 25))
    breakdown["pass_1d"] = pass_1d * _safe_float(rules.get("pass_1d", 0.2))

    # --- Rushing ---
    rush_yd = _safe_float(p.get("rush_yd", 0))
    rush_td = _safe_float(p.get("rush_td", 0))
    rush_1d = _safe_float(p.get("rush_1d", 0))

    breakdown["rush_yd"] = rush_yd * _safe_float(rules.get("rush_yd", 0.1))  # 1/10 per yard
    breakdown["rush_td"] = rush_td * _safe_float(rules.get("rush_td", 6.0))
    breakdown["rush_1d"] = rush_1d * _safe_float(rules.get("rush_1d", 0.3))

    # Data-driven rush bonuses (preferred)
    rush_bonus_pts = _apply_bonus_list(rush_yd, rules.get("rush_bonuses"))
    # Backward compatibility: old two-threshold style
    if rush_bonus_pts == 0.0 and not isinstance(rules.get("rush_bonuses"), list):
        if rush_yd >= 200:
            rush_bonus_pts = _safe_float(rules.get("rush_bonus_200", 4.0))
        elif rush_yd >= 100:
            rush_bonus_pts = _safe_float(rules.get("rush_bonus_100", 2.0))
    breakdown["rush_bonus"] = rush_bonus_pts

    # --- Receiving ---
    rec = _safe_float(p.get("reception", 0))
    rec_yd = _safe_float(p.get("rec_yd", 0))
    rec_td = _safe_float(p.get("rec_td", 0))
    rec_1d = _safe_float(p.get("rec_1d", 0))

    breakdown["rec"] = rec * _safe_float(rules.get("reception", 0.5))
    breakdown["rec_yd"] = rec_yd * _safe_float(rules.get("rec_yd", 0.1))     # 1/10 per yard
    breakdown["rec_td"] = rec_td * _safe_float(rules.get("rec_td", 6.0))
    breakdown["rec_1d"] = rec_1d * _safe_float(rules.get("rec_1d", 0.5))

    # Data-driven receiving bonuses (if you later add rec_bonuses list)
        # Data-driven receiving bonuses (if you later add rec_bonuses list)
    rec_bonus_pts = _apply_bonus_list(rec_yd, rules.get("rec_bonuses"))
    # Backward compatibility: old one-threshold style
    if rec_bonus_pts == 0.0 and rec_yd >= 200:
        rec_bonus_pts = _safe_float(rules.get("rec_bonus_200", 4.0))
    breakdown["rec_bonus"] = rec_bonus_pts

    # --- Returns / misc TDs ---
    return_td = _safe_float(p.get("return_td", 0))
    breakdown["return_td"] = return_td * _safe_float(rules.get("return_td", 6.0))

    # --- 2-point conversions ---
    two_pt = _safe_float(p.get("two_pt", 0))
    breakdown["two_pt"] = two_pt * _safe_float(rules.get("two_pt", 2.0))

    # --- Fumbles ---
    fumbles_lost = _safe_float(p.get("fumble_lost", 0))
    breakdown["fumbles_lost"] = fumbles_lost * _safe_float(rules.get("fumble_lost", -2.0))

    total = sum(breakdown.values())
    return total, breakdown

def apply_importance_layer(players: list[dict], context: dict | None = None) -> list[dict]:
    if not context:                                                                   #no context=do nothing
        return players

    phase = (context.get("phase") or "regular").lower()                                 #lower just changes capital letters to lowercase
    risk = (context.get("risk_tolerance") or "medium").lower()                          #pulls key words that weight model
    need_pos = set((context.get("need_positions") or []))                               #gets positions

    updated = []

    for p in players:
        mult = 1.0

        if phase in ("playoffs", "championship"):
            mult *= 1.03

        volatility = float(p.get("volatility", 0.0))                                    #volatility is boom/bust risk
        if risk == "low":
            mult *= (1.0 - min(0.05, volatility * 0.02))
        elif risk == "high":
            mult *= (1.0 + min(0.05, volatility * 0.02))

        pos = (p.get("position") or "").upper()
        if pos in need_pos:
            mult *= 1.05

        p = {
            **p,                                                                        #dictionary unpacking, not a pointer to a pointer. create new dict and copy key values over
            "importance_multiplier": round(mult, 4),
            "value_score": round(p["fantasy_points"] * mult, 2)
        }

        updated.append(p)

    return updated

def apply_draft_bias(players: list[dict], league_settings: dict | None = None) -> list[dict]:
    
    league_setting = league_settings or {}

    default_bias = {
        "RB": 1.10,
        "WR": 1.08,
        "TE": 1.03,
        "QB": 0.95,
        "K":  0.85,
        "DST": 0.80,
    }
    bias_map = {**default_bias, **(league_settings.get("position_bias") or {})}     #defaut. allows customizable and multiple leages; would have to edit code. creates new dict

    updated = []
    for p in players:                                                               #goes through all players
        pos = (p.get("position") or "").upper()

        bias = float(bias_map.get(pos, 1.0))  # unknown position -> neutral
        base = float(p.get("value_score", p.get("fantasy_points", 0.0)))

        updated.append({
            **p,
            "position_bias": round(bias, 4),
            "draft_score": round(base * bias, 2),
        })

    # If you want this function to also sort, do it here:
    updated.sort(key=lambda x: x["draft_score"], reverse=True)
    return updated

def add_explanations(
    players: list[dict],
    context: dict | None = None,
    league_settings: dict | None = None,
) -> list[dict]:
    context = context or {}
    league_settings = league_settings or {}

    phase = (context.get("phase") or "regular").lower()
    risk = (context.get("risk_tolerance") or "medium").lower()
    need_pos = set((context.get("need_positions") or []))

    default_bias = {
        "RB": 1.10, "WR": 1.08, "TE": 1.03, "QB": 0.95, "K": 0.85, "DST": 0.80
    }
    bias_map = {**default_bias, **(league_settings.get("position_bias") or {})}

    updated = []
    for p in players:
        explanations: list[str] = []

        # --- Phase note (importance layer) ---
        if phase in ("playoffs", "championship"):
            explanations.append(f"High-stakes phase: {phase} (importance boost applied)")

        # --- Risk / volatility note ---
        vol = float(p.get("volatility", 0.0))
        if vol > 0:
            if risk == "low":
                explanations.append(f"Low risk tolerance: volatility penalized (vol={vol:g})")
            elif risk == "high":
                explanations.append(f"High risk tolerance: volatility rewarded (vol={vol:g})")

        # --- Need positions note ---
        pos = (p.get("position") or "").upper()
        if pos in need_pos:
            explanations.append(f"Team need match: {pos} boosted")

        # --- Position bias note (draft strategy layer) ---
        bias = float(p.get("position_bias", bias_map.get(pos, 1.0)))
        if abs(bias - 1.0) > 1e-9:
            pct = (bias - 1.0) * 100.0
            if pct > 0:
                explanations.append(f"Positional scarcity bias: {pos} +{pct:.1f}%")
            else:
                explanations.append(f"Positional scarcity bias: {pos} {pct:.1f}%")

        # Fallback if nothing triggered
        if not explanations:
            explanations.append("No contextual adjustments applied")

        updated.append({**p, "explanations": explanations})

    return updated


def rank_players(players: list[dict], settings: dict | None = None, context: dict | None = None, top_n: int = 50) -> list[dict]:
    """
    Returns players enriched with:
      - base_points
      - adjusted_value (importance-adjusted)
      - breakdown
    Sorted by adjusted_value desc.
    """
    enriched: list[dict] = []

    for p in players:
        base_pts, breakdown = compute_fantasy_points(p, settings)
        adj = apply_importance_layer(p, base_pts, context or {})

        enriched.append({
            **p,
            "base_points": round(base_pts, 2),
            "adjusted_value": round(adj, 2),
            "breakdown": breakdown,
        })

    ranked = sorted(enriched, key=lambda x: x["adjusted_value"], reverse=True)
    return ranked[:top_n]




