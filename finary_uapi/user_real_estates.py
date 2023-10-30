import requests
from .constants import API_ROOT
from .utils import get_and_print
from .real_estates import get_real_estates_placeid
import json
import logging
from typing import Dict, Union
from .user_me import get_display_currency_code, update_display_currency_by_code


def get_user_real_estates(session: requests.Session):
    url = f"{API_ROOT}/users/me/real_estates"
    return get_and_print(session, url)


def add_user_real_estates(
    session: requests.Session,
    # category: rent, live_primary, live_secondary, other
    category,
    # use to get the place ID from address
    address,
    # user estimated price in Euro
    user_estimated_value,
    description,
    # surface un sqm
    surface,
    # buying price in Euro
    buying_price,
    # building type: house, building, apartment, land, commercial, parking_box, or other
    building_type,
    # ownership percentage 0.00 format
    ownership_percentage,
    # monthy charges (total) in Euro (mandatory if rent category)
    monthly_charges=0,
    # monthly rent (total) in Euro (mandatory if rent category)
    monthly_rent=0,
    # yearly taxes in Euro (mandatory if rent category)
    yearly_taxes=0,
    # rental period: annual or seasonal (mandatory if rent category)
    rental_period="annual",
    # rental type: nue, lmnp or sci (mandatory if rent category)
    rental_type="nue",
):
    url = f"{API_ROOT}/users/me/real_estates"
    data: Dict[str, Union[str, bool, int, float]] = {}
    data["is_automated_valuation"] = False
    data["is_furnished"] = False
    data["is_new"] = False
    data["has_lift"] = False
    data["has_sauna"] = False
    data["has_pool"] = False
    data["flooring_quality"] = ""
    data["flooring_condition"] = ""
    data["windows_quality"] = ""
    data["windows_condition"] = ""
    data["bathrooms_quality"] = ""
    data["bathrooms_condition"] = ""
    data["kitchen_quality"] = ""
    data["kitchen_condition"] = ""
    data["general_quality"] = ""
    data["general_condition"] = ""
    data["parking_spaces"] = ""
    data["garage_spaces"] = ""
    data["number_of_rooms"] = ""
    data["number_of_bathrooms"] = ""
    data["number_of_floors"] = ""
    data["floor_number"] = ""
    data["balcony_area"] = ""
    data["garden_area"] = ""
    data["category"] = category
    data["is_estimable"] = False
    data["user_estimated_value"] = int(user_estimated_value)
    data["description"] = description
    data["surface"] = int(surface)
    data["agency_fees"] = ""
    data["notary_fees"] = ""
    data["furnishing_fees"] = ""
    data["renovation_fees"] = ""
    data["buying_price"] = int(buying_price)
    data["building_type"] = building_type
    data["ownership_percentage"] = float(ownership_percentage)
    data["place_id"] = get_real_estates_placeid(session, address)
    if category == "rent":
        data["monthly_charges"] = int(monthly_charges)
        data["monthly_rent"] = float(monthly_rent)
        data["yearly_taxes"] = int(yearly_taxes)
        data["rental_period"] = rental_period
        data["rental_type"] = rental_type
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.post(url, data=data_json, headers=headers)
    return x.json()


def update_user_real_estates(
    session: requests.Session,
    # category: rent, live_primary, live_secondary, other
    category,
    # 'asset_id' is the id of the asset for this user, as provided by GET
    asset_id,
    # user estimated price in Euro
    user_estimated_value,
    description,
    # surface un sqm
    # surface,
    # buying price in Euro
    buying_price,
    # building type: house, building, apartment, land, commercial, parking_box, or other
    # building_type,
    # ownership percentage 0.00 format
    ownership_percentage,
    # monthy charges (total) in Euro
    # monthly_charges,
    # monthly rent (total) in Euro
    monthly_rent,
    # yearly taxes in Euro
    # yearly_taxes,
    # rental period: annual or seasonal
    # rental_period,
    # rental type: nue, lmnp or sci
    # rental_type
):
    url = f"{API_ROOT}/users/me/real_estates/{asset_id}"
    data: Dict[str, Union[str, bool, int, float]] = {}
    data["user_estimated_value"] = int(user_estimated_value)
    data["description"] = description
    data["buying_price"] = int(buying_price)
    data["ownership_percentage"] = float(ownership_percentage)
    data["id"] = asset_id
    if category == "rent":
        data["monthly_rent"] = int(monthly_rent)
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.put(url, data=data_json, headers=headers)
    return x.json()


def delete_user_real_estates(session: requests.Session, asset_id):
    """
    `asset_id` is the id of the asset for this user, as provided by GET
    """
    url = f"{API_ROOT}/users/me/real_estates/{asset_id}"
    x = session.delete(url)
    logging.debug(x.status_code)
    return x.status_code


# convenience functions


def add_user_real_estates_with_currency(
    session: requests.Session,
    category,
    address,
    # currency code used by this real estate object
    # Currently limited by Finary to "EUR", "USD", "SGD", "CHF", "GBP",or "CAD"
    currency_code,
    user_estimated_value,
    description,
    surface,
    buying_price,
    building_type,
    ownership_percentage,
    monthly_charges=0,
    monthly_rent=0,
    yearly_taxes=0,
    rental_period="annual",
    rental_type="nue",
):
    current_display_currency = ""
    if not currency_code:
        currency_code = ""
    else:  # minimize number of calls, currency None or "" -> no call
        current_display_currency = get_display_currency_code(session)
    result = ""
    if currency_code == current_display_currency:
        result = add_user_real_estates(
            session,
            category,
            address,
            user_estimated_value,
            description,
            surface,
            buying_price,
            building_type,
            ownership_percentage,
            monthly_charges,
            monthly_rent,
            yearly_taxes,
            rental_period,
            rental_type,
        )
    else:
        update_display_currency_by_code(session, currency_code)
        result = add_user_real_estates(
            session,
            category,
            address,
            user_estimated_value,
            description,
            surface,
            buying_price,
            building_type,
            ownership_percentage,
            monthly_charges,
            monthly_rent,
            yearly_taxes,
            rental_period,
            rental_type,
        )
        update_display_currency_by_code(session, current_display_currency)
    return result
