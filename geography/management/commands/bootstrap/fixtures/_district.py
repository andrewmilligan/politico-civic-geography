import json
import os

from tqdm import tqdm

import shapefile
from django.contrib.humanize.templatetags.humanize import ordinal
from geography.models import Division, Geometry


class DistrictFixtures(object):
    def create_district_fixtures(self):
        SHP_SLUG = "cb_{}_us_cd{}_500k".format(self.YEAR, self.CONGRESS)
        DOWNLOAD_PATH = os.path.join(self.DOWNLOAD_DIRECTORY, SHP_SLUG)

        shape = shapefile.Reader(
            os.path.join(DOWNLOAD_PATH, "{}.shp".format(SHP_SLUG))
        )
        fields = shape.fields[1:]
        field_names = [f[0] for f in fields]

        for shp in tqdm(shape.shapeRecords(), desc="Districts"):
            district = dict(zip(field_names, shp.record))
            # Skip territories and DC
            if int(district["STATEFP"]) > 56 or int(district["STATEFP"]) == 11:
                continue

            state = Division.objects.get(
                code=district["STATEFP"], level=self.STATE_LEVEL
            )
            code_key = "CD{}FP".format(self.CONGRESS)
            if int(district[code_key]) == 0:
                label = "{} at-large congressional district".format(
                    state.label, ordinal(int(district[code_key]))
                )
            else:
                label = "{} {} congressional district".format(
                    state.label, ordinal(int(district[code_key]))
                )
            district_obj, created = Division.objects.update_or_create(
                code=district[code_key],
                level=self.DISTRICT_LEVEL,
                parent=state,
                defaults={
                    "name": label,
                    "label": label,
                    "code_components": {
                        "fips": {"state": state.code},
                        "district": district[code_key],
                    },
                },
            )
            geodata = {
                "type": "Feature",
                "geometry": shp.shape.__geo_interface__,
                "properties": {
                    "state": state.code,
                    "district": district[code_key],
                    "name": label,
                },
            }
            geojson, created = Geometry.objects.update_or_create(
                division=district_obj,
                subdivision_level=self.DISTRICT_LEVEL,
                simplification=self.THRESHOLDS["district"],
                source=os.path.join(
                    self.SHP_SOURCE_BASE.format(self.YEAR), SHP_SLUG
                )
                + ".zip",
                series=self.YEAR,
                defaults={
                    "topojson": self.toposimplify(
                        geodata, self.THRESHOLDS["district"]
                    )
                },
            )
            tqdm.write(
                self.TQDM_PREFIX
                + ">  FIPS {}, District {}  @ ~{}kb               ".format(
                    district["STATEFP"],
                    district[code_key],
                    round(len(json.dumps(geojson.topojson)) / 1000),
                )
            )

            geojson, created = Geometry.objects.update_or_create(
                division=district_obj,
                subdivision_level=self.COUNTY_LEVEL,
                simplification=self.THRESHOLDS["county"],
                source=os.path.join(
                    self.SHP_SOURCE_BASE.format(self.YEAR), SHP_SLUG
                )
                + ".zip",
                series=self.YEAR,
                defaults={
                    "topojson": self.get_district_county_shps(
                        district["STATEFP"], district[code_key]
                    )
                },
            )

            tqdm.write(
                self.TQDM_PREFIX
                + ">  FIPS {}, District {}  @ ~{}kb         ".format(
                    district["STATEFP"],
                    district[code_key],
                    round(len(json.dumps(geojson.topojson)) / 1000),
                )
            )
        tqdm.write(self.style.SUCCESS("Done.\n"))
