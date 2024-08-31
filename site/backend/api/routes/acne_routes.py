from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from fastapi import UploadFile

from service.photo_service import PhotoService
from service.acne_service import AcneService

app_router = APIRouter()
acne_service = AcneService()

@app_router.post('/report')
def post(
    request: Request,
    photo: UploadFile = Depends(PhotoService.validate_photo)
):
    last_model_keras_name = request.app.state.model_keras
    report = acne_service.get_acne_report(photo, last_model_keras_name)
    return Response(str(report), 200)
