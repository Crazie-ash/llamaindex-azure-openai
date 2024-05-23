import pkgutil
import importlib
from fastapi import APIRouter

router = APIRouter()

# Dynamically import all modules in the current package
package = __package__
for _, module_name, _ in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{package}.{module_name}")
    if hasattr(module, "router"):
        router.include_router(module.router)
