from fastapi import FastAPI
from controllers.User_controllers import user_router
from controllers.Entidad_controllers import entidad_router
from controllers.Mascotas_controllers import mascota_router
from controllers.MascotasExtravidas_controllers import mascotasE_router
from controllers.Donaciones_controllers import donaciones_router
from controllers.DenunciasSeguimiento_controllers import seguimiento_router
from controllers.DenunciasComentarios_controllers import comentario_router
from controllers.Denuncias_controllers import denuncias_router
from controllers.Adopciones_controllers import adopciones_router
from fastapi.staticfiles import StaticFiles
import sys
sys.path.append("C:\\Users\\Milto\\OneDrive\\Documentos\\Api_Multi\\db")

app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(user_router, prefix="/users")
app.include_router(entidad_router, prefix="/entidades")
app.include_router(mascota_router, prefix="/mascotas")
app.include_router(mascotasE_router, prefix="/mascotas-extravidas")
app.include_router(donaciones_router, prefix="/donaciones")
app.include_router(seguimiento_router, prefix="/seguimiento")
app.include_router(comentario_router, prefix="/comentarios")
app.include_router(denuncias_router, prefix="/denuncias")
app.include_router(adopciones_router, prefix="/adopciones")


