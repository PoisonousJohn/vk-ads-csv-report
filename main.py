import argparse
import csv
import json
import logging
import os
from datetime import date, datetime, timedelta
from logging import Logger
from logging import basicConfig as loggingBasicConfig
from typing import List, Optional

import requests


class Api:
    base_url = "https://ads.vk.com/api/v2/"
    token_cache_file = "token.txt"
    token = ""

    def __init__(self, token: str) -> None:
        if not token:
            raise RuntimeError("Token is empty")
        self.token = token

    def _get_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def get_all_ad_plans(self) -> List[dict]:
        result = []
        query_params = {
            "limit": 20,
            "offset": 0,
        }

        while True:
            plans = self.get_method("ad_plans", query_params=query_params)
            result.extend(plans["items"])
            total_count = plans["count"]
            query_params["offset"] += query_params["limit"]
            if query_params["offset"] >= total_count:
                break

        return result

    def get_plans_stats(self, plan_ids: List[str], date_from: date, date_to: date):
        params = {
            "id": ",".join(plan_ids),
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat(),
        }

        return self.get_method("statistics/ad_plans/day", query_params=params)

    def get_method(self, method: str, query_params: Optional[dict] = None) -> dict:
        resp = requests.get(
            self.base_url + method + ".json",
            headers=self._get_headers(),
            timeout=5,
            params=query_params,
        )

        if resp.status_code != 200:
            raise RuntimeError(
                f"Failed to get {method}: {resp.status_code} {resp.text}"
            )

        return json.loads(resp.text)


def write_csv(stats: dict, id_to_name: dict, output_file: str):
    with open(output_file, "w", newline="", encoding="utf8") as f:
        fieldnames = ["name", "date", "clicks", "shows", "spent"]

        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()

        for item in stats["items"]:
            name = id_to_name.get(item["id"], "Unknown")
            for row in item["rows"]:
                values = {key: row["base"].get(key) for key in fieldnames}
                values["name"] = name
                values["date"] = row["date"]
                writer.writerow(values)


def main():
    yesterday = date.today() - timedelta(days=1)
    date_from = date.today() - timedelta(days=15)

    args = argparse.ArgumentParser("Simple vk ads report fetcher")
    args.add_argument(
        "-o",
        "--output_file",
        required=True,
        type=str,
        default=None,
        help="path to output CSV file",
    )
    args.add_argument(
        "--date_from",
        required=False,
        type=lambda d: datetime.strptime(d, "%Y-%m-%d"),
        default=None,
        help="date to build report from. YYYY-MM-DD format. By default it's two weeks ago",
    )
    args.add_argument(
        "--date_to",
        required=False,
        type=lambda d: datetime.strptime(d, "%Y-%m-%d"),
        default=None,
        help="date to build report to. YYYY-MM-DD format. By default it's yesterday",
    )

    parsed_args = args.parse_args()

    loggingBasicConfig()

    logging.root.setLevel(logging.INFO)

    logger = logging.root

    api = Api(os.getenv("VK_ADS_TOKEN"))

    plans = api.get_all_ad_plans()
    logger.info("Found %s plans", len(plans))

    id_to_name = {plan["id"]: plan["name"] for plan in plans}
    plan_ids = [str(plan["id"]) for plan in plans]

    yesterday = date.today() - timedelta(days=1)
    date_to = parsed_args.date_to or yesterday
    date_from = parsed_args.date_from or date.today() - timedelta(days=15)

    stats = api.get_plans_stats(plan_ids=plan_ids, date_from=date_from, date_to=date_to)

    write_csv(stats, id_to_name, parsed_args.output_file)


main()
