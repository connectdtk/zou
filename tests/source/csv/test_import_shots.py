import os

from tests.base import ApiDBTestCase

from zou.app.models.entity_type import EntityType
from zou.app.services import shots_service


class ImportCsvShotsTestCase(ApiDBTestCase):

    def setUp(self):
        super(ImportCsvShotsTestCase, self).setUp()

        self.generate_fixture_project_status()
        self.generate_fixture_project()
        self.generate_fixture_metadata_descriptor(entity_type="Shot")

    def test_import_shots(self):
        path = "/import/csv/projects/%s/shots" % self.project.id

        file_path_fixture = self.get_fixture_file_path(
            os.path.join("csv", "shots.csv")
        )
        self.upload_file(path, file_path_fixture)

        sequences = shots_service.get_sequences()
        self.assertEqual(len(sequences), 3)
        shots = shots_service.get_shots()
        self.assertEqual(len(shots), 4)

        entity_types = EntityType.query.all()
        self.assertEqual(len(entity_types), 3)

        shot = shots[0]
        self.assertEquals(shot["data"].get("contractor", None), "contractor 1")
