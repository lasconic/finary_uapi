#!/usr/bin/env python3
"""
Finary MCP Server
-----------------
Expose l'API non-officielle Finary comme un serveur MCP (Model Context Protocol).
Un LLM peut ainsi interroger directement votre portefeuille Finary.

Prérequis :
  - credentials.json à la racine (même format que credentials.json.tpl)
  - poetry run python -m finary_uapi signin  (première connexion)
  - poetry run python mcp_server.py
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any

# Force le répertoire de travail vers le dossier du script,
# afin que jwt.json, cookies.txt et credentials.json soient toujours trouvés,
# quel que soit le cwd utilisé par Claude Desktop au lancement.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions

try:
    from finary_uapi.auth import prepare_session
    import finary_uapi.user_portfolio as portfolio
    import finary_uapi.user_me as user_me
    import finary_uapi.user_real_estates as user_real_estates
    import finary_uapi.user_scpis as user_scpis
    import finary_uapi.user_generic_assets as user_generic_assets
    import finary_uapi.user_fonds_euro as user_fonds_euro
    import finary_uapi.user_startups as user_startups
    import finary_uapi.user_precious_metals as user_precious_metals
    import finary_uapi.user_crowdlendings as user_crowdlendings
except ImportError as e:
    print(f"[ERREUR] Import finary_uapi échoué : {e}", file=sys.stderr)
    sys.exit(1)

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("finary-mcp")

# ── Session globale réutilisée entre les appels ────────────────────────────────
_session = None


def get_session():
    """
    Retourne une session authentifiée.
    prepare_session() relit le cookie sauvegardé par 'signin' et le renouvelle
    si besoin. Les credentials viennent de credentials.json (géré nativement par signin).
    """
    global _session
    if _session is None:
        logger.info("Préparation de la session Finary…")
        _session = prepare_session()
        if _session is None:
            raise RuntimeError(
                "Impossible d'obtenir une session Finary. "
                "Lancez d'abord : poetry run python -m finary_uapi signin"
            )
        logger.info("Session Finary prête.")
    return _session


def _json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


# ── Serveur MCP ────────────────────────────────────────────────────────────────
app = Server("finary-mcp")

TOOLS = [
    types.Tool(
        name="finary_portfolio",
        description=(
            "Vue globale du portefeuille Finary par classe d'actifs "
            "(cryptos, actions, immobilier, crowdlending…) avec valorisation et performance."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "description": (
                        "Classe d'actifs : 'cryptos', 'investments', 'real_estates', "
                        "'crowdlendings', 'fonds_euro', 'precious_metals', "
                        "'startups', 'scpis', ou laisser vide pour tout."
                    ),
                    "default": "",
                }
            },
        },
    ),
    types.Tool(
        name="finary_portfolio_distribution",
        description="Répartition du patrimoine global par classe d'actifs (allocation en %).",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_portfolio_timeseries",
        description="Historique de valorisation du portefeuille sur une période.",
        inputSchema={
            "type": "object",
            "properties": {
                "period": {
                    "type": "string",
                    "enum": ["1w", "1m", "ytd", "1y", "all"],
                    "default": "1m",
                    "description": "Période : 1 semaine, 1 mois, depuis janvier, 1 an, tout",
                }
            },
        },
    ),
    types.Tool(
        name="finary_investments",
        description="Liste les investissements en valeurs mobilières (actions, ETF, fonds).",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_investments_dividends",
        description="Dividendes perçus sur les investissements.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_investments_transactions",
        description="Historique des transactions sur les investissements.",
        inputSchema={
            "type": "object",
            "properties": {
                "page": {"type": "integer", "default": 1},
                "per_page": {"type": "integer", "default": 20},
            },
        },
    ),
    types.Tool(
        name="finary_cryptos",
        description="Liste les cryptomonnaies détenues avec quantité, prix et plus/moins-value.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_cryptos_distribution",
        description="Répartition des cryptomonnaies par devise.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_precious_metals",
        description="Liste les métaux précieux détenus (or, argent…) avec leur valorisation.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_real_estates",
        description="Liste les biens immobiliers avec valeur estimée, prix d'achat et rendement.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_crowdlendings",
        description="Liste les investissements en crowdlending avec taux et durée.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_crowdlendings_distribution",
        description="Répartition des crowdlendings par plateforme.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_fonds_euro",
        description="Liste les fonds euros (assurance-vie) avec leur valorisation.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_startups",
        description="Liste les investissements en startups / equity non coté.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_scpis",
        description="Liste les SCPI détenues avec leur rendement.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_generic_assets",
        description="Liste les actifs génériques (art, voiture, objets de valeur…).",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_checking_accounts_transactions",
        description="Transactions des comptes courants.",
        inputSchema={
            "type": "object",
            "properties": {
                "page": {"type": "integer", "default": 1},
                "per_page": {"type": "integer", "default": 20},
            },
        },
    ),
    types.Tool(
        name="finary_me",
        description="Informations sur le compte utilisateur Finary connecté.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="finary_wealth_summary",
        description=(
            "Retourne la valeur totale du patrimoine Finary agrégée par catégorie : "
            "Immobilier (SCPI + biens physiques), Actions & Fonds, Crypto, Fonds euros, "
            "Startups & PME, Crowdlending, Métaux précieux, Comptes bancaires, Autres. "
            "Utiliser cet outil pour répondre à toute question sur la valeur totale du patrimoine."
        ),
        inputSchema={"type": "object", "properties": {}},
    ),
]


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        session = get_session()
        result = _dispatch(session, name, arguments)
        return [types.TextContent(type="text", text=_json(result))]
    except RuntimeError as e:
        return [types.TextContent(type="text", text=f"[ERREUR] {e}")]
    except Exception as e:
        logger.exception(f"Erreur inattendue — outil : {name}")
        return [types.TextContent(type="text", text=f"[ERREUR INATTENDUE] {e}")]



def _get_category_total(data: Any) -> float:
    """Extrait la valeur totale depuis une réponse finary_uapi."""
    try:
        result = data.get("result", data)
        if isinstance(result, list):
            return sum(
                item.get("current_value", item.get("amount", item.get("value", 0)))
                for item in result
            )
        if isinstance(result, dict):
            # Cherche un champ "total" ou "amount" ou "current_value"
            for key in ("total", "amount", "current_value", "value"):
                if key in result:
                    val = result[key]
                    if isinstance(val, dict):
                        return val.get("amount", 0)
                    return float(val) if val else 0
    except Exception:
        pass
    return 0


def _wealth_summary(session) -> dict:
    """Appelle chaque catégorie et agrège les totaux."""
    def safe(fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Erreur lors de la récupération ({fn.__name__}): {e}")
            return {}

    categories = {
        "Immobilier — Biens physiques": safe(user_real_estates.get_user_real_estates, session),
        "Immobilier — SCPI":            safe(user_scpis.get_user_scpis, session),
        "Actions & Fonds":              safe(portfolio.get_portfolio_investments, session),
        "Crypto":                       safe(portfolio.get_portfolio_cryptos, session),
        "Fonds euros":                  safe(user_fonds_euro.get_user_fonds_euro, session),
        "Startups & PME":               safe(user_startups.get_user_startups, session),
        "Crowdlending":                 safe(user_crowdlendings.get_user_crowdlendings, session),
        "Métaux précieux":              safe(user_precious_metals.get_user_precious_metals, session),
        "Autres (actifs génériques)":   safe(user_generic_assets.get_user_generic_assets, session),
    }

    summary = {}
    grand_total = 0.0

    for label, data in categories.items():
        total = _get_category_total(data)
        summary[label] = {
            "total_eur": round(total, 2),
            "raw": data,
        }
        grand_total += total

    return {
        "patrimoine_total_eur": round(grand_total, 2),
        "categories": summary,
    }

def _dispatch(session, name: str, args: dict) -> Any:
    """Appelle la fonction finary_uapi correspondante au nom de l'outil MCP."""

    if name == "finary_portfolio":
        asset_type = args.get("type", "")
        return portfolio.get_portfolio(session, asset_type) if asset_type else portfolio.get_portfolio(session)

    elif name == "finary_portfolio_distribution":
        return portfolio.get_portfolio_distribution(session)

    elif name == "finary_portfolio_timeseries":
        return portfolio.get_portfolio_timeseries(session, args.get("period", "1m"))

    elif name == "finary_investments":
        return portfolio.get_portfolio_investments(session)

    elif name == "finary_investments_dividends":
        return portfolio.get_portfolio_investments_dividends(session)

    elif name == "finary_investments_transactions":
        return portfolio.get_portfolio_investments_transactions(
            session, page=args.get("page", 1), per_page=args.get("per_page", 20)
        )

    elif name == "finary_cryptos":
        return portfolio.get_portfolio_cryptos(session)

    elif name == "finary_cryptos_distribution":
        return portfolio.get_portfolio_cryptos_distribution(session)

    elif name == "finary_precious_metals":
        return user_precious_metals.get_user_precious_metals(session)

    elif name == "finary_real_estates":
        return user_real_estates.get_user_real_estates(session)

    elif name == "finary_crowdlendings":
        return user_crowdlendings.get_user_crowdlendings(session)

    elif name == "finary_crowdlendings_distribution":
        return user_crowdlendings.get_user_crowdlendings(session)

    elif name == "finary_fonds_euro":
        return user_fonds_euro.get_user_fonds_euro(session)

    elif name == "finary_startups":
        return user_startups.get_user_startups(session)

    elif name == "finary_scpis":
        return user_scpis.get_user_scpis(session)

    elif name == "finary_generic_assets":
        return user_generic_assets.get_user_generic_assets(session)

    elif name == "finary_checking_accounts_transactions":
        return portfolio.get_portfolio_checking_accounts_transactions(
            session, page=args.get("page", 1), per_page=args.get("per_page", 20)
        )

    elif name == "finary_me":
        return user_me.get_user_me(session)

    elif name == "finary_wealth_summary":
        return _wealth_summary(session)

    else:
        raise ValueError(f"Outil inconnu : {name}")


# ── Point d'entrée ─────────────────────────────────────────────────────────────
async def main():
    logger.info("Démarrage du serveur MCP Finary…")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="finary-mcp",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())