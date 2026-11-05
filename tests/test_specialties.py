import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from app.api.api_router import api_router
from app.api.v1.endpoints.especialidades import listar_especialidades
from app.core.initialization import ensure_patient_records, seed_initial_specialty


class SpecialtiesTest(unittest.TestCase):
    def test_specialties_route_is_registered_as_authenticated_get(self):
        route = next(
            route
            for route in api_router.routes
            if getattr(route, "path", None) == "/especialidades"
        )
        self.assertEqual(route.methods, {"GET"})
        self.assertTrue(route.dependant.dependencies)

    def test_patient_record_route_is_registered_as_authenticated_get(self):
        route = next(
            route
            for route in api_router.routes
            if getattr(route, "path", None) == "/pacientes/{id}/prontuario"
        )
        self.assertEqual(route.methods, {"GET"})
        self.assertTrue(route.dependant.dependencies)

    def test_list_returns_database_rows_ordered_by_id(self):
        rows = [SimpleNamespace(id=3, nome="Semiologia", ativo=True)]
        query = Mock()
        query.order_by.return_value = query
        query.all.return_value = rows
        db = Mock()
        db.query.return_value = query

        result = listar_especialidades(db=db, user=SimpleNamespace(id=1))

        self.assertIs(result, rows)
        query.order_by.assert_called_once()

    def test_seed_inserts_semiologia_only_for_empty_table(self):
        db = Mock()
        db.query.return_value.first.return_value = None

        inserted = seed_initial_specialty(db)

        self.assertTrue(inserted)
        specialty = db.add.call_args.args[0]
        self.assertEqual(specialty.nome, "Semiologia")
        self.assertTrue(specialty.ativo)
        db.commit.assert_called_once()

    def test_seed_does_not_duplicate_existing_semiologia(self):
        db = Mock()
        db.query.return_value.filter.return_value.first.return_value = SimpleNamespace(
            nome="Semiologia"
        )

        inserted = seed_initial_specialty(db)

        self.assertFalse(inserted)
        db.add.assert_not_called()
        db.commit.assert_not_called()

    def test_seed_adds_semiologia_when_another_specialty_exists(self):
        db = Mock()
        db.query.return_value.filter.return_value.first.return_value = None

        inserted = seed_initial_specialty(db)

        self.assertTrue(inserted)
        self.assertEqual(db.add.call_args.args[0].nome, "Semiologia")
        db.commit.assert_called_once()

    def test_startup_creates_records_only_for_patients_without_one(self):
        patient = SimpleNamespace(id=12)
        query = Mock()
        query.outerjoin.return_value.filter.return_value.all.return_value = [patient]
        db = Mock()
        db.query.return_value = query

        created_count = ensure_patient_records(db)

        self.assertEqual(created_count, 1)
        created_record = db.add_all.call_args.args[0][0]
        self.assertEqual(created_record.paciente_id, 12)
        db.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
