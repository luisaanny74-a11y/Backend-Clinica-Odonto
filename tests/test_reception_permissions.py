import unittest

from fastapi.routing import APIRoute

from app.api.v1.endpoints.pacientes import router
from domain.enums import PerfilUsuario


def _allowed_profiles(path: str, method: str) -> set[PerfilUsuario]:
    route = next(
        route
        for route in router.routes
        if isinstance(route, APIRoute)
        and route.path == path
        and method in route.methods
    )
    pending = list(route.dependant.dependencies)
    while pending:
        dependency = pending.pop()
        checker = dependency.call
        if getattr(checker, "__name__", "") == "perfil_checker":
            for cell in checker.__closure__ or ():
                value = cell.cell_contents
                if isinstance(value, list) and all(
                    isinstance(profile, PerfilUsuario) for profile in value
                ):
                    return set(value)
        pending.extend(dependency.dependencies)
    raise AssertionError(f"No profile checker found for {method} {path}")


class ReceptionPermissionsTest(unittest.TestCase):
    def test_reception_can_list_and_register_patients(self):
        self.assertIn(PerfilUsuario.RECEPCAO, _allowed_profiles("", "GET"))
        self.assertIn(PerfilUsuario.RECEPCAO, _allowed_profiles("", "POST"))

    def test_reception_cannot_read_clinical_record(self):
        self.assertNotIn(
            PerfilUsuario.RECEPCAO,
            _allowed_profiles("/{id}/prontuario", "GET"),
        )
