from django.utils.functional import cached_property

from corehq.apps.locations.models import LocationType, SQLLocation
from custom.icds.location_reassignment.exceptions import InvalidTransitionError
from custom.icds.location_reassignment.utils import deprecate_locations


class Processor(object):
    def __init__(self, domain, transitions, site_codes):
        """
        :param domain: domain
        :param transitions: transitions in format generated by Parser
        :param site_codes: site codes of all locations undergoing transitions
        """
        self.domain = domain
        self.location_type_codes = list(map(lambda lt: lt.code, LocationType.objects.by_domain(self.domain)))
        self.transitions = transitions
        self.site_codes = site_codes

    def process(self):
        # process each sheet, in reverse order of hierarchy
        for location_type_code in list(reversed(self.location_type_codes)):
            for operation, transitions in self.transitions[location_type_code].items():
                self._perform_transitions(operation, transitions)

    def _perform_transitions(self, operation, transitions):
        for old_site_codes, new_site_codes in transitions.items():
            deprecate_locations(self._get_locations(old_site_codes), self._get_locations(new_site_codes),
                                operation)

    def _get_locations(self, site_codes):
        site_codes = site_codes if isinstance(site_codes, list) else [site_codes]
        locations = [self.locations_by_site_code.get(site_code)
                     for site_code in site_codes
                     if self.locations_by_site_code.get(site_code)]
        if len(locations) != len(site_codes):
            loaded_site_codes = [loc.site_code for loc in locations]
            missing_site_codes = set(site_codes) - set(loaded_site_codes)
            raise InvalidTransitionError(
                "Could not load location with following site codes: %s" % ",".join(missing_site_codes))
        return locations

    @cached_property
    def locations_by_site_code(self):
        return {
            loc.site_code: loc
            for loc in SQLLocation.active_objects.filter(site_code__in=self.site_codes)
        }
