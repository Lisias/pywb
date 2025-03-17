import re
import logging
from datetime import datetime, timedelta, timezone

from warcio.timeutils import timestamp_to_datetime, datetime_to_iso_date


class Filter(object):
    def __init__(self, policies:str):
        self.ignore_delta_seconds = None

        policies = policies.replace('revisit:', '').split(";")
        for policy in policies:
            policy = policy.strip()
            match = re.search('older\((.+?)\)', policy)
            if match:
                self.ignore_delta_seconds = self._parse_policy_older(match.group(1))
                continue
            logging.error("WriteRevisitWithConstraintPolicy {:s} doesn't exists!".format(policy));

    def __call__(self, cdx, params):
        dt = timestamp_to_datetime(cdx['timestamp'], True)
        delta = datetime.now(timezone.utc) - dt
        if self.ignore_delta_seconds and delta.total_seconds() < self.ignore_delta_seconds:
            return 'skip'

        return ('revisit', cdx['url'], datetime_to_iso_date(dt))

    def _parse_policy_older(self, params:str):
        params = params.split(",")
        years_num = 0
        months_num = 0
        weeks_num = 0
        days_num = 0
        hours_num = 0

        for param in params:
            try:
                param = param.strip()

                match = re.search('([\.0-9]+?) ?ye?a?r?s?', param)
                if match:
                    years_num = float(match.group(1))
                    continue

                match = re.search('([\.0-9]+?) ?mo?n?t?h?s?', param)
                if match:
                    months_num = float(match.group(1))
                    continue

                match = re.search('([\.0-9]+?) ?we?e?e?k?s?', param)
                if match:
                    weeks_num = float(match.group(1))
                    continue

                match = re.search('([\.0-9]+?) ?da?y?s?', param)
                if match:
                    days_num = float(match.group(1))
                    continue

                match = re.search('([\.0-9]+?) ?ho?u?r?s?', param)
                if match:
                    hours_num = float(match.group(1))
                    continue
            except:
                pass

            logging.error("WriteRevisitWithConstraintPolicy's Older param {:s} is invalid!".format(param))

        months = months_num + 12 * years_num
        weeks = weeks_num + 4 * months
        d = timedelta(weeks=weeks, days=days_num, hours=hours_num)

        return d.total_seconds()
