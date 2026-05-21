"""
Importación centralizada de modelos ORM.

Esto ayuda a que SQLAlchemy conozca todos los modelos de la aplicación.
"""

from app.models.role import Role
from app.models.user import User
from app.models.team import Team
from app.models.prediction import Prediction, PredictionMatch
from app.models.favorite import Favorite
from app.models.audit import LoginAudit, PredictionAudit